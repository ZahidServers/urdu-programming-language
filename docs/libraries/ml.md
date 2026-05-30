# Machine Learning Library — اردو/ذہین

The `اردو/ذہین` library brings the full Python ML ecosystem — Pandas, NumPy, TensorFlow/Keras, Scikit-learn, and local LLMs — into the Urdu Programming Language with Urdu-named constructors and methods.

> **اردو:** `اردو/ذہین` لائبریری مشینی سیکھنا (machine learning) کا مکمل ماحول — پانڈاز، نمپائی، ٹینسر فلو/کیراس، سکِٹ-لرن، اور مقامی بڑے لسانی ماڈل — اردو ناموں کے ساتھ فراہم کرتی ہے۔

**Import:**

```urdu
درآمد { پانڈاز, نمپائی, ٹینسر_فلو, کیراس, ترتیبی_ماڈل, درجہ_بندی, ریگریشن, بڑا_لسانی_ماڈل, ڈیٹا } سے "اردو/ذہین"
```

---

## Table of Contents — فہرست مضامین

1. [Pandas — پانڈاز](#pandas--پانڈاز)
2. [NumPy — نمپائی](#numpy--نمپائی)
3. [TensorFlow / Keras — ٹینسر_فلو / کیراس](#tensorflow--keras--ٹینسر_فلو--کیراس)
4. [Scikit-learn — درجہ_بندی / ریگریشن](#scikit-learn--درجہ_بندی--ریگریشن)
5. [LLM — بڑا_لسانی_ماڈل](#llm--بڑا_لسانی_ماڈل)

---

## Pandas — پانڈاز

Pandas provides data manipulation through DataFrames and Series. Construct a Pandas instance first:

> **اردو:** پانڈاز ڈیٹاسیٹ (dataset) کی ترتیب و تجزیہ کے لیے ڈیٹا فریم اور سیریز فراہم کرتا ہے۔ پہلے ایک پانڈاز نمونہ بنائیں۔

```urdu
متغیر pd = نیا پانڈاز()
```

### Constructor

| Call | Description |
|------|-------------|
| `نیا پانڈاز()` | Create a Pandas helper instance |

### Methods — طریقے

| Method | Returns | Description |
|--------|---------|-------------|
| `pd.جدول(ڈکشنری)` | DataFrame | Create a DataFrame from a dictionary of columns |
| `pd.csv_پڑھو(راستہ)` | DataFrame | Read a CSV file from disk |
| `pd.csv_لکھو(df, راستہ)` | path str | Write a DataFrame to a CSV file |
| `pd.excel_پڑھو(راستہ, sheet_name=null)` | DataFrame | Read an Excel file (.xlsx) |
| `pd.excel_لکھو(df, راستہ)` | path str | Write a DataFrame to an Excel file |
| `pd.ملاؤ(df1, df2, on=کالم, how="inner")` | DataFrame | Merge two DataFrames (inner/left/right/outer) |
| `pd.سیریز(ڈیٹا, نام=null)` | Series | Create a Series from a list or dict |

### DataFrame properties and aggregations — ڈیٹا فریم کی خصوصیات

Once you have a DataFrame `df`:

> **اردو:** جب آپ کے پاس ڈیٹا فریم `df` ہو تو یہ اظہارات استعمال کر سکتے ہیں۔

| Expression | Description |
|------------|-------------|
| `df["کالم_نام"]` | Select a column by name |
| `df.shape` | `[rows, columns]` tuple |
| `df.empty` | `سچ` if DataFrame has no rows |
| `df.columns` | List of column names |
| `df["کالم"].mean()` | Arithmetic mean of column |
| `df["کالم"].max()` | Maximum value |
| `df["کالم"].min()` | Minimum value |
| `df["کالم"].sum()` | Sum of all values |
| `df.describe()` | Summary statistics for all numeric columns |

### Example 1 — Create DataFrame and basic statistics

> **اردو:** مثال ۱ — ڈیٹا فریم بنانا اور بنیادی اعداد و شمار

```urdu
درآمد { پانڈاز } سے "اردو/ذہین"

متغیر pd = نیا پانڈاز()

// طلباء کا ڈیٹا بنائیں
متغیر ڈیٹا = {
    "نام":   ["احمد", "فاطمہ", "علی", "زینب", "حسن"],
    "عمر":   [20, 22, 21, 23, 20],
    "نمبر":  [85, 92, 78, 88, 95]
}

متغیر df = pd.جدول(ڈیٹا)

لکھو("ڈیٹا فریم:")
لکھو(df)

لکھو("\nشکل:", df.shape)
لکھو("کالمز:", df.columns)

لکھو("\nاوسط نمبر:", df["نمبر"].mean())
لکھو("زیادہ سے زیادہ:", df["نمبر"].max())
لکھو("کم سے کم:", df["نمبر"].min())
لکھو("مجموعہ:", df["نمبر"].sum())

لکھو("\nتفصیلی اعداد و شمار:")
لکھو(df.describe())
```

### Example 2 — CSV read and write

> **اردو:** مثال ۲ — CSV فائل پڑھنا اور لکھنا

```urdu
درآمد { پانڈاز } سے "اردو/ذہین"

متغیر pd = نیا پانڈاز()

// CSV فائل پڑھیں
متغیر df = pd.csv_پڑھو("فروخت.csv")

لکھو("مجموعی اندراجات:", df.shape[0])
لکھو("کالم:", df.columns)

// فلٹر کریں — صرف وہ قطاریں جہاں فروخت > 1000
متغیر زیادہ_فروخت = df[df["فروخت"] > 1000]
لکھو("1000 سے زیادہ فروخت:", زیادہ_فروخت.shape[0], "اندراجات")

// نتیجہ محفوظ کریں
pd.csv_لکھو(زیادہ_فروخت, "زیادہ_فروخت.csv")
لکھو("فائل محفوظ ہو گئی")
```

### Example 3 — Excel read and write with multiple sheets

> **اردو:** مثال ۳ — ایکسل (excel) فائل پڑھنا اور متعدد ورق (worksheet) لکھنا

```urdu
درآمد { پانڈاز } سے "اردو/ذہین"

متغیر pd = نیا پانڈاز()

// پہلی شیٹ پڑھیں
متغیر df_جنوری = pd.excel_پڑھو("رپورٹ.xlsx", sheet_name="جنوری")
متغیر df_فروری = pd.excel_پڑھو("رپورٹ.xlsx", sheet_name="فروری")

لکھو("جنوری کل:", df_جنوری["فروخت"].sum())
لکھو("فروری کل:", df_فروری["فروخت"].sum())

// دو شیٹس ملائیں
متغیر df_کل = pd.ملاؤ(df_جنوری, df_فروری, on="مصنوع", how="outer")
لکھو("مجموعی ڈیٹا:")
لکھو(df_کل)

// Excel میں محفوظ کریں
pd.excel_لکھو(df_کل, "مجموعی_رپورٹ.xlsx")
لکھو("رپورٹ محفوظ ہو گئی")
```

### Example 4 — Series operations

> **اردو:** مثال ۴ — سیریز کے عمل

```urdu
درآمد { پانڈاز } سے "اردو/ذہین"

متغیر pd = نیا پانڈاز()

// Series بنائیں
متغیر درجہ_حرارت = pd.سیریز([23, 25, 28, 22, 30, 27, 24], نام="درجہ_حرارت")

لکھو("Series:", درجہ_حرارت)
لکھو("اوسط:", درجہ_حرارت.mean())
لکھو("زیادہ:", درجہ_حرارت.max())
لکھو("کم:", درجہ_حرارت.min())
```

---

## NumPy — نمپائی

NumPy provides fast multi-dimensional array operations.

> **اردو:** نمپائی تیز رفتار کثیر الجہتی سرنی (array) عملیات فراہم کرتا ہے۔

```urdu
متغیر np = نیا نمپائی()
```

### Methods — طریقے

| Method | Description |
|--------|-------------|
| `np.سرنی(فہرست)` | Create array from list |
| `np.صفر([m, n])` | m×n array of zeros |
| `np.ایک([m, n])` | m×n array of ones |
| `np.ترتیب(شروع, آخر, قدم)` | Range array (like Python range) |
| `np.شکل_بدلو(سرنی, [m, n])` | Reshape an array |
| `np.مجموع(سرنی)` | Sum of all elements |
| `np.اوسط(سرنی)` | Mean of all elements |
| `np.زیادہ(سرنی)` | Maximum element |
| `np.کم(سرنی)` | Minimum element |
| `np.لاگ(سرنی)` | Element-wise natural log |
| `np.مطلق(سرنی)` | Element-wise absolute value |
| `np.جوڑ(سرنی_1, سرنی_2)` | Concatenate two arrays |

### Example — Matrix operations

> **اردو:** مثال — میٹرکس عملیات

```urdu
درآمد { نمپائی } سے "اردو/ذہین"

متغیر np = نیا نمپائی()

// بنیادی سرنی
متغیر اعداد = np.سرنی([1, 2, 3, 4, 5, 6])
لکھو("سرنی:", اعداد)
لکھو("مجموع:", np.مجموع(اعداد))
لکھو("اوسط:", np.اوسط(اعداد))

// 2D میٹرکس بنائیں
متغیر میٹرکس = np.شکل_بدلو(اعداد, [2, 3])
لکھو("\n2×3 میٹرکس:")
لکھو(میٹرکس)

// صفر اور ایک کی سرنیاں
متغیر صفر_میٹرکس = np.صفر([3, 3])
متغیر ایک_میٹرکس  = np.ایک([3, 3])
لکھو("\nصفر میٹرکس:")
لکھو(صفر_میٹرکس)
لکھو("\nایک میٹرکس:")
لکھو(ایک_میٹرکس)

// حساب
متغیر رینج = np.ترتیب(0, 10, 2)        # [0, 2, 4, 6, 8]
لکھو("\nرینج:", رینج)

متغیر x = np.سرنی([-3, -1, 0, 2, 5])
لکھو("مطلق قدر:", np.مطلق(x))
لکھو("لاگاریتھم (مثبت اعداد):", np.لاگ(np.سرنی([1, 2, 3, 4])))

// دو سرنیاں جوڑیں
متغیر الف = np.سرنی([1, 2, 3])
متغیر ب   = np.سرنی([4, 5, 6])
لکھو("جوڑ:", np.جوڑ(الف, ب))

// عنصر در عنصر ضرب
لکھو("ضرب:", الف * ب)
لکھو("جمع:", الف + ب)
```

---

## TensorFlow / Keras — ٹینسر_فلو / کیراس

Build and train neural networks using the Keras Sequential API.

> **اردو:** کیراس کے ترتیبی ماڈل (Sequential Model) سے عصبی جال (neural network) بنائیں اور تربیت (train) دیں۔

### Layer Functions — پرت فنکشن

Create layers to pass to `ترتیبی_ماڈل`:

> **اردو:** `ترتیبی_ماڈل` میں دینے کے لیے پرتیں (layers) بنائیں۔

| Function | Equivalent | Description |
|----------|-----------|-------------|
| `کیراس.گھنی(یونٹ, فعالیت="relu")` | `Dense` | Fully-connected layer |
| `کیراس.ایل_ایس_ٹی_ایم(یونٹ, واپسی=جھوٹ)` | `LSTM` | Long Short-Term Memory layer |
| `کیراس.تحویل_2ڈی(فلٹر, kernel)` | `Conv2D` | 2D Convolutional layer |
| `کیراس.اخراج(شرح)` | `Dropout` | Regularisation dropout layer |
| `کیراس.بیچ_ضابطہ()` | `BatchNormalization` | Batch normalisation layer |
| `کیراس.سرایت(ذخیرہ, طول)` | `Embedding` | Word/token embedding layer |

### ترتیبی_ماڈل — Sequential Model

```urdu
متغیر ماڈل = نیا ترتیبی_ماڈل()
```

| Method | Description |
|--------|-------------|
| `ماڈل.شامل_کریں(پرت)` | Add a layer to the model |
| `ماڈل.مرتب_کریں(مرتب_کنندہ, نقصان, پیمانے)` | Compile: set optimizer, loss, metrics |
| `ماڈل.سیکھیں(X, y, دور, بیچ)` | Train the model |
| `ماڈل.پیش_گوئی(X)` | Run inference |
| `ماڈل.جانچیں(X, y)` | Evaluate on test data → [loss, accuracy] |
| `ماڈل.محفوظ(راستہ)` | Save model to disk |
| `ماڈل.لوڈ(راستہ)` | Load model from disk |

**Common optimizer strings:** `"adam"`, `"sgd"`, `"rmsprop"`

**Common loss strings:** `"sparse_categorical_crossentropy"`, `"binary_crossentropy"`, `"mse"`

**Common metric strings:** `"accuracy"`, `"mae"`

### Example 1 — Digit classification (MNIST-style)

> **اردو:** مثال ۱ — ہندسوں کی پہچان۔ ماڈل (model) کو تربیت دیں، پھر درستگی (accuracy) جانچیں اور اندازہ لگائیں (predict)۔

```urdu
درآمد { ٹینسر_فلو, کیراس, ترتیبی_ماڈل } سے "اردو/ذہین"

// ═══════════════════════════════════════
// ہندسوں کی پہچان — نیورل نیٹ ورک
// ═══════════════════════════════════════

// MNIST ڈیٹا لوڈ کریں
متغیر [X_تربیت, y_تربیت, X_جانچ, y_جانچ] = ٹینسر_فلو.mnist_لوڈ()

// ڈیٹا 0-1 کے درمیان کریں
X_تربیت = X_تربیت / 255.0
X_جانچ  = X_جانچ  / 255.0

لکھو("تربیتی نمونے:", X_تربیت.shape[0])
لکھو("جانچ نمونے:",  X_جانچ.shape[0])

// ماڈل بنائیں
متغیر ماڈل = نیا ترتیبی_ماڈل()

ماڈل.شامل_کریں(کیراس.گھنی(128, فعالیت="relu"))   # پوشیدہ پرت 1
ماڈل.شامل_کریں(کیراس.اخراج(0.2))                  # اخراج 20%
ماڈل.شامل_کریں(کیراس.گھنی(64, فعالیت="relu"))    # پوشیدہ پرت 2
ماڈل.شامل_کریں(کیراس.گھنی(10, فعالیت="softmax")) # آخری پرت (10 ہندسے)

// مرتب کریں
ماڈل.مرتب_کریں("adam", "sparse_categorical_crossentropy", ["accuracy"])

// تربیت دیں
لکھو("\nتربیت شروع ہو رہی ہے...")
ماڈل.سیکھیں(X_تربیت, y_تربیت, دور=10, بیچ=32)

// جانچیں
متغیر [نقصان, درستگی] = ماڈل.جانچیں(X_جانچ, y_جانچ)
لکھو(`\nجانچ درستگی: ${(درستگی * 100).toFixed(2)}%`)

// پیش گوئی
متغیر نتائج = ماڈل.پیش_گوئی(X_جانچ[0:5])
لکھو("پہلے 5 نمونوں کی پیش گوئی:", نتائج)

// ماڈل محفوظ کریں
ماڈل.محفوظ("ہندسہ_ماڈل.h5")
لکھو("ماڈل محفوظ ہو گیا")
```

### Example 2 — Text Sentiment (LSTM)

> **اردو:** مثال ۲ — LSTM عصبی جال سے متن کے جذبات کا تجزیہ

```urdu
درآمد { کیراس, ترتیبی_ماڈل } سے "اردو/ذہین"

متغیر ذخیرہ_الفاظ = 10000
متغیر زیادہ_طول   = 200

// LSTM ماڈل
متغیر ماڈل = نیا ترتیبی_ماڈل()
ماڈل.شامل_کریں(کیراس.سرایت(ذخیرہ_الفاظ, 64))
ماڈل.شامل_کریں(کیراس.ایل_ایس_ٹی_ایم(64, واپسی=جھوٹ))
ماڈل.شامل_کریں(کیراس.اخراج(0.3))
ماڈل.شامل_کریں(کیراس.گھنی(1, فعالیت="sigmoid"))

ماڈل.مرتب_کریں("adam", "binary_crossentropy", ["accuracy"])
لکھو("LSTM جذبات ماڈل تیار ہے")
```

### Example 3 — Convolutional Image Classifier

> **اردو:** مثال ۳ — تصویری درجہ بندی کے لیے کنوولیوشنل عصبی جال

```urdu
درآمد { کیراس, ترتیبی_ماڈل } سے "اردو/ذہین"

متغیر ماڈل = نیا ترتیبی_ماڈل()

// تصویر کی خصوصیات نکالنا
ماڈل.شامل_کریں(کیراس.تحویل_2ڈی(32, [3, 3], فعالیت="relu"))
ماڈل.شامل_کریں(کیراس.بیچ_ضابطہ())
ماڈل.شامل_کریں(کیراس.تحویل_2ڈی(64, [3, 3], فعالیت="relu"))
ماڈل.شامل_کریں(کیراس.اخراج(0.25))

// درجہ بندی
ماڈل.شامل_کریں(کیراس.گھنی(128, فعالیت="relu"))
ماڈل.شامل_کریں(کیراس.گھنی(10, فعالیت="softmax"))

ماڈل.مرتب_کریں("adam", "sparse_categorical_crossentropy", ["accuracy"])
لکھو("CNN تصویر ماڈل تیار ہے")
```

---

## Scikit-learn — درجہ_بندی / ریگریشن

> **اردو:** سکِٹ-لرن مشینی سیکھنا (machine learning) کے روایتی الگورتھم فراہم کرتا ہے۔ `درجہ_بندی` سے درجہ بندی (classification) اور `ریگریشن` سے مسلسل قدر کا اندازہ لگانا (predict) ممکن ہے۔

### درجہ_بندی — Classification

```urdu
متغیر clf = نیا درجہ_بندی(الگورتھم)
```

**Algorithm strings:**

| Urdu alias | English alias | Algorithm |
|-----------|---------------|-----------|
| `"جنگل"` | `"random_forest"` | Random Forest |
| `"لاجسٹک"` | `"logistic_regression"` | Logistic Regression |
| `"ایس_وی_ایم"` | `"svm"` | Support Vector Machine |
| `"پڑوسی"` | `"knn"` | K-Nearest Neighbours |
| `"درخت"` | `"decision_tree"` | Decision Tree |

| Method | Description |
|--------|-------------|
| `clf.سیکھیں(X, y)` | Train the classifier |
| `clf.پیش_گوئی(X)` | Predict class labels |
| `clf.درستگی(X, y)` | Return accuracy score (0.0–1.0) |

### ریگریشن — Regression

```urdu
متغیر reg = نیا ریگریشن(الگورتھم)
```

**Algorithm strings:**

| Urdu alias | English alias | Algorithm |
|-----------|---------------|-----------|
| `"خطی"` | `"linear"` | Linear Regression |
| `"ridge"` | `"ridge"` | Ridge Regression |
| `"lasso"` | `"lasso"` | Lasso Regression |
| `"جنگل"` | `"random_forest"` | Random Forest Regression |

| Method | Description |
|--------|-------------|
| `reg.سیکھیں(X, y)` | Train the regressor |
| `reg.پیش_گوئی(X)` | Predict continuous values |

### ڈیٹا — Data Utilities

> **اردو:** ڈیٹاسیٹ (dataset) کو تقسیم کرنے، معمول بنانے، اور CSV پڑھنے کے لیے مددگار فنکشن۔

| Method | Description |
|--------|-------------|
| `ڈیٹا.تقسیم(X, y, جانچ=0.2)` | Train/test split → `[X_train, X_test, y_train, y_test]` |
| `ڈیٹا.معمول(X)` | Normalise features to 0–1 range |
| `ڈیٹا.پڑھو_csv(راستہ)` | Read CSV → DataFrame |

### Example — Spam detection with Random Forest

> **اردو:** مثال — رینڈم فارسٹ سے سپیم پیغام پہچاننا۔ ماڈل کو تربیت دیں، درستگی جانچیں، پھر نئے پیغامات پر اندازہ لگائیں۔

```urdu
درآمد { درجہ_بندی, ڈیٹا } سے "اردو/ذہین"

// ═══════════════════════════════════════
// سپیم پیغام پہچاننے والا
// ═══════════════════════════════════════

// ڈیٹا لوڈ کریں
متغیر df = ڈیٹا.پڑھو_csv("پیغامات.csv")

// فیچر اور لیبل الگ کریں
متغیر X = df["خصوصیات"]
متغیر y = df["سپیم"]

// تربیت اور جانچ میں تقسیم (80/20)
متغیر [X_تربیت, X_جانچ, y_تربیت, y_جانچ] = ڈیٹا.تقسیم(X, y, جانچ=0.2)

// معمول بنائیں
X_تربیت = ڈیٹا.معمول(X_تربیت)
X_جانچ  = ڈیٹا.معمول(X_جانچ)

// رینڈم فارسٹ بنائیں اور تربیت دیں
متغیر clf = نیا درجہ_بندی("جنگل")
clf.سیکھیں(X_تربیت, y_تربیت)

// جانچیں
متغیر درستگی = clf.درستگی(X_جانچ, y_جانچ)
لکھو(`درستگی: ${(درستگی * 100).toFixed(1)}%`)

// نئے پیغامات کی پیش گوئی
متغیر نئے_پیغامات = [[0.8, 0.2, 0.9], [0.1, 0.7, 0.1]]
متغیر نتائج = clf.پیش_گوئی(نئے_پیغامات)
لکھو("پیش گوئی:", نتائج)  // [1, 0] — سپیم/نہیں
```

### Example — House price regression

> **اردو:** مثال — خطی ریگریشن سے مکان کی قیمت کا اندازہ لگانا

```urdu
درآمد { ریگریشن, ڈیٹا } سے "اردو/ذہین"

متغیر df = ڈیٹا.پڑھو_csv("مکانات.csv")

متغیر X = df[["رقبہ", "کمرے", "منزل", "عمر"]]
متغیر y = df["قیمت"]

متغیر [X_تربیت, X_جانچ, y_تربیت, y_جانچ] = ڈیٹا.تقسیم(X, y, جانچ=0.2)

متغیر reg = نیا ریگریشن("خطی")
reg.سیکھیں(X_تربیت, y_تربیت)

متغیر پیش_گوئیاں = reg.پیش_گوئی(X_جانچ)
لکھو("پہلے 5 قیمتیں:", پیش_گوئیاں[0:5])
```

---

## LLM — بڑا_لسانی_ماڈل

Run local large language models (GGUF format via llama.cpp) directly from Urdu code.

> **اردو:** مقامی بڑے لسانی ماڈل (LLM) کو اردو کوڈ سے چلائیں۔ یہ GGUF فارمیٹ (llama.cpp) کو سپورٹ کرتا ہے۔

### Constructor

```urdu
متغیر llm = نیا بڑا_لسانی_ماڈل(ماڈل_راستہ, { تھریڈ: 4, طوالت: 512 })
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `تھریڈ` | int | `4` | CPU threads to use |
| `طوالت` | int | `512` | Max tokens to generate |

### Methods — طریقے

| Method | Returns | Description |
|--------|---------|-------------|
| `بڑا_لسانی_ماڈل.متاح()` | bool | Static check — is llama.cpp installed? |
| `llm.بات_کرو(سوال)` | string | Single-turn question → answer |
| `llm.چیٹ(پیغامات)` | string | Multi-turn chat; pass list of `{کردار, مواد}` |
| `llm.ایمبیڈنگ(متن)` | float[] | Get embedding vector for text |

### Example 1 — Simple Q&A

> **اردو:** مثال ۱ — سادہ سوال و جواب

```urdu
درآمد { بڑا_لسانی_ماڈل } سے "اردو/ذہین"

// LLM دستیاب ہے؟
اگر (نہیں بڑا_لسانی_ماڈل.متاح()) {
    لکھو("llama.cpp نصب نہیں — pip install llama-cpp-python")
    عمل_ختم(1)
}

متغیر llm = نیا بڑا_لسانی_ماڈل("ماڈلز/llama-3.gguf", { تھریڈ: 8, طوالت: 256 })

متغیر جواب = llm.بات_کرو("پاکستان کا دارالحکومت کیا ہے؟")
لکھو("جواب:", جواب)
```

### Example 2 — Multi-turn chat

> **اردو:** مثال ۲ — کثیر رخی گفتگو

```urdu
درآمد { بڑا_لسانی_ماڈل } سے "اردو/ذہین"

متغیر llm = نیا بڑا_لسانی_ماڈل("ماڈلز/llama-3.gguf", { طوالت: 512 })

متغیر گفتگو = [
    { کردار: "system",    مواد: "آپ ایک مددگار اردو استاد ہیں۔" },
    { کردار: "user",      مواد: "ضرب کے قواعد سمجھائیں۔" }
]

متغیر جواب_1 = llm.چیٹ(گفتگو)
لکھو("استاد:", جواب_1)

// گفتگو جاری رکھیں
گفتگو.شامل({ کردار: "assistant", مواد: جواب_1 })
گفتگو.شامل({ کردار: "user",      مواد: "ایک مثال دیں۔" })

متغیر جواب_2 = llm.چیٹ(گفتگو)
لکھو("استاد:", جواب_2)
```

### Example 3 — Semantic search with embeddings

> **اردو:** مثال ۳ — ایمبیڈنگ ویکٹر سے معنائی تلاش

```urdu
درآمد { بڑا_لسانی_ماڈل } سے "اردو/ذہین"

متغیر llm = نیا بڑا_لسانی_ماڈل("ماڈلز/embedding.gguf")

متغیر جملے = [
    "آج موسم بہت اچھا ہے",
    "کراچی پاکستان کا بڑا شہر ہے",
    "پروگرامنگ ایک اہم ہنر ہے"
]

// ہر جملے کی ایمبیڈنگ نکالیں
متغیر ویکٹر = []
کے_لیے (متغیر جملہ کا جملے) {
    متغیر v = llm.ایمبیڈنگ(جملہ)
    ویکٹر.شامل(v)
    لکھو(`"${جملہ}" — ویکٹر سائز: ${v.length}`)
}
```

---

*Previous: [Database →](database.md) | Next: [HTTP Client →](http.md)*
