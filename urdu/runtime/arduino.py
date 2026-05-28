"""
اردو/آردوینو — Arduino & Serial Communication Library
Urdu Programming Language

Provides three layers:
  سیریل        — raw pyserial wrapper (any serial device)
  آردوینو       — native pyfirmata2 wrapper (digital, analog, PWM, servo, I2C, callbacks)
  سیریل_آردوینو — lightweight text-command protocol (no Firmata needed)

Board variants:  آردوینو  آردوینو_میگا  آردوینو_نانو  آردوینو_ڈیو

Install:
    urdu نصب اردو/آردوینو

Usage:
    درآمد { آردوینو, اونچا, نیچا, آؤٹ_پٹ, ان_پٹ, PWM_موڈ } سے "اردو/آردوینو";

    بورڈ = آردوینو("COM3")
    بورڈ.پن_موڈ(13, آؤٹ_پٹ)
    بورڈ.بلند_کریں(13)
    بورڈ.تاخیر(1)
    بورڈ.نیچے_کریں(13)
    بورڈ.بند()
"""

from __future__ import annotations
import time as _time
import threading as _threading
from typing import Optional, List, Callable, Any


# ══════════════════════════════════════════════════════════════════════════════
#  Lazy imports
# ══════════════════════════════════════════════════════════════════════════════

def _pyserial():
    try:
        import serial
        return serial
    except ImportError:
        raise ImportError(
            "pyserial نصب کریں:  urdu نصب اردو/آردوینو\n"
            "یا:  pip install pyserial"
        )


def _pyfirmata2():
    try:
        import pyfirmata2
        return pyfirmata2
    except ImportError:
        raise ImportError(
            "pyfirmata2 نصب کریں:  urdu نصب اردو/آردوینو\n"
            "یا:  pip install pyfirmata2\n\n"
            "آردوینو بورڈ پر StandardFirmata sketch بھی ضروری ہے:\n"
            "  Arduino IDE → Examples → Firmata → StandardFirmata"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  Mode constants  (اردو نام ↔ pyfirmata2 integer)
# ══════════════════════════════════════════════════════════════════════════════

اونچا          = HIGH          = 1
نیچا           = LOW           = 0

ان_پٹ          = INPUT         = 0
ان_پٹ_پل_اپ   = INPUT_PULLUP  = 11
آؤٹ_پٹ        = OUTPUT        = 1
اینالاگ_موڈ   = ANALOG        = 2
PWM_موڈ        = PWM           = 3
سرو_موڈ_نام   = SERVO         = 4
DIGITAL        = 1   # internal type tag

# Human-readable mode names (for __repr__)
_MODE_NAMES = {0: "ان_پٹ", 1: "آؤٹ_پٹ", 2: "اینالاگ", 3: "PWM", 4: "سرو", 11: "ان_پٹ_پل_اپ", -1: "غیر_دستیاب"}


# ══════════════════════════════════════════════════════════════════════════════
#  پن  —  First-class pin object
# ══════════════════════════════════════════════════════════════════════════════

class پن:
    """
    First-class Urdu pin object — wraps a pyfirmata2.Pin.

    حاصل کریں:
        ڈیجیٹل پن:  p = بورڈ.ڈیجیٹل(13)
        اینالاگ پن: p = بورڈ.اینالاگ(0)

    پھر:
        p.آؤٹ_پٹ_بنائیں()
        p.لکھو(اونچا)
        p.کال_بیک_مقرر(lambda v: لکھو("قدر:", v))
        قدر = p.پڑھو()
    """

    def __init__(self, _pin, _num: int, _is_analog: bool):
        self._pin        = _pin
        self._num        = _num
        self._is_analog  = _is_analog
        self._last_val   = None
        self._user_cb: Optional[Callable] = None
        # Always register internal capture callback
        self._pin.register_callback(self._capture)

    # ── Internal value capture ────────────────────────────────────────────────

    def _capture(self, value):
        self._last_val = value
        if self._user_cb:
            self._user_cb(value)

    # ── Mode setting ──────────────────────────────────────────────────────────

    def آؤٹ_پٹ_بنائیں(self) -> "پن":
        """Set to digital output."""
        pf = _pyfirmata2()
        self._pin.mode = pf.OUTPUT
        return self

    def ان_پٹ_بنائیں(self, پل_اپ: bool = False) -> "پن":
        """Set to digital input. پل_اپ=True activates internal pull-up resistor."""
        pf = _pyfirmata2()
        self._pin.mode = pf.INPUT_PULLUP if پل_اپ else pf.INPUT
        return self

    def PWM_بنائیں(self) -> "پن":
        """Set to PWM output (0.0–1.0 → 0–255 duty cycle)."""
        pf = _pyfirmata2()
        self._pin.mode = pf.PWM
        return self

    def سرو_بنائیں(self) -> "پن":
        """Set to servo output (0–180 degrees)."""
        pf = _pyfirmata2()
        self._pin.mode = pf.SERVO
        return self

    def اینالاگ_بنائیں(self) -> "پن":
        """Enable analog reporting on this analog pin."""
        self._pin.enable_reporting()
        return self

    # ── Read / Write ──────────────────────────────────────────────────────────

    def لکھو(self, قدر) -> "پن":
        """
        Write a value to the pin:
          OUTPUT → 0/1 (اونچا/نیچا)
          PWM    → float 0.0–1.0  (یا int 0–255, auto-normalised)
          SERVO  → int degrees 0–180
        """
        pf = _pyfirmata2()
        mode = self._pin.mode
        if mode == pf.PWM and isinstance(قدر, int) and قدر > 1:
            # Allow 0-255 convenience — normalise to 0.0-1.0
            قدر = max(0.0, min(1.0, قدر / 255.0))
        self._pin.write(قدر)
        return self

    def پڑھو(self) -> Any:
        """
        Return the most recently received value.
        Analog pins: float 0.0–1.0  (×1023 for raw ADC)
        Digital INPUT: bool
        Requires:
          • analog pin: بورڈ.نمونہ_چالو() یا کال_بیک_مقرر() called
          • digital input: کال_بیک_مقرر() called
        """
        return self._last_val

    def خام_پڑھو(self) -> Optional[int]:
        """Analog only — return raw ADC value 0–1023 (or None if no data yet)."""
        v = self._last_val
        return int(round(v * 1023)) if v is not None else None

    def بلند(self) -> "پن":
        """Write HIGH (digital output shortcut)."""
        return self.لکھو(1)

    def نیچا_کریں(self) -> "پن":
        """Write LOW (digital output shortcut)."""
        return self.لکھو(0)

    def ٹاگل_کریں(self) -> "پن":
        """Toggle digital output pin."""
        current = self._last_val
        return self.لکھو(0 if current else 1)

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def کال_بیک_مقرر(self, fn: Callable) -> "پن":
        """
        Register a callback fired whenever the pin's value changes.
          fn(قدر)  — bool for digital inputs, float 0-1 for analog
        """
        self._user_cb = fn
        return self

    def کال_بیک_ہٹائیں(self) -> "پن":
        """Remove the user callback."""
        self._user_cb = None
        return self

    # ── Reporting ─────────────────────────────────────────────────────────────

    def رپورٹنگ_چالو(self) -> "پن":
        """Enable reporting (analog pins, or digital INPUT)."""
        self._pin.enable_reporting()
        return self

    def رپورٹنگ_بند(self) -> "پن":
        """Disable reporting."""
        self._pin.disable_reporting()
        return self

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def نمبر(self) -> int:
        return self._num

    @property
    def موڈ(self) -> str:
        return _MODE_NAMES.get(self._pin.mode, str(self._pin.mode))

    @property
    def قدر(self) -> Any:
        return self._last_val

    @property
    def اینالاگ_ہے(self) -> bool:
        return self._is_analog

    # ── Syntactic sugar ───────────────────────────────────────────────────────

    def __call__(self, قدر=None) -> Any:
        """پن() → پڑھو()  |  پن(قدر) → لکھو(قدر)"""
        if قدر is None:
            return self.پڑھو()
        return self.لکھو(قدر)

    def __repr__(self) -> str:
        kind = "اینالاگ" if self._is_analog else "ڈیجیٹل"
        return f"<پن {kind}[{self._num}] موڈ={self.موڈ} قدر={self._last_val}>"


# ══════════════════════════════════════════════════════════════════════════════
#  _آردوینو_بنیاد  —  Internal base board wrapper
# ══════════════════════════════════════════════════════════════════════════════

class _آردوینو_بنیاد:
    """
    Internal base — do not instantiate directly.
    Use  آردوینو  آردوینو_میگا  آردوینو_نانو  آردوینو_ڈیو  instead.
    """

    # Subclasses set this to the pyfirmata2 board class name
    _BOARD_CLS = "Arduino"

    def __init__(self, پورٹ: str, *, بوڈ: int = 57600, تاخیر: float = 2.0,
                 نمونہ_وقفہ_ms: int = 19):
        pf = _pyfirmata2()
        cls = getattr(pf, self._BOARD_CLS)
        self._board = cls(پورٹ, baudrate=بوڈ)
        # Start background iterator (keeps incoming data flowing)
        it = pf.util.Iterator(self._board)
        it.daemon = True
        it.start()
        # Give the board time to send firmware info
        _time.sleep(تاخیر)
        # Start analog sampling
        self._board.samplingOn(نمونہ_وقفہ_ms)
        # Cache of پن wrappers
        self._digital_pins: dict[int, پن] = {}
        self._analog_pins:  dict[int, پن] = {}

    # ── Pin access ────────────────────────────────────────────────────────────

    def ڈیجیٹل(self, n: int) -> پن:
        """Return the پن wrapper for digital pin n."""
        if n not in self._digital_pins:
            raw = self._board.digital[n]
            self._digital_pins[n] = پن(raw, n, False)
        return self._digital_pins[n]

    def اینالاگ(self, n: int) -> پن:
        """Return the پن wrapper for analog pin A{n}."""
        if n not in self._analog_pins:
            raw = self._board.analog[n]
            raw.enable_reporting()
            self._analog_pins[n] = پن(raw, n, True)
        return self._analog_pins[n]

    # ── Mode setup ────────────────────────────────────────────────────────────

    def پن_موڈ(self, n: int, موڈ: int) -> "_آردوینو_بنیاد":
        """
        Set digital pin n to the given mode:
          آؤٹ_پٹ | ان_پٹ | ان_پٹ_پل_اپ | PWM_موڈ | سرو_موڈ_نام
        """
        pf = _pyfirmata2()
        self._board.digital[n].mode = موڈ
        return self

    # ── Direct digital I/O ────────────────────────────────────────────────────

    def ڈیجیٹل_لکھو(self, n: int, قدر: int) -> "_آردوینو_بنیاد":
        """Write HIGH (1) or LOW (0) to digital output pin n."""
        pf = _pyfirmata2()
        pin = self._board.digital[n]
        if pin.mode != pf.OUTPUT:
            pin.mode = pf.OUTPUT
        pin.write(1 if قدر else 0)
        return self

    def ڈیجیٹل_پڑھو(self, n: int) -> Optional[bool]:
        """Return the most recently received value from digital input pin n."""
        return self.ڈیجیٹل(n).پڑھو()

    def بلند_کریں(self, n: int) -> "_آردوینو_بنیاد":
        """Set digital pin n HIGH."""
        return self.ڈیجیٹل_لکھو(n, اونچا)

    def نیچے_کریں(self, n: int) -> "_آردوینو_بنیاد":
        """Set digital pin n LOW."""
        return self.ڈیجیٹل_لکھو(n, نیچا)

    def ٹاگل(self, n: int) -> "_آردوینو_بنیاد":
        """Toggle digital output pin n."""
        p = self.ڈیجیٹل(n)
        current = p.قدر
        return self.ڈیجیٹل_لکھو(n, 0 if current else 1)

    # ── Analog I/O ────────────────────────────────────────────────────────────

    def اینالاگ_پڑھو(self, n: int) -> Optional[float]:
        """
        Read analog pin A{n}.
        Returns float 0.0–1.0 (most recent sampled value).
        Multiply by 1023 for raw 10-bit ADC integer.
        """
        return self.اینالاگ(n).پڑھو()

    def اینالاگ_خام(self, n: int) -> Optional[int]:
        """Read analog pin A{n} as raw integer 0–1023."""
        return self.اینالاگ(n).خام_پڑھو()

    def اینالاگ_لکھو(self, n: int, قدر: int) -> "_آردوینو_بنیاد":
        """
        PWM output on digital pin n (must be PWM-capable).
        قدر: 0–255
        """
        pf = _pyfirmata2()
        pin = self._board.digital[n]
        if pin.mode != pf.PWM:
            pin.mode = pf.PWM
        pin.write(max(0.0, min(1.0, قدر / 255.0)))
        return self

    # ── Servo ─────────────────────────────────────────────────────────────────

    def سرو_لکھو(self, n: int, زاویہ: int) -> "_آردوینو_بنیاد":
        """
        Write servo angle (0–180°) to pin n.
        Automatically sets pin to SERVO mode if needed.
        """
        pf = _pyfirmata2()
        pin = self._board.digital[n]
        if pin.mode != pf.SERVO:
            pin.mode = pf.SERVO
        pin.write(max(0, min(180, int(زاویہ))))
        return self

    def سرو_موڈ(self, n: int) -> "_آردوینو_بنیاد":
        """Explicitly set pin n to SERVO mode."""
        pf = _pyfirmata2()
        self._board.digital[n].mode = pf.SERVO
        return self

    # ── Input pullup ──────────────────────────────────────────────────────────

    def ان_پٹ_پل_اپ_موڈ(self, n: int) -> "_آردوینو_بنیاد":
        """Set pin n to INPUT with internal pull-up resistor enabled."""
        pf = _pyfirmata2()
        self._board.digital[n].mode = pf.INPUT_PULLUP
        return self

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def ڈیجیٹل_تبدیلی(self, n: int, fn: Callable) -> "_آردوینو_بنیاد":
        """
        Register callback for digital input pin n.
        fn(قدر: bool) called whenever the pin level changes.
        Pin is automatically set to INPUT mode.
        """
        pf = _pyfirmata2()
        pin = self._board.digital[n]
        if pin.mode not in (pf.INPUT, pf.INPUT_PULLUP):
            pin.mode = pf.INPUT
        self.ڈیجیٹل(n).کال_بیک_مقرر(fn)
        return self

    def اینالاگ_تبدیلی(self, n: int, fn: Callable) -> "_آردوینو_بنیاد":
        """
        Register callback for analog pin A{n}.
        fn(قدر: float) called with value 0.0–1.0 on every sample.
        """
        self.اینالاگ(n).کال_بیک_مقرر(fn)
        return self

    def کال_بیک_ہٹائیں_ڈیجیٹل(self, n: int) -> "_آردوینو_بنیاد":
        """Remove the user callback from digital pin n."""
        self.ڈیجیٹل(n).کال_بیک_ہٹائیں()
        return self

    def کال_بیک_ہٹائیں_اینالاگ(self, n: int) -> "_آردوینو_بنیاد":
        """Remove the user callback from analog pin A{n}."""
        self.اینالاگ(n).کال_بیک_ہٹائیں()
        return self

    # ── Sampling control ──────────────────────────────────────────────────────

    def نمونہ_چالو(self, وقفہ_ms: int = 19) -> "_آردوینو_بنیاد":
        """
        Enable analog sampling. وقفہ_ms: sampling interval in milliseconds.
        19 ms ≈ 52 Hz (Arduino default). Lower = faster but more serial traffic.
        """
        self._board.samplingOn(وقفہ_ms)
        return self

    def نمونہ_بند(self) -> "_آردوینو_بنیاد":
        """Stop analog sampling (saves serial bandwidth when not reading analog)."""
        self._board.samplingOff()
        return self

    def نمونہ_وقفہ(self, ms: int) -> "_آردوینو_بنیاد":
        """Change the sampling interval without stopping/starting."""
        self._board.setSamplingInterval(ms)
        return self

    # ── I2C ───────────────────────────────────────────────────────────────────

    def I2C_آغاز(self, تاخیر_us: int = 0) -> "_آردوینو_بنیاد":
        """
        Enable I2C on the board (sends I2C_CONFIG sysex).
        تاخیر_us: optional delay between reads in microseconds.
        """
        pf = _pyfirmata2()
        d_low  = تاخیر_us & 0x7F
        d_high = (تاخیر_us >> 7) & 0x7F
        self._board.send_sysex(pf.I2C_CONFIG, [d_low, d_high])
        _time.sleep(0.1)
        return self

    def I2C_لکھو(self, پتہ: int, *بائٹس: int) -> "_آردوینو_بنیاد":
        """
        Write bytes to an I2C device at the given 7-bit address.
        مثال: بورڈ.I2C_لکھو(0x3C, 0x00, 0xFF)
        """
        pf = _pyfirmata2()
        # mode byte: bits[1:0] = 00 (write), bits[2] = 0 (7-bit addr)
        data = [پتہ & 0x7F, (پتہ >> 7) & 0x7F, 0b00000000]
        for b in بائٹس:
            data += [b & 0x7F, (b >> 7) & 0x7F]
        self._board.send_sysex(pf.I2C_REQUEST, data)
        return self

    def I2C_پڑھو(self, پتہ: int, تعداد: int,
                  کال_بیک: Callable = None) -> "_آردوینو_بنیاد":
        """
        Request *تعداد* bytes from I2C device at *پتہ*.
        کال_بیک(بائٹس_فہرست) called when reply arrives.
        """
        pf = _pyfirmata2()
        # mode byte: bits[1:0] = 01 (read once)
        data = [
            پتہ & 0x7F, (پتہ >> 7) & 0x7F,
            0b00001000,
            تعداد & 0x7F, (تعداد >> 7) & 0x7F,
        ]
        if کال_بیک:
            def _handler(data):
                کال_بیک(data)
            self._board.add_cmd_handler(pf.I2C_REPLY, _handler)
        self._board.send_sysex(pf.I2C_REQUEST, data)
        return self

    # ── Utility ───────────────────────────────────────────────────────────────

    def چمک(self, n: int = 13, *, تعداد: int = 3,
              وقفہ: float = 0.5) -> "_آردوینو_بنیاد":
        """
        Blink LED on pin *n*.
        بورڈ.چمک(13, تعداد=5, وقفہ=0.2)
        """
        self.پن_موڈ(n, آؤٹ_پٹ)
        for _ in range(تعداد):
            self.بلند_کریں(n)
            _time.sleep(وقفہ)
            self.نیچے_کریں(n)
            _time.sleep(وقفہ)
        return self

    def تاخیر(self, سیکنڈ: float) -> "_آردوینو_بنیاد":
        """Sleep for *سیکنڈ* seconds."""
        _time.sleep(سیکنڈ)
        return self

    def ملی_سیکنڈ(self, ms: int) -> "_آردوینو_بنیاد":
        """Sleep for *ms* milliseconds."""
        _time.sleep(ms / 1000.0)
        return self

    # ── Info ──────────────────────────────────────────────────────────────────

    def نسخہ(self) -> str:
        """Firmware version string reported by the board."""
        name = getattr(self._board, "firmware", "")
        ver  = getattr(self._board, "firmware_version", ())
        return f"{name} {'.'.join(str(v) for v in ver)}" if ver else name

    def پورٹ_نام(self) -> str:
        """Serial port name this board is connected on."""
        return self._board.sp.port

    def ڈیجیٹل_پن_تعداد(self) -> int:
        """Number of digital pins on this board."""
        return len(self._board.digital)

    def اینالاگ_پن_تعداد(self) -> int:
        """Number of analog pins on this board."""
        return len(self._board.analog)

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def بازنشست(self) -> "_آردوینو_بنیاد":
        """Send SYSTEM_RESET to the board."""
        pf = _pyfirmata2()
        self._board.sp.write(bytearray([pf.SYSTEM_RESET]))
        _time.sleep(2.0)
        return self

    def بند(self) -> None:
        """Disconnect from the board and close the serial port."""
        try:
            self._board.samplingOff()
        except Exception:
            pass
        self._board.exit()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.بند()

    def __repr__(self) -> str:
        try:
            fw = self.نسخہ()
            port = self.پورٹ_نام()
        except Exception:
            fw, port = "?", "?"
        return f"<{self.__class__.__name__} پورٹ={port} firmware={fw}>"


# ══════════════════════════════════════════════════════════════════════════════
#  Public board classes
# ══════════════════════════════════════════════════════════════════════════════

class آردوینو(_آردوینو_بنیاد):
    """
    Arduino Uno / Leonardo / compatible (14 digital, 6 analog pins).
    StandardFirmata sketch required.
    """
    _BOARD_CLS = "Arduino"


class آردوینو_میگا(_آردوینو_بنیاد):
    """
    Arduino Mega 2560 (54 digital, 16 analog pins).
    StandardFirmataPlus sketch recommended.
    """
    _BOARD_CLS = "ArduinoMega"


class آردوینو_نانو(_آردوینو_بنیاد):
    """Arduino Nano (compatible with Uno pinout)."""
    _BOARD_CLS = "ArduinoNano"


class آردوینو_ڈیو(_آردوینو_بنیاد):
    """Arduino Due (84 MHz ARM, 3.3 V logic)."""
    _BOARD_CLS = "ArduinoDue"


# ══════════════════════════════════════════════════════════════════════════════
#  I2C helper (standalone)
# ══════════════════════════════════════════════════════════════════════════════

class I2C_آلہ:
    """
    Convenience wrapper around a single I2C device attached to an Arduino.

    استعمال:
        بورڈ.I2C_آغاز()
        آلہ = I2C_آلہ(بورڈ, پتہ=0x3C)   # SSD1306 OLED مثال
        آلہ.لکھو(0x00, 0xAE)            # send command
    """

    def __init__(self, بورڈ: _آردوینو_بنیاد, پتہ: int):
        self._board = بورڈ
        self._addr  = پتہ

    def لکھو(self, *بائٹس: int) -> "I2C_آلہ":
        """Write bytes to this device."""
        self._board.I2C_لکھو(self._addr, *بائٹس)
        return self

    def پڑھو(self, تعداد: int, کال_بیک: Callable = None) -> "I2C_آلہ":
        """Request *تعداد* bytes. Result delivered via *کال_بیک* when ready."""
        self._board.I2C_پڑھو(self._addr, تعداد, کال_بیک)
        return self

    def __repr__(self) -> str:
        return f"<I2C_آلہ پتہ=0x{self._addr:02X}>"


# ══════════════════════════════════════════════════════════════════════════════
#  سیریل  —  Raw pyserial wrapper  (unchanged from v1)
# ══════════════════════════════════════════════════════════════════════════════

class سیریل:
    """
    Urdu-named wrapper around pyserial.Serial.

    استعمال:
        پورٹ = سیریل("COM3", 9600)
        پورٹ.لکھو("ہیلو\\n")
        سطر = پورٹ.سطر_پڑھو()
        پورٹ.بند()
    """

    def __init__(self, پورٹ: str, بوڈ: int = 9600, *,
                 بٹ: int = 8, وقفہ: float = 1.0,
                 لکھنے_کا_وقفہ: float = 1.0):
        serial = _pyserial()
        self._serial = serial.Serial(
            port=پورٹ, baudrate=بوڈ, bytesize=بٹ,
            timeout=وقفہ, write_timeout=لکھنے_کا_وقفہ,
        )
        self._encoding = "utf-8"

    def کھولو(self) -> "سیریل":
        if not self._serial.is_open:
            self._serial.open()
        return self

    def بند(self) -> None:
        if self._serial.is_open:
            self._serial.close()

    def کھلا(self) -> bool:
        return self._serial.is_open

    def صاف(self) -> "سیریل":
        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()
        return self

    def لکھو(self, مواد, انکوڈنگ: str = None) -> int:
        enc = انکوڈنگ or self._encoding
        if isinstance(مواد, str):
            data = مواد.encode(enc)
        elif isinstance(مواد, (bytes, bytearray)):
            data = مواد
        else:
            data = str(مواد).encode(enc)
        return self._serial.write(data)

    def سطر_لکھو(self, سطر: str, انکوڈنگ: str = None) -> int:
        return self.لکھو(سطر.rstrip("\n") + "\n", انکوڈنگ)

    def بائٹ_لکھو(self, قدر: int) -> int:
        return self._serial.write(bytes([قدر & 0xFF]))

    def پڑھو(self, تعداد: int = 1) -> bytes:
        return self._serial.read(تعداد)

    def سطر_پڑھو(self, انکوڈنگ: str = None) -> str:
        enc = انکوڈنگ or self._encoding
        return self._serial.readline().decode(enc, errors="replace").strip()

    def سب_پڑھو(self) -> bytes:
        n = self._serial.in_waiting or 1
        return self._serial.read(n)

    def متن_پڑھو(self, انکوڈنگ: str = None) -> str:
        enc = انکوڈنگ or self._encoding
        return self.سب_پڑھو().decode(enc, errors="replace")

    def بائٹ_پڑھو(self) -> Optional[int]:
        b = self._serial.read(1)
        return b[0] if b else None

    def انتظار(self, تعداد: int = 1) -> bool:
        deadline = _time.monotonic() + (self._serial.timeout or 1.0)
        while _time.monotonic() < deadline:
            if self._serial.in_waiting >= تعداد:
                return True
            _time.sleep(0.001)
        return False

    def دستیاب(self) -> int:
        return self._serial.in_waiting

    def نام(self) -> str:
        return self._serial.port

    def بوڈ_ریٹ(self) -> int:
        return self._serial.baudrate

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.بند()

    def __repr__(self) -> str:
        state = "کھلا" if self.کھلا() else "بند"
        return f"<سیریل {self._serial.port} {self._serial.baudrate} [{state}]>"


# ══════════════════════════════════════════════════════════════════════════════
#  سیریل_آردوینو  —  Simple text-command protocol (no Firmata needed)
# ══════════════════════════════════════════════════════════════════════════════

class سیریل_آردوینو:
    """
    Lightweight serial command wrapper — no Firmata required.
    Pair with a simple Arduino sketch that reads lines and responds.

    Protocol (example sketch):
        "D13:1\\n"  → digitalWrite(13, HIGH)
        "D13:0\\n"  → digitalWrite(13, LOW)
        "A0?\\n"    → analogRead(A0), responds "512\\n"
    """

    def __init__(self, پورٹ: str, بوڈ: int = 9600, *, وقفہ: float = 1.0):
        self._s = سیریل(پورٹ, بوڈ, وقفہ=وقفہ)
        _time.sleep(2.0)   # let Arduino reset after USB connect
        self._s.صاف()

    def ڈیجیٹل_لکھو(self, n: int, قدر: int) -> "سیریل_آردوینو":
        self._s.سطر_لکھو(f"D{n}:{1 if قدر else 0}")
        return self

    def اینالاگ_پڑھو(self, n: int) -> Optional[int]:
        self._s.سطر_لکھو(f"A{n}?")
        resp = self._s.سطر_پڑھو()
        try:
            return int(resp.strip())
        except ValueError:
            return None

    def حکم(self, متن: str) -> str:
        """Send a raw text command and return the response line."""
        self._s.سطر_لکھو(متن)
        return self._s.سطر_پڑھو()

    def بند(self) -> None:
        self._s.بند()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.بند()


# ── Serial port listing ───────────────────────────────────────────────────────

def پورٹ_فہرست() -> List[str]:
    """Return a list of available serial port names on this machine."""
    try:
        from serial.tools.list_ports import comports
        return [p.device for p in comports()]
    except ImportError:
        _pyserial()
        return []


# ══════════════════════════════════════════════════════════════════════════════
#  Exports
# ══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Board classes
    "آردوینو", "آردوینو_میگا", "آردوینو_نانو", "آردوینو_ڈیو",
    # Pin class
    "پن",
    # I2C helper
    "I2C_آلہ",
    # Serial classes
    "سیریل", "سیریل_آردوینو",
    # Constants
    "اونچا", "نیچا",
    "ان_پٹ", "ان_پٹ_پل_اپ", "آؤٹ_پٹ",
    "PWM_موڈ", "سرو_موڈ_نام", "اینالاگ_موڈ",
    # Utility
    "پورٹ_فہرست",
    # English aliases
    "Arduino", "ArduinoMega", "ArduinoNano", "ArduinoDue",
    "Pin", "I2CDevice",
    "Serial", "SerialArduino",
    "HIGH", "LOW", "INPUT", "INPUT_PULLUP", "OUTPUT", "PWM", "SERVO", "ANALOG",
    "list_ports",
]

# English aliases
Arduino       = آردوینو
ArduinoMega   = آردوینو_میگا
ArduinoNano   = آردوینو_نانو
ArduinoDue    = آردوینو_ڈیو
Pin           = پن
I2CDevice     = I2C_آلہ
Serial        = سیریل
SerialArduino = سیریل_آردوینو
list_ports    = پورٹ_فہرست
