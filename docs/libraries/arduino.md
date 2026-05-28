# Arduino / Embedded — اردو/آردوینو

The `اردو/آردوینو` library provides three layers of hardware communication:

| Layer | Class | Protocol | Use when |
|-------|-------|---------|---------|
| `آردوینو` | Native pyfirmata2 | Firmata | Full I/O, PWM, servo, I2C, callbacks |
| `سیریل_آردوینو` | Text-command | Custom UART | No Firmata needed — simple command/response |
| `سیریل` | Raw pyserial | Raw bytes | Any serial device (GPS, Bluetooth, sensors) |

> **اردو:** `اردو/آردوینو` لائبریری تین پرتوں میں Arduino اور سیریل آلات سے جوڑتی ہے — مکمل Firmata سپورٹ سے لے کر خام بائٹ اسٹریم تک۔

**Install:**

```
pip install pyfirmata2 pyserial
```

For `آردوینو` (Firmata) you also need to upload **StandardFirmata** to your board:
`Arduino IDE → File → Examples → Firmata → StandardFirmata`

**Import:**

```urdu
درآمد { آردوینو, پن, اونچا, نیچا, آؤٹ_پٹ, ان_پٹ, ان_پٹ_پل_اپ, PWM_موڈ, سرو_موڈ_نام } سے "اردو/آردوینو"
درآمد { سیریل, سیریل_آردوینو } سے "اردو/آردوینو"
```

---

## آردوینو — Firmata Board

### Supported Board Classes

| Urdu class | pyfirmata2 class | Notes |
|------------|-----------------|-------|
| `آردوینو` | `Arduino` | Uno / standard |
| `آردوینو_میگا` | `ArduinoMega` | Mega 2560 |
| `آردوینو_نانو` | `ArduinoNano` | Nano |
| `آردوینو_ڈیو` | `ArduinoDue` | Due |

### Constructor

```urdu
متغیر بورڈ = نیا آردوینو("COM3")         // Windows
متغیر بورڈ = نیا آردوینو("/dev/ttyUSB0") // Linux
متغیر بورڈ = نیا آردوینو("COM4", باڈ=57600)
```

The board starts the background iterator and analog sampling automatically.

---

### Direct Board Methods

**Digital output — LED blink:**

```urdu
بورڈ.پن_موڈ(13, آؤٹ_پٹ)
بورڈ.بلند_کریں(13)       // HIGH
بورڈ.تاخیر(1)             // 1 second
بورڈ.نیچے_کریں(13)       // LOW
بورڈ.تاخیر(1)
```

**Digital read with pull-up:**

```urdu
بورڈ.پن_موڈ(2, ان_پٹ_پل_اپ)
متغیر حالت = بورڈ.ڈیجیٹل_پڑھو(2)  // True / False
```

**Analog read:**

```urdu
متغیر قدر = بورڈ.اینالاگ_پڑھو(0)    // 0.0 – 1.0 (normalised)
متغیر خام = بورڈ.اینالاگ_خام(0)     // 0 – 1023 (raw ADC)
```

**PWM (LED dimming):**

```urdu
بورڈ.پن_موڈ(9, PWM_موڈ)
بورڈ.اینالاگ_لکھو(9, 0.5)    // 50% duty cycle
```

**Servo:**

```urdu
بورڈ.سرو_لکھو(10, 90)    // 90° (0–180)
```

| Method | Description |
|--------|-------------|
| `.پن_موڈ(پن, موڈ)` | Set pin mode (`ان_پٹ`, `آؤٹ_پٹ`, `PWM_موڈ`, `سرو_موڈ_نام`, `ان_پٹ_پل_اپ`) |
| `.بلند_کریں(پن)` | Set digital pin HIGH |
| `.نیچے_کریں(پن)` | Set digital pin LOW |
| `.ٹاگل(پن)` | Toggle digital pin |
| `.ڈیجیٹل_لکھو(پن, قدر)` | Write `اونچا`/`نیچا` |
| `.ڈیجیٹل_پڑھو(پن)` | Read digital state (`True`/`False`) |
| `.اینالاگ_لکھو(پن, قدر)` | PWM output — `0.0` to `1.0` |
| `.اینالاگ_پڑھو(پن)` | Normalised analog read — `0.0` to `1.0` |
| `.اینالاگ_خام(پن)` | Raw ADC value — `0` to `1023` |
| `.سرو_لکھو(پن, درجہ)` | Set servo angle — `0` to `180` |
| `.تاخیر(ثانیے)` | `time.sleep(ثانیے)` |
| `.بند()` | Disconnect from board |

---

### پن — First-Class Pin Object

Get a pin object for repeated use:

```urdu
متغیر ایل_ای_ڈی = بورڈ.ڈیجیٹل(13)
ایل_ای_ڈی.آؤٹ_پٹ_بنائیں()
ایل_ای_ڈی.لکھو(اونچا)

متغیر بٹن = بورڈ.ڈیجیٹل(2)
بٹن.ان_پٹ_بنائیں(پل_اپ=سچ)
لکھو(بٹن.پڑھو())           // True / False

متغیر روشنی = بورڈ.اینالاگ(0)
لکھو(روشنی.پڑھو())          // 0.0 – 1.0

متغیر موٹر = بورڈ.ڈیجیٹل(9)
موٹر.PWM_بنائیں()
موٹر.لکھو(0.75)              // 75% PWM
```

| Method | Description |
|--------|-------------|
| `.آؤٹ_پٹ_بنائیں()` | Set as OUTPUT |
| `.ان_پٹ_بنائیں(پل_اپ=جھوٹ)` | Set as INPUT or INPUT_PULLUP |
| `.PWM_بنائیں()` | Set as PWM output |
| `.سرو_بنائیں()` | Set as Servo |
| `.لکھو(قدر)` | Write: digital (`اونچا`/`نیچا`) or analog (`0.0`–`1.0`) or servo (`0`–`180`) |
| `.پڑھو()` | Read current value |
| `.خام_پڑھو()` | Raw ADC integer read |
| `.کال_بیک_مقرر(fn)` | Register callback `fn(value)` called on every change |
| `.رپورٹنگ_چالو()` | Enable change reporting to callback |
| `.رپورٹنگ_بند()` | Disable change reporting |

---

### Callbacks — Interrupt-Style

Register a function to be called whenever a pin's value changes — no polling required:

```urdu
متغیر حرکت = بورڈ.ڈیجیٹل(3)
حرکت.ان_پٹ_بنائیں()
حرکت.رپورٹنگ_چالو()
حرکت.کال_بیک_مقرر(فنکشن(قدر) {
    اگر (قدر) {
        لکھو("حرکت محسوس کی!")
    }
})
```

Board-level callbacks by pin number:

```urdu
بورڈ.ڈیجیٹل_تبدیلی(3, فنکشن(قدر) { لکھو("D3:", قدر) })
بورڈ.اینالاگ_تبدیلی(0, فنکشن(قدر) { لکھو("A0:", قدر) })
```

---

### Sampling Control

```urdu
بورڈ.نمونہ_چالو(50)     // sample every 50 ms
بورڈ.نمونہ_وقفہ(100)    // change to 100 ms
بورڈ.نمونہ_بند()         // stop analog sampling
```

---

### I2C

```urdu
بورڈ.I2C_آغاز()
بورڈ.I2C_لکھو(0x68, 0x6B, 0x00)    // (address, register, value)
بورڈ.I2C_پڑھو(0x68, 6, فنکشن(ڈیٹا) {
    لکھو("I2C data:", ڈیٹا)
})
```

---

## سیریل_آردوینو — Text-Command Protocol

No Firmata needed — communicate with any sketch that reads/writes text over Serial.

```urdu
درآمد { سیریل_آردوینو } سے "اردو/آردوینو";

متغیر ارد = نیا سیریل_آردوینو("COM3")

// بھیجیں
ارد.بھیجیں("LED:ON")
ارد.بھیجیں("MOTOR:128")

// پڑھیں
متغیر جواب = ارد.پڑھیں()       // reads one line (strips \r\n)
متغیر جواب = ارد.پڑھیں(0.5)    // with 0.5s timeout

// حلقہ
ارد.حلقہ(فنکشن(سطر) {
    لکھو("Arduino said:", سطر)
})

ارد.بند()
```

| Method | Description |
|--------|-------------|
| `.بھیجیں(متن)` | Send a line (appends `\n`) |
| `.پڑھیں(ختمی=1.0)` | Read one line — returns string or `None` on timeout |
| `.حلقہ(fn)` | Blocking loop — calls `fn(line)` for every received line |
| `.بند()` | Close serial port |

---

## سیریل — Raw Serial

Direct pyserial wrapper for any serial device:

```urdu
درآمد { سیریل } سے "اردو/آردوینو";

متغیر پورٹ = نیا سیریل("COM3", باڈ=9600, ختمی=2.0)

پورٹ.لکھو(b"hello\n")         // write bytes
پورٹ.متن_لکھو("hello\n")      // write string as UTF-8

متغیر بائٹس = پورٹ.پڑھو(10)   // read exactly 10 bytes
متغیر سطر   = پورٹ.سطر_پڑھو() // read until \n

پورٹ.صاف_کریں()               // flush buffers
پورٹ.بند()
```

| Method | Description |
|--------|-------------|
| `.لکھو(بائٹس)` | Write raw bytes |
| `.متن_لکھو(متن)` | Write UTF-8 encoded string |
| `.پڑھو(تعداد)` | Read n bytes |
| `.سطر_پڑھو()` | Read until `\n` |
| `.دستیاب()` | Number of bytes waiting to be read |
| `.صاف_کریں()` | Flush input/output buffers |
| `.بند()` | Close port |

---

## Mode Constants — موڈ مستقل

| Urdu constant | Value | Description |
|---------------|-------|-------------|
| `اونچا` / `HIGH` | `1` | Digital HIGH |
| `نیچا` / `LOW` | `0` | Digital LOW |
| `ان_پٹ` / `INPUT` | `0` | Digital input |
| `ان_پٹ_پل_اپ` / `INPUT_PULLUP` | `11` | Input with pull-up resistor |
| `آؤٹ_پٹ` / `OUTPUT` | `1` | Digital output |
| `اینالاگ_موڈ` / `ANALOG` | `2` | Analog input |
| `PWM_موڈ` / `PWM` | `3` | PWM output |
| `سرو_موڈ_نام` / `SERVO` | `4` | Servo output |

---

## Common Recipes

**Blink an LED:**

```urdu
متغیر بورڈ = نیا آردوینو("COM3")
بورڈ.پن_موڈ(13, آؤٹ_پٹ)
جبکہ (سچ) {
    بورڈ.ٹاگل(13)
    بورڈ.تاخیر(0.5)
}
```

**Read a potentiometer:**

```urdu
متغیر بورڈ = نیا آردوینو("COM3")
متغیر پوٹ = بورڈ.اینالاگ(0)
جبکہ (سچ) {
    لکھو(`A0: ${پوٹ.پڑھو():.2f}`)
    بورڈ.تاخیر(0.1)
}
```

**Servo sweep:**

```urdu
متغیر بورڈ = نیا آردوینو("COM3")
متغیر سرو = بورڈ.ڈیجیٹل(9)
سرو.سرو_بنائیں()
کے_لیے (متغیر زاویہ کا حد(0, 181, 5)) {
    سرvo.لکھو(زاویہ)
    بورڈ.تاخیر(0.05)
}
```
