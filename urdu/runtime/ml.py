"""
Machine Learning library for the Urdu Programming Language.
Wraps: TensorFlow/Keras, PyTorch, scikit-learn, llama-cpp-python.

Usage from Urdu:
    درآمد { TensorFlow, ماڈل_بنائیں, Dense, LSTM } سے "اردو/ذہین";
"""

from __future__ import annotations
from typing import Any, Optional


# ─── TensorFlow / Keras ───────────────────────────────────────────────────────

class _TensorFlow:
    """Lazy-loaded TensorFlow wrapper."""

    def __init__(self):
        self._tf = None

    def _load(self):
        if self._tf is None:
            try:
                import tensorflow as tf
                self._tf = tf
            except ImportError:
                raise ImportError("TensorFlow کے لیے چلائیں: pip install tensorflow")
        return self._tf

    def __getattr__(self, name):
        return getattr(self._load(), name)

    def مستقل(self, value):
        return self._load().constant(value)

    def متغیر(self, value):
        return self._load().Variable(value)

    def تبدیل(self, x, dtype=None):
        return self._load().cast(x, dtype or self._load().float32)


TensorFlow = _TensorFlow()


class _Keras:
    """Keras API wrapper."""

    def __init__(self):
        self._keras = None

    def _load(self):
        if self._keras is None:
            try:
                import tensorflow as tf
                self._keras = tf.keras
            except ImportError:
                try:
                    import keras
                    self._keras = keras
                except ImportError:
                    raise ImportError("Keras کے لیے چلائیں: pip install tensorflow")
        return self._keras

    def __getattr__(self, name):
        return getattr(self._load(), name)

Keras = _Keras()


# ─── Layer wrappers ───────────────────────────────────────────────────────────

class گھنی:
    """Keras Dense layer."""
    def __new__(cls, units: int, *, فعالیت: str = "relu", **kwargs):
        try:
            from tensorflow.keras.layers import Dense as KerasDense
        except ImportError:
            raise ImportError("pip install tensorflow")
        return KerasDense(units, activation=فعالیت, **kwargs)


class ایل_ایس_ٹی_ایم:
    """Keras LSTM layer."""
    def __new__(cls, units: int, *, واپسی: bool = False, **kwargs):
        try:
            from tensorflow.keras.layers import LSTM as KerasLSTM
        except ImportError:
            raise ImportError("pip install tensorflow")
        return KerasLSTM(units, return_sequences=واپسی, **kwargs)


class تحویل_2ڈی:
    """Keras Conv2D layer."""
    def __new__(cls, فلٹر: int, kernel=(3, 3), *, فعالیت: str = "relu", **kwargs):
        try:
            from tensorflow.keras.layers import Conv2D as KerasConv2D
        except ImportError:
            raise ImportError("pip install tensorflow")
        return KerasConv2D(فلٹر, kernel, activation=فعالیت, **kwargs)


class اخراج:
    """Keras Dropout layer."""
    def __new__(cls, شرح: float = 0.5):
        try:
            from tensorflow.keras.layers import Dropout as KerasDropout
        except ImportError:
            raise ImportError("pip install tensorflow")
        return KerasDropout(شرح)


class بیچ_ضابطہ:
    """Keras BatchNormalization."""
    def __new__(cls):
        try:
            from tensorflow.keras.layers import BatchNormalization as BN
        except ImportError:
            raise ImportError("pip install tensorflow")
        return BN()


class سرایت:
    """Keras Embedding layer."""
    def __new__(cls, ذخیرہ: int, طول: int, **kwargs):
        try:
            from tensorflow.keras.layers import Embedding as KerasEmbed
        except ImportError:
            raise ImportError("pip install tensorflow")
        return KerasEmbed(ذخیرہ, طول, **kwargs)


# ─── Sequential model ─────────────────────────────────────────────────────────

class ترتیبی_ماڈل:
    """Sequential Keras model with Urdu API."""

    def __init__(self, پرتیں: list = None):
        try:
            from tensorflow.keras import Sequential
        except ImportError:
            raise ImportError("pip install tensorflow")
        self._model = Sequential(پرتیں or [])

    def شامل_کریں(self, پرت):
        self._model.add(پرت)
        return self

    def مرتب_کریں(self, *, مرتب_کنندہ="adam",
                  نقصان="sparse_categorical_crossentropy",
                  پیمانے=None):
        self._model.compile(
            optimizer=مرتب_کنندہ,
            loss=نقصان,
            metrics=پیمانے or ["accuracy"]
        )
        return self

    def سیکھیں(self, X, y, *, دور=10, بیچ=32,
               تصدیق=None, خاموش=False):
        vh = (تصدیق[0], تصدیق[1]) if تصدیق else None
        return self._model.fit(
            X, y, epochs=دور, batch_size=بیچ,
            validation_data=vh,
            verbose=0 if خاموش else 1
        )

    def پیش_گوئی(self, X):
        return self._model.predict(X)

    def جانچیں(self, X, y):
        return self._model.evaluate(X, y)

    def محفوظ(self, راستہ: str):
        self._model.save(راستہ)
        return self

    @staticmethod
    def لوڈ(راستہ: str):
        try:
            from tensorflow.keras.models import load_model
        except ImportError:
            raise ImportError("pip install tensorflow")
        obj = ترتیبی_ماڈل.__new__(ترتیبی_ماڈل)
        obj._model = load_model(راستہ)
        return obj

    def خلاصہ(self, input_shape=None):
        if input_shape is not None:
            self._model.build((None, *input_shape) if not isinstance(input_shape[0], tuple) else input_shape)
        try:
            self._model.summary()
        except ValueError:
            print(f"  (ماڈل ابھی بنا نہیں — پہلے input_shape دیں یا ڈیٹا پر چلائیں)")

    def __repr__(self):
        return f"ترتیبی_ماڈل(پرتیں={len(self._model.layers)})"

Sequential = ترتیبی_ماڈل


# ─── Scikit-learn wrappers ────────────────────────────────────────────────────

class درجہ_بندی:
    """Classification wrapper (scikit-learn)."""

    def __init__(self, الگورتھم: str = "random_forest", **kwargs):
        try:
            import sklearn
        except ImportError:
            raise ImportError("scikit-learn کے لیے چلائیں: pip install scikit-learn")
        self._clf = self._create(الگورتھم, **kwargs)

    def _create(self, algo, **kw):
        algo = algo.lower().replace(" ", "_").replace("-", "_")
        if algo in ("random_forest", "جنگل"):
            from sklearn.ensemble import RandomForestClassifier
            return RandomForestClassifier(**kw)
        if algo in ("logistic_regression", "لاجسٹک"):
            from sklearn.linear_model import LogisticRegression
            return LogisticRegression(**kw)
        if algo in ("svm", "ایس_وی_ایم"):
            from sklearn.svm import SVC
            return SVC(**kw)
        if algo in ("knn", "پڑوسی"):
            from sklearn.neighbors import KNeighborsClassifier
            return KNeighborsClassifier(**kw)
        if algo in ("decision_tree", "درخت"):
            from sklearn.tree import DecisionTreeClassifier
            return DecisionTreeClassifier(**kw)
        if algo in ("gradient_boosting", "ترقی"):
            from sklearn.ensemble import GradientBoostingClassifier
            return GradientBoostingClassifier(**kw)
        raise ValueError(f"نامعلوم الگورتھم: {algo}")

    def سیکھیں(self, X, y):
        self._clf.fit(X, y)
        return self

    def پیش_گوئی(self, X):
        return self._clf.predict(X)

    def درستگی(self, X, y) -> float:
        from sklearn.metrics import accuracy_score
        return accuracy_score(y, self._clf.predict(X))


class ریگریشن:
    """Regression wrapper (scikit-learn)."""

    def __init__(self, الگورتھم: str = "linear", **kwargs):
        try:
            import sklearn
        except ImportError:
            raise ImportError("pip install scikit-learn")
        self._reg = self._create(الگورتھم, **kwargs)

    def _create(self, algo, **kw):
        algo = algo.lower()
        if algo in ("linear", "خطی"):
            from sklearn.linear_model import LinearRegression
            return LinearRegression(**kw)
        if algo in ("ridge",):
            from sklearn.linear_model import Ridge
            return Ridge(**kw)
        if algo in ("lasso",):
            from sklearn.linear_model import Lasso
            return Lasso(**kw)
        if algo in ("random_forest", "جنگل"):
            from sklearn.ensemble import RandomForestRegressor
            return RandomForestRegressor(**kw)
        raise ValueError(f"نامعلوم الگورتھم: {algo}")

    def سیکھیں(self, X, y):
        self._reg.fit(X, y)
        return self

    def پیش_گوئی(self, X):
        return self._reg.predict(X)


# ─── LLM (llama.cpp) ─────────────────────────────────────────────────────────

class بڑا_لسانی_ماڈل:
    """Large Language Model using llama-cpp-python."""

    def __init__(self, ماڈل_راستہ: str, *, تھریڈ: int = 4,
                 طوالت: int = 512, جی_پی_یو: bool = False,
                 ایمبیڈنگ_موڈ: bool = False):
        try:
            from llama_cpp import Llama
        except ImportError:
            raise ImportError("LLM کے لیے چلائیں: pip install llama-cpp-python")
        self._llm = Llama(
            model_path=ماڈل_راستہ,
            n_threads=تھریڈ,
            n_ctx=طوالت,
            n_gpu_layers=999 if جی_پی_یو else 0,
            embedding=ایمبیڈنگ_موڈ,
            verbose=False,
        )
        self._max_tokens = طوالت

    @classmethod
    def متاح(cls) -> bool:
        """Returns True if llama-cpp-python is installed."""
        try:
            from llama_cpp import Llama
            return True
        except ImportError:
            return False

    def بات_کرو(self, سوال: str, *, زیادہ_ٹوکن: int = 200,
                درجہ_حرارت: float = 0.7) -> str:
        result = self._llm(
            سوال,
            max_tokens=زیادہ_ٹوکن,
            temperature=درجہ_حرارت,
            stop=["###", "\n\n"],
        )
        return result["choices"][0]["text"].strip()

    def چیٹ(self, پیغامات: list[dict], *, زیادہ_ٹوکن: int = 500) -> str:
        result = self._llm.create_chat_completion(
            messages=پیغامات,
            max_tokens=زیادہ_ٹوکن,
        )
        return result["choices"][0]["message"]["content"]

    def ایمبیڈنگ(self, متن: str) -> list[float]:
        return self._llm.create_embedding(متن)["data"][0]["embedding"]


# ─── Data preprocessing ───────────────────────────────────────────────────────

class ڈیٹا:
    """Data preprocessing utilities."""

    @staticmethod
    def تقسیم(X, y, *, جانچ: float = 0.2, بیج: int = 42):
        try:
            from sklearn.model_selection import train_test_split
        except ImportError:
            raise ImportError("pip install scikit-learn")
        return train_test_split(X, y, test_size=جانچ, random_state=بیج)

    @staticmethod
    def معمول(X):
        try:
            from sklearn.preprocessing import StandardScaler
        except ImportError:
            raise ImportError("pip install scikit-learn")
        sc = StandardScaler()
        return sc.fit_transform(X)

    @staticmethod
    def بائنری(y, کلاسیں=None):
        try:
            from sklearn.preprocessing import LabelBinarizer
        except ImportError:
            raise ImportError("pip install scikit-learn")
        lb = LabelBinarizer()
        if کلاسیں:
            lb.fit(کلاسیں)
        return lb.fit_transform(y)

    @staticmethod
    def پڑھو_csv(راستہ: str, **kwargs):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas کے لیے چلائیں: pip install pandas")
        return pd.read_csv(راستہ, **kwargs)


# ─── PyTorch ─────────────────────────────────────────────────────────────────

class _پائی_ٹارچ:
    """PyTorch wrapper."""

    def __init__(self):
        self._torch = None

    def _load(self):
        if self._torch is None:
            try:
                import torch
                self._torch = torch
            except ImportError:
                raise ImportError("PyTorch کے لیے چلائیں: pip install torch")
        return self._torch

    def __getattr__(self, name):
        return getattr(self._load(), name)

    def ٹینسر(self, data):
        return self._load().tensor(data, dtype=self._load().float32)

    def ماڈل(self):
        import torch.nn as nn
        return nn.Sequential()


torch = _پائی_ٹارچ()
پائی_ٹارچ = torch
PyTorch = _پائی_ٹارچ


# ─── NumPy ────────────────────────────────────────────────────────────────────

class نمپائی:
    """NumPy wrapper with Urdu API."""

    def __init__(self):
        try:
            import numpy as np
            self._np = np
        except ImportError:
            raise ImportError("numpy کے لیے چلائیں: pip install numpy")

    def __getattr__(self, name):
        return getattr(self._np, name)

    def سرنی(self, data):
        return self._np.array(data)

    def صفر(self, shape):
        return self._np.zeros(shape)

    def ایک(self, shape):
        return self._np.ones(shape)

    def جوڑ(self, a, b):
        return float(self._np.dot(a, b))

    def ترتیب(self, *args):
        return self._np.arange(*args)

    def شکل_بدلو(self, a, shape):
        return self._np.reshape(a, shape)

    def مجموع(self, a):
        return float(self._np.sum(a))

    def اوسط(self, a):
        return float(self._np.mean(a))

    def زیادہ(self, a):
        return float(self._np.max(a))

    def کم(self, a):
        return float(self._np.min(a))

    def لاگ(self, a):
        return self._np.log(a)

    def مطلق(self, a):
        return self._np.abs(a)


# ─── Pandas ───────────────────────────────────────────────────────────────────

class پانڈاز:
    """Pandas wrapper with Urdu API."""

    def __init__(self):
        try:
            import pandas as pd
            self._pd = pd
        except ImportError:
            raise ImportError("pandas کے لیے چلائیں: pip install pandas")

    def __getattr__(self, name):
        return getattr(self._pd, name)

    def جدول(self, data, ستون=None):
        import pandas as pd
        d = dict(data) if isinstance(data, dict) else data
        return pd.DataFrame(d, columns=ستون)

    def csv_پڑھو(self, راستہ, **kwargs):
        import pandas as pd
        return pd.read_csv(راستہ, **kwargs)

    def csv_لکھو(self, df, راستہ, **kwargs):
        kwargs.setdefault("index", False)
        df.to_csv(راستہ, **kwargs)
        return راستہ

    def excel_پڑھو(self, راستہ, **kwargs):
        import pandas as pd
        return pd.read_excel(راستہ, **kwargs)

    def excel_لکھو(self, df, راستہ, **kwargs):
        kwargs.setdefault("index", False)
        df.to_excel(راستہ, **kwargs)
        return راستہ

    def ملاؤ(self, left, right, **kwargs):
        import pandas as pd
        return pd.merge(left, right, **kwargs)

    def سیریز(self, data, *, نام=None):
        import pandas as pd
        return pd.Series(data, name=نام)


# ─── Singleton / class aliases ───────────────────────────────────────────────

ٹینسر_فلو = TensorFlow
کیراس = Keras
Numpy = نمپائی
Pandas = پانڈاز

# ─── Backward-compat English aliases ─────────────────────────────────────────

Dense = گھنی
LSTM = ایل_ایس_ٹی_ایم
Conv2D = تحویل_2ڈی
Dropout = اخراج
BatchNormalization = بیچ_ضابطہ
Embedding = سرایت
LLM = بڑا_لسانی_ماڈل

# ─── Exports ─────────────────────────────────────────────────────────────────

__all__ = [
    # Urdu names — primary
    "ٹینسر_فلو", "کیراس",
    "گھنی", "ایل_ایس_ٹی_ایم", "تحویل_2ڈی", "اخراج", "بیچ_ضابطہ", "سرایت",
    "ترتیبی_ماڈل",
    "درجہ_بندی", "ریگریشن",
    "بڑا_لسانی_ماڈل",
    "ڈیٹا",
    "torch", "پائی_ٹارچ",
    "نمپائی", "پانڈاز",
    # English backward-compat
    "TensorFlow", "Keras",
    "Dense", "LSTM", "Conv2D", "Dropout", "BatchNormalization", "Embedding",
    "Sequential",
    "LLM",
    "PyTorch",
    "Numpy", "Pandas",
]
