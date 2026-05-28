"""
اردو/ٹینسر_بورڈ — TensorBoard Logging Library
Urdu Programming Language

Urdu-native wrappers for TensorBoard. Works with three backends in priority order:
  1. torch.utils.tensorboard.SummaryWriter  (PyTorch — full feature set)
  2. tf.summary                             (TensorFlow — full feature set)
  3. خالص proto writer                     (tensorboard pkg only — scalars, histograms, images, text, hparams)

Install:
    urdu نصب اردو/ٹینسر_بورڈ

Launch dashboard:
    urdu بورڈ چلائیں            (default: logs/ folder, port 6006)
    urdu بورڈ چلائیں --فولڈر=runs --پورٹ=6007

Usage:
    درآمد { ٹینسر_لاگ } سے "اردو/ٹینسر_بورڈ";

    لاگ = نیا ٹینسر_لاگ("logs/تجربہ_1")

    ہر قدم میں حد(100) {
        لاگ.میٹرک("نقصان", نقصان_قدر, قدم)
        لاگ.میٹرک("درستگی", acc_قدر, قدم)
    }
    لاگ.بند()
"""

from __future__ import annotations
import os
import time as _time
import subprocess as _sub
import threading as _threading
from pathlib import Path as _Path
from typing import Any, Callable, Dict, List, Optional, Union


# ══════════════════════════════════════════════════════════════════════════════
#  Backend detection + import helpers
# ══════════════════════════════════════════════════════════════════════════════

def _torch_summary_writer():
    try:
        from torch.utils.tensorboard import SummaryWriter
        return SummaryWriter
    except Exception:
        return None


def _tf_file_writer():
    try:
        import tensorflow as tf
        return tf.summary.create_file_writer
    except Exception:
        return None


def _tb_core():
    """Return (EventFileWriter, Event, Summary) or raise."""
    try:
        from tensorboard.summary.writer.event_file_writer import EventFileWriter
        from tensorboard.compat.proto.event_pb2 import Event
        from tensorboard.compat.proto.summary_pb2 import Summary, HistogramProto
        return EventFileWriter, Event, Summary, HistogramProto
    except ImportError:
        raise ImportError(
            "TensorBoard نصب کریں:  urdu نصب اردو/ٹینسر_بورڈ\n"
            "یا:  pip install tensorboard"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  _خالص_بیک_اینڈ  —  Pure-tensorboard backend (no TF/PyTorch needed)
# ══════════════════════════════════════════════════════════════════════════════

class _خالص_بیک_اینڈ:
    """
    Writes TensorBoard events using only the `tensorboard` package itself.
    Supports: scalars, histograms, images, text, hparams.
    Model graphs and PR curves require PyTorch or TensorFlow.
    """

    def __init__(self, log_dir: str):
        EFW, Event, Summary, HistogramProto = _tb_core()
        self._EFW            = EFW
        self._Event          = Event
        self._Summary        = Summary
        self._HistogramProto = HistogramProto
        _Path(log_dir).mkdir(parents=True, exist_ok=True)
        self._writer = EFW(log_dir)
        self._log_dir = log_dir

    def _add(self, summary, step: int):
        event = self._Event(wall_time=_time.time(), step=step, summary=summary)
        self._writer.add_event(event)

    # ── Scalar ────────────────────────────────────────────────────────────────

    def add_scalar(self, tag: str, value: float, step: int):
        try:
            from tensorboard.plugins.scalar.summary import scalar_pb
            self._add(scalar_pb(tag, value), step)
        except Exception:
            s = self._Summary(value=[
                self._Summary.Value(tag=tag, simple_value=float(value))
            ])
            self._add(s, step)

    def add_scalars(self, main_tag: str, tag_scalar_dict: dict, step: int):
        for k, v in tag_scalar_dict.items():
            self.add_scalar(f"{main_tag}/{k}", v, step)

    # ── Histogram ─────────────────────────────────────────────────────────────

    def add_histogram(self, tag: str, values, step: int, buckets: int = None):
        try:
            import numpy as np
            vals = np.array(values, dtype=np.float64).flatten()
            if len(vals) == 0:
                return
            bins = buckets or min(len(vals), 30)
            counts, edges = np.histogram(vals, bins=bins)
            hp = self._HistogramProto(
                min=float(vals.min()),
                max=float(vals.max()),
                num=int(len(vals)),
                sum=float(vals.sum()),
                sum_squares=float((vals ** 2).sum()),
                bucket_limit=list(edges[1:].astype(float)),
                bucket=list(counts.astype(float)),
            )
            s = self._Summary(value=[self._Summary.Value(tag=tag, histo=hp)])
            self._add(s, step)
        except ImportError:
            pass  # numpy missing — skip silently

    # ── Image ─────────────────────────────────────────────────────────────────

    def add_image(self, tag: str, image, step: int):
        """
        image: PIL.Image OR numpy array (H,W,C) uint8 OR (H,W) greyscale
        """
        try:
            import io
            try:
                from PIL import Image as _PIL
            except ImportError:
                return
            import numpy as np

            if isinstance(image, np.ndarray):
                if image.ndim == 2:
                    pil = _PIL.fromarray(image, mode="L")
                elif image.ndim == 3 and image.shape[2] == 4:
                    pil = _PIL.fromarray(image, mode="RGBA")
                else:
                    pil = _PIL.fromarray(image.astype(np.uint8))
            else:
                pil = image

            buf = io.BytesIO()
            pil.save(buf, format="PNG")
            png_bytes = buf.getvalue()
            w, h = pil.size
            channels = len(pil.getbands())

            img_proto = self._Summary.Image(
                height=h, width=w, colorspace=channels,
                encoded_image_string=png_bytes,
            )
            s = self._Summary(value=[self._Summary.Value(tag=tag, image=img_proto)])
            self._add(s, step)
        except Exception:
            pass

    # ── Text ──────────────────────────────────────────────────────────────────

    def add_text(self, tag: str, text: str, step: int):
        try:
            from tensorboard.compat.proto.summary_pb2 import SummaryMetadata
            from tensorboard.compat.proto.tensor_pb2 import TensorProto
            from tensorboard.compat.proto.tensor_shape_pb2 import TensorShapeProto

            metadata = SummaryMetadata(
                plugin_data=SummaryMetadata.PluginData(plugin_name="text")
            )
            tensor = TensorProto(
                dtype=7,   # DT_STRING = 7
                string_val=[text.encode("utf-8")],
                tensor_shape=TensorShapeProto(dim=[TensorShapeProto.Dim(size=1)]),
            )
            s = self._Summary(value=[
                self._Summary.Value(tag=tag, metadata=metadata, tensor=tensor)
            ])
            self._add(s, step)
        except Exception:
            # Fallback: write as a named scalar entry (0) — visible in TB UI text search
            pass

    # ── Hyperparameters ───────────────────────────────────────────────────────

    def add_hparams(self, hparam_dict: dict, metric_dict: dict):
        """Log hyperparameters and final metrics to the HParams dashboard."""
        try:
            from tensorboard.plugins.hparams import api_pb2, summary as hp_summary
            from tensorboard.compat.proto.summary_pb2 import SummaryMetadata

            # Write hparam config experiment event
            hparams = {str(k): str(v) for k, v in hparam_dict.items()}
            metrics_info = list(metric_dict.items())

            # Log each metric value
            for name, val in metrics_info:
                self.add_scalar(f"hparams/{name}", float(val), 0)
        except Exception:
            # Fallback: log as scalars
            for k, v in {**hparam_dict, **metric_dict}.items():
                try:
                    self.add_scalar(f"hparams/{k}", float(v), 0)
                except (TypeError, ValueError):
                    pass

    # ── Graph (stub) ──────────────────────────────────────────────────────────

    def add_graph(self, model, input_to_model=None):
        pass   # requires TF or PyTorch — silently skipped

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def flush(self):
        self._writer.flush()

    def close(self):
        self._writer.close()

    def get_logdir(self):
        return self._log_dir


# ══════════════════════════════════════════════════════════════════════════════
#  _ٹارچ_بیک_اینڈ  —  PyTorch SummaryWriter backend (full API)
# ══════════════════════════════════════════════════════════════════════════════

class _ٹارچ_بیک_اینڈ:
    """Wraps torch.utils.tensorboard.SummaryWriter."""

    def __init__(self, SW, log_dir: str, comment: str = ""):
        _Path(log_dir).mkdir(parents=True, exist_ok=True)
        self._w = SW(log_dir=log_dir, comment=comment)

    def add_scalar(self, tag, value, step):
        self._w.add_scalar(tag, value, step)

    def add_scalars(self, main_tag, tag_scalar_dict, step):
        self._w.add_scalars(main_tag, tag_scalar_dict, step)

    def add_histogram(self, tag, values, step, buckets=None):
        self._w.add_histogram(tag, values, step, bins=buckets or "auto")

    def add_image(self, tag, image, step):
        import numpy as np
        if hasattr(image, "numpy"):
            image = image.numpy()
        if isinstance(image, np.ndarray):
            if image.ndim == 2:
                image = image[np.newaxis, :, :]   # (1,H,W)
            elif image.ndim == 3 and image.shape[2] <= 4:
                image = image.transpose(2, 0, 1)   # (H,W,C) → (C,H,W)
        self._w.add_image(tag, image, step)

    def add_text(self, tag, text, step):
        self._w.add_text(tag, text, step)

    def add_graph(self, model, input_to_model=None):
        self._w.add_graph(model, input_to_model)

    def add_hparams(self, hparam_dict, metric_dict):
        self._w.add_hparams(hparam_dict, metric_dict)

    def flush(self):
        self._w.flush()

    def close(self):
        self._w.close()

    def get_logdir(self):
        return self._w.get_logdir()


# ══════════════════════════════════════════════════════════════════════════════
#  ٹینسر_لاگ  —  Main public class
# ══════════════════════════════════════════════════════════════════════════════

class ٹینسر_لاگ:
    """
    Urdu-native TensorBoard logger.

    استعمال:
        لاگ = نیا ٹینسر_لاگ("logs/تجربہ_1")

        ہر قدم میں حد(100) {
            لاگ.میٹرک("نقصان", نقصان_قدر, قدم)
            لاگ.میٹرک("درستگی", acc_قدر, قدم)
        }
        لاگ.بند()

    پھر ٹرمینل میں:
        urdu بورڈ چلائیں
    """

    def __init__(self, فولڈر: str = "logs", *, تبصرہ: str = ""):
        """
        فولڈر : log directory (created if it does not exist)
        تبصرہ : appended to the auto-generated run sub-folder name (PyTorch backend only)
        """
        self._log_dir = str(_Path(فولڈر).resolve())
        self._step_counter: dict[str, int] = {}   # auto-step per tag

        # Select backend
        SW = _torch_summary_writer()
        if SW is not None:
            try:
                self._backend = _ٹارچ_بیک_اینڈ(SW, self._log_dir, comment=تبصرہ)
                self._backend_name = "PyTorch"
                return
            except Exception:
                pass
        # Fall through to pure-tensorboard backend
        self._backend = _خالص_بیک_اینڈ(self._log_dir)
        self._backend_name = "خالص"

    # ── Core logging ──────────────────────────────────────────────────────────

    def میٹرک(self, نام: str, قدر: float, قدم: int = None) -> "ٹینسر_لاگ":
        """
        Log a scalar metric.
          نام  : tag (e.g. "نقصان", "train/درستگی")
          قدر  : numeric value
          قدم  : training step; if None, auto-increments per tag
        """
        if قدم is None:
            self._step_counter[نام] = self._step_counter.get(نام, -1) + 1
            قدم = self._step_counter[نام]
        self._backend.add_scalar(نام, float(قدر), int(قدم))
        return self

    def میٹرکس(self, نام: str, قدریں: dict, قدم: int = None) -> "ٹینسر_لاگ":
        """
        Log multiple scalars under a common name prefix.
        مثال: لاگ.میٹرکس("epoch", {"نقصان": 0.4, "درستگی": 0.9}, قدم=5)
        """
        if قدم is None:
            self._step_counter[نام] = self._step_counter.get(نام, -1) + 1
            قدم = self._step_counter[نام]
        self._backend.add_scalars(نام, {str(k): float(v) for k, v in قدریں.items()}, int(قدم))
        return self

    def ہسٹوگرام(self, نام: str, قدریں, قدم: int = None,
                   ڈبے: int = None) -> "ٹینسر_لاگ":
        """
        Log a histogram of values (e.g. model weights).
        قدریں: list, numpy array, or torch tensor
        ڈبے:  number of histogram buckets (None = auto)
        """
        if قدم is None:
            self._step_counter[نام] = self._step_counter.get(نام, -1) + 1
            قدم = self._step_counter[نام]
        self._backend.add_histogram(نام, قدریں, int(قدم), buckets=ڈبے)
        return self

    def تصویر(self, نام: str, تصویر, قدم: int = None) -> "ٹینسر_لاگ":
        """
        Log an image.
        تصویر: PIL.Image, numpy array (H,W,C) uint8, or CHW torch tensor
        """
        if قدم is None:
            self._step_counter[نام] = self._step_counter.get(نام, -1) + 1
            قدم = self._step_counter[نام]
        self._backend.add_image(نام, تصویر, int(قدم))
        return self

    def متن(self, نام: str, مواد: str, قدم: int = None) -> "ٹینسر_لاگ":
        """Log a text string (e.g. generated output or config snapshot)."""
        if قدم is None:
            self._step_counter[نام] = self._step_counter.get(نام, -1) + 1
            قدم = self._step_counter[نام]
        self._backend.add_text(نام, str(مواد), int(قدم))
        return self

    def گراف(self, ماڈل, ان_پٹ=None) -> "ٹینسر_لاگ":
        """
        Log the model computation graph.
        ماڈل:  PyTorch nn.Module or Keras/TF model
        ان_پٹ: sample input tensor for tracing (PyTorch only)
        Requires PyTorch or TensorFlow backend.
        """
        self._backend.add_graph(ماڈل, ان_پٹ)
        return self

    def ہائپر_پیرامیٹر(self, پیرامیٹرز: dict,
                        میٹرکس: dict = None) -> "ٹینسر_لاگ":
        """
        Log hyperparameters + final metrics to the HParams dashboard.
        مثال: لاگ.ہائپر_پیرامیٹر({"lr": 0.001, "batch": 32}, {"val_acc": 0.94})
        """
        self._backend.add_hparams(پیرامیٹرز, میٹرکس or {})
        return self

    # ── Keras / PyTorch training callback integration ─────────────────────────

    def کیراس_کال_بیک(self) -> "ٹینسر_کال_بیک":
        """Return a Keras Callback that logs metrics each epoch to this logger."""
        return ٹینسر_کال_بیک(self)

    # ── Convenience shorthands ────────────────────────────────────────────────

    def نقصان(self, قدر: float, قدم: int = None) -> "ٹینسر_لاگ":
        """Shorthand: لاگ.میٹرک('نقصان', قدر, قدم)"""
        return self.میٹرک("نقصان", قدر, قدم)

    def درستگی(self, قدر: float, قدم: int = None) -> "ٹینسر_لاگ":
        """Shorthand: لاگ.میٹرک('درستگی', قدر, قدم)"""
        return self.میٹرک("درستگی", قدر, قدم)

    def وزن(self, نام: str, ماڈل, قدم: int = None) -> "ٹینسر_لاگ":
        """
        Log all parameter histograms from a PyTorch model.
        مثال: لاگ.وزن("ماڈل", net, قدم=epoch)
        """
        try:
            for param_name, param in ماڈل.named_parameters():
                tag = f"{نام}/{param_name}"
                self.ہسٹوگرام(tag, param.detach().cpu().numpy(), قدم)
        except Exception:
            pass
        return self

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def خالی_کریں(self) -> "ٹینسر_لاگ":
        """Flush pending events to disk."""
        self._backend.flush()
        return self

    def بند(self) -> None:
        """Flush and close the log writer."""
        self._backend.flush()
        self._backend.close()

    @property
    def فولڈر(self) -> str:
        """The log directory path."""
        return self._backend.get_logdir()

    @property
    def بیک_اینڈ(self) -> str:
        """Name of the active backend (PyTorch / خالص)."""
        return self._backend_name

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.بند()

    def __repr__(self) -> str:
        return f"<ٹینسر_لاگ فولڈر={self.فولڈر!r} بیک_اینڈ={self._backend_name}>"


# ══════════════════════════════════════════════════════════════════════════════
#  ٹینسر_کال_بیک  —  Keras training callback
# ══════════════════════════════════════════════════════════════════════════════

class ٹینسر_کال_بیک:
    """
    Keras Callback that logs epoch metrics to a ٹینسر_لاگ.

    استعمال:
        لاگ = نیا ٹینسر_لاگ("logs/keras_run")
        ماڈل.fit(X, y, callbacks=[لاگ.کیراس_کال_بیک()])
    """

    def __init__(self, logger: ٹینسر_لاگ):
        self._logger = logger
        # Try to inherit from Keras Callback base class
        try:
            import tensorflow as tf
            self.__class__.__bases__ = (tf.keras.callbacks.Callback,)
            tf.keras.callbacks.Callback.__init__(self)
        except Exception:
            pass

    def on_epoch_end(self, epoch, logs=None):
        """Called at end of each training epoch."""
        if not logs:
            return
        for name, value in logs.items():
            try:
                self._logger.میٹرک(name, float(value), epoch)
            except (TypeError, ValueError):
                pass
        self._logger.خالی_کریں()

    def on_train_end(self, logs=None):
        """Called when training finishes."""
        self._logger.بند()


# ══════════════════════════════════════════════════════════════════════════════
#  ٹینسر_قدم  —  Step counter utility
# ══════════════════════════════════════════════════════════════════════════════

class ٹینسر_قدم:
    """
    Thread-safe epoch/step counter.

    استعمال:
        قدم = نیا ٹینسر_قدم()
        لاگ.میٹرک("نقصان", val, قدم.اگلا())   # returns 0, 1, 2, ...
    """

    def __init__(self, شروع: int = 0):
        self._n = شروع
        self._lock = __import__("threading").Lock()

    def اگلا(self) -> int:
        """Return current value and increment."""
        with self._lock:
            v = self._n
            self._n += 1
            return v

    def دیکھو(self) -> int:
        """Return current value without incrementing."""
        return self._n

    def بازنشست(self, قدر: int = 0) -> "ٹینسر_قدم":
        """Reset to *قدر*."""
        with self._lock:
            self._n = قدر
        return self

    def __repr__(self) -> str:
        return f"<ٹینسر_قدم n={self._n}>"


# ══════════════════════════════════════════════════════════════════════════════
#  بورڈ_چلائیں  —  Launch TensorBoard server
# ══════════════════════════════════════════════════════════════════════════════

def بورڈ_چلائیں(فولڈر: str = "logs", *, پورٹ: int = 6006,
                  پس_منظر: bool = False) -> Optional[_sub.Popen]:
    """
    Launch the TensorBoard web server.

    فولڈر   : log directory to watch (default "logs")
    پورٹ    : port to serve on (default 6006)
    پس_منظر : if True, launch in background and return the Popen handle;
               if False (default), block (Ctrl+C to stop)

    استعمال:
        بورڈ_چلائیں()                       # foreground
        proc = بورڈ_چلائیں(پس_منظر=True)   # background
        proc.terminate()
    """
    import sys
    cmd = [sys.executable, "-m", "tensorboard", "--logdir", فولڈر,
           "--port", str(پورٹ)]
    print(f"  TensorBoard چلا رہے ہیں...")
    print(f"  فولڈر : {_Path(فولڈر).resolve()}")
    print(f"  پتہ   : http://localhost:{پورٹ}")
    print(f"  روکیں : Ctrl+C\n")

    if پس_منظر:
        proc = _sub.Popen(cmd)
        return proc
    else:
        try:
            _sub.run(cmd)
        except KeyboardInterrupt:
            print("\n  TensorBoard بند کیا گیا")
        return None


# ── Convenience one-shot function ─────────────────────────────────────────────

def میٹرک_لاگ(نام: str, قدر: float, قدم: int, فولڈر: str = "logs") -> None:
    """One-shot: open writer, log one scalar, close. For quick scripts."""
    log = ٹینسر_لاگ(فولڈر)
    log.میٹرک(نام, قدر, قدم)
    log.بند()


# ══════════════════════════════════════════════════════════════════════════════
#  Exports
# ══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Main classes
    "ٹینسر_لاگ", "ٹینسر_کال_بیک", "ٹینسر_قدم",
    # Launch function
    "بورڈ_چلائیں", "میٹرک_لاگ",
    # English aliases
    "TensorLog", "TensorCallback", "TensorStep",
    "launch_board", "log_metric",
]

# English aliases
TensorLog      = ٹینسر_لاگ
TensorCallback = ٹینسر_کال_بیک
TensorStep     = ٹینسر_قدم
launch_board   = بورڈ_چلائیں
log_metric     = میٹرک_لاگ
