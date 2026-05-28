# TensorBoard — اردو/ٹینسر_بورڈ

The `اردو/ٹینسر_بورڈ` library provides Urdu-named wrappers for TensorBoard — log training metrics, plot histograms, display images and text, record hyperparameters, and launch the TensorBoard dashboard from your Urdu ML programs.

> **اردو:** `اردو/ٹینسر_بورڈ` لائبریری TensorBoard کے لیے اردو نامی ریپر فراہم کرتی ہے — تربیتی میٹرک لاگ کریں، ہسٹوگرام اور تصاویر ریکارڈ کریں، ہائپر پیرامیٹر محفوظ کریں، اور TensorBoard ڈیش بورڈ چلائیں۔

**Install:**

```
pip install tensorboard
```

For full feature support (model graphs, PR curves), also install PyTorch or TensorFlow. The library auto-selects the best available backend.

**Import:**

```urdu
درآمد { ٹینسر_لاگ, ٹینسر_قدم, بورڈ_چلائیں, میٹرک_لاگ } سے "اردو/ٹینسر_بورڈ"
```

---

## Backend Auto-Selection

The library tries three backends in order:

| Priority | Backend | Requires |
|----------|---------|---------|
| 1 | `torch.utils.tensorboard.SummaryWriter` | PyTorch |
| 2 | `tf.summary` | TensorFlow |
| 3 | Pure-tensorboard proto writer | `tensorboard` package only |

All backends support scalars, histograms, images, text, and HParams. Model graphs and PR curves require PyTorch or TensorFlow.

---

## ٹینسر_لاگ — Main Logger

### Constructor

```urdu
متغیر لاگ = نیا ٹینسر_لاگ("logs/تجربہ_1")
متغیر لاگ = نیا ٹینسر_لاگ("runs/آج", تبصرہ="lr=0.01")
```

| Parameter | Description |
|-----------|-------------|
| `فولڈر` (positional) | Directory to write event files |
| `تبصرہ` | Appended to folder name for easy identification |

---

### Scalar Logging — میٹرک لاگ

```urdu
کے_لیے (متغیر قدم کا حد(100)) {
    لاگ.میٹرک("تربیت/نقصان", نقصان_قدر, قدم)
    لاگ.میٹرک("تربیت/درستگی", درستگی_قدر, قدم)
}
```

Log multiple scalars under one prefix:

```urdu
لاگ.میٹرکس("epoch", { "نقصان": 0.5, "درستگی": 0.85 }, قدم=10)
```

Convenience shorthands:

```urdu
لاگ.نقصان(0.42, قدم=5)
لاگ.درستگی(0.91, قدم=5)
```

| Method | Description |
|--------|-------------|
| `.میٹرک(نام, قدر, قدم)` | Log one scalar |
| `.میٹرکس(نام, قدریں_ڈکٹ, قدم)` | Log multiple scalars under a prefix |
| `.نقصان(قدر, قدم)` | Shorthand for `loss` |
| `.درستگی(قدر, قدم)` | Shorthand for `accuracy` |

---

### Histogram Logging

```urdu
لاگ.ہسٹوگرام("وزن/پہلی_پرت", ماڈل.fc1.weight.data, قدم=0)
```

| Method | Description |
|--------|-------------|
| `.ہسٹوگرام(نام, قدریں, قدم)` | Log a histogram; `قدریں` can be a NumPy array or list |

Requires NumPy. Silently skipped if NumPy is not installed.

---

### Image Logging

```urdu
لاگ.تصویر("نمونے/آدان", تصویر_سرنی, قدم=0)
```

Accepts a PIL Image, or a NumPy array of shape `(H, W, C)` uint8 or `(H, W)` greyscale.

| Method | Description |
|--------|-------------|
| `.تصویر(نام, تصویر, قدم)` | Log an image (PIL or NumPy) |

Requires NumPy and Pillow. Silently skipped if not available.

---

### Text Logging

```urdu
لاگ.متن("نمونے/پیشگوئی", "یہ جملہ ہے", قدم=1)
```

| Method | Description |
|--------|-------------|
| `.متن(نام, مواد, قدم)` | Log a text string to the Text tab |

---

### HParams (Hyperparameter Tracking)

```urdu
لاگ.ہائپر_پیرامیٹر(
    { "سیکھنے_کی_شرح": 0.001, "بیچ_سائز": 32, "پرتیں": 3 },
    { "بہترین_درستگی": 0.94 }
)
```

| Method | Description |
|--------|-------------|
| `.ہائپر_پیرامیٹر(پیرامیٹرز, میٹرکس)` | Log hyperparameters + final metrics to the HParams tab |

---

### Weights Logging

```urdu
لاگ.وزن("ماڈل/وزن", ماڈل, قدم=epoch)
```

| Method | Description |
|--------|-------------|
| `.وزن(نام, ماڈل, قدم)` | Log all named parameter histograms of a PyTorch model |

---

### Keras Callback

Drop-in callback for `model.fit()` with TensorFlow/Keras:

```urdu
متغیر کال_بیک = لاگ.کیراس_کال_بیک()
ماڈل.fit(X_train, y_train, callbacks=[کال_بیک], epochs=50)
```

| Method | Description |
|--------|-------------|
| `.کیراس_کال_بیک()` | Returns a `tf.keras.callbacks.TensorBoard`-compatible callback |

---

### Flush and Close

```urdu
لاگ.بند()
```

Always call `.بند()` after the training loop to flush buffered events to disk.

---

## ٹینسر_قدم — Thread-Safe Step Counter

Automatically increments a step counter — useful when training across multiple threads or loops.

```urdu
متغیر قدم_گن = نیا ٹینسر_قدم()

کے_لیے (متغیر batch کا ڈیٹا_لوڈر) {
    لاگ.میٹرک("نقصان", نقصان, قدم_گن.اگلا())   // returns 0, 1, 2, ...
}

لکھو(قدم_گن.موجودہ())    // current step
قدم_گن.بازنشست(0)        // reset to 0
```

| Method | Description |
|--------|-------------|
| `.اگلا()` | Return current step and increment — thread-safe |
| `.موجودہ()` | Read current step without incrementing |
| `.بازنشست(قدر=0)` | Reset to given value |

---

## بورڈ_چلائیں — Launch Dashboard

```urdu
بورڈ_چلائیں("logs")                     // opens http://localhost:6006
بورڈ_چلائیں("runs", پورٹ=7007)
بورڈ_چلائیں("logs", پس_منظر=سچ)        // non-blocking
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `فولڈر` | `"logs"` | Log directory to read from |
| `پورٹ` | `6006` | HTTP port for the dashboard |
| `پس_منظر` | `جھوٹ` | `True` → non-blocking (returns a `subprocess.Popen`) |

---

## میٹرک_لاگ — One-Shot Convenience

Log a single scalar without managing a `ٹینسر_لاگ` instance:

```urdu
میٹرک_لاگ("val/درستگی", 0.93, قدم=100)
میٹرک_لاگ("val/نقصان", 0.12, قدم=100, فولڈر="runs/exp2")
```

Opens a writer, logs the scalar, then closes — suitable for quick scripts.

---

## Full Training Loop Example

```urdu
درآمد { ٹینسر_لاگ, ٹینسر_قدم, بورڈ_چلائیں } سے "اردو/ٹینسر_بورڈ";

متغیر لاگ    = نیا ٹینسر_لاگ("logs/تربیت")
متغیر قدم_گن = نیا ٹینسر_قدم()

لاگ.ہائپر_پیرامیٹر(
    { "سیکھنے_کی_شرح": 0.001, "epochs": 10 },
    { "بہترین_درستگی": 0.0 }
)

کے_لیے (متغیر epoch کا حد(10)) {
    متغیر نقصان    = تربیت_قدم()
    متغیر درستگی   = جانچ_قدم()

    لاگ.نقصان(نقصان, قدم_گن.اگلا())
    لاگ.درستگی(درستگی, قدم_گن.موجودہ())
    لکھو(`Epoch ${epoch}: loss=${نقصان}, acc=${درستگی}`)
}

لاگ.بند()
بورڈ_چلائیں("logs")
```

---

## CLI Command

Launch TensorBoard from the terminal without writing Urdu code:

```
urdu بورڈ چلائیں                   # default: logs/ folder, port 6006
urdu بورڈ چلائیں --فولڈر=runs
urdu بورڈ چلائیں --پورٹ=7007
```
