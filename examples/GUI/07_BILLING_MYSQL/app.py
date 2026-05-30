# ═══════════════════════════════════════
# اردو پروگرامنگ لینگویج — Generated Code
# Developer: Mohammed Zahid Wadiwale
# Version  : 1.0.1
# ═══════════════════════════════════════
from __future__ import annotations
import asyncio, sys, os
from urdu.runtime.builtins import *

# urdu:8
from urdu.runtime.gui import گوئی
from urdu.runtime.gui import کنٹینر
from urdu.runtime.gui import فریم
from urdu.runtime.gui import ردیف
from urdu.runtime.gui import کالم
from urdu.runtime.gui import لیبل
from urdu.runtime.gui import بٹن
from urdu.runtime.gui import ان_پٹ
from urdu.runtime.gui import جدول
from urdu.runtime.gui import ٹیب_ویو
from urdu.runtime.gui import ڈائیلاگ
# urdu:9
import mysql.connector as mysql_connector
# urdu:10
import datetime as datetime
# urdu:13
ترتیب = _UrduObj({'host': 'localhost', 'user': 'root', 'password': '', 'port': 3306})
# urdu:20

def جوڑو():
    # urdu:21
    con = mysql_connector.connect(host = ترتیب['host'], user = ترتیب['user'], password = ترتیب['password'], port = ترتیب['port'])
    # urdu:22
    cur = con.cursor()
    # urdu:23
    cur.execute('CREATE DATABASE IF NOT EXISTS urdu_billing CHARACTER SET utf8mb4')
    # urdu:24
    cur.execute('USE urdu_billing')
    # urdu:25
    cur.executemany('SELECT 1', [])
    # urdu:26
    con.commit()
    # urdu:27
    cur.close()
    # urdu:28
    con.close()
    # urdu:29
    db = mysql_connector.connect(database = 'urdu_billing', host = ترتیب['host'], user = ترتیب['user'], password = ترتیب['password'], port = ترتیب['port'])
    # urdu:30
    db.autocommit = True
    # urdu:31
    return db

# urdu:34
try:
    # urdu:35
    ڈی_بی = جوڑو()
    # urdu:36
    ڈی_بی_cur = ڈی_بی.cursor()
    # urdu:37
    ڈی_بی_cur.execute(f"CREATE TABLE IF NOT EXISTS مصنوعات (\n        id INT AUTO_INCREMENT PRIMARY KEY,\n        نام VARCHAR(200) NOT NULL,\n        قیمت DECIMAL(10,2) NOT NULL DEFAULT 0,\n        مقدار INT NOT NULL DEFAULT 0\n    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
    # urdu:43
    ڈی_بی_cur.execute(f"CREATE TABLE IF NOT EXISTS گاہک (\n        id INT AUTO_INCREMENT PRIMARY KEY,\n        نام VARCHAR(200) NOT NULL,\n        فون VARCHAR(50) DEFAULT '',\n        پتہ VARCHAR(300) DEFAULT ''\n    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
    # urdu:49
    ڈی_بی_cur.execute(f"CREATE TABLE IF NOT EXISTS بل (\n        id INT AUTO_INCREMENT PRIMARY KEY,\n        گاہک_id INT NOT NULL,\n        تاریخ VARCHAR(20) NOT NULL,\n        کل DECIMAL(10,2) NOT NULL DEFAULT 0\n    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
    # urdu:55
    ڈی_بی_cur.execute(f"CREATE TABLE IF NOT EXISTS بل_اشیاء (\n        id INT AUTO_INCREMENT PRIMARY KEY,\n        بل_id INT NOT NULL,\n        مصنوع_نام VARCHAR(200) NOT NULL,\n        مقدار INT NOT NULL DEFAULT 1,\n        قیمت DECIMAL(10,2) NOT NULL DEFAULT 0\n    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
    # urdu:62
    ڈی_بی.commit()
    # urdu:63
    ڈی_بی_cur.close()
    # urdu:64
    جڑا = True
except Exception as e:
    if not hasattr(e, 'پیغام'): e.پیغام = str(e)
    # urdu:66
    جڑا = False
    # urdu:67
    print(f"MySQL کنکشن خطا: {e}")
# urdu:70

def سوال(sql, params):
    # urdu:71
    try:
        # urdu:72
        cur = ڈی_بی.cursor(dictionary = True)
        # urdu:73
        cur.execute(sql, (params or []))
        # urdu:74
        نتائج = cur.fetchall()
        # urdu:75
        cur.close()
        # urdu:76
        return نتائج
    except Exception as e:
        if not hasattr(e, 'پیغام'): e.پیغام = str(e)
        # urdu:78
        print(f"سوال خطا: {e}")
        # urdu:79
        return []

# urdu:83

def چلائیں(sql, params):
    # urdu:84
    try:
        # urdu:85
        cur = ڈی_بی.cursor()
        # urdu:86
        cur.execute(sql, (params or []))
        # urdu:87
        ڈی_بی.commit()
        # urdu:88
        lid = cur.lastrowid
        # urdu:89
        cur.close()
        # urdu:90
        return lid
    except Exception as e:
        if not hasattr(e, 'پیغام'): e.پیغام = str(e)
        # urdu:92
        print(f"چلائیں خطا: {e}")
        # urdu:93
        return None

# urdu:98
ونڈو = گوئی('بلنگ و انوینٹری — MySQL', 900, 620)
# urdu:99
ونڈو.مرکز()
# urdu:100
مرکزی = کنٹینر(ونڈو, پیڈنگ = 8)
# urdu:102
if (not جڑا):
    # urdu:103
    لیبل(مرکزی, 'MySQL کنکشن ناکام — localhost:3306 پر سرور چلائیں', کلاس = 'h3 text-danger fw-bold')
    # urdu:104
    ونڈو.چلائیں()
# urdu:107
لیبل(مرکزی, 'بلنگ و انوینٹری مینیجر — MySQL', کلاس = 'h2 text-primary fw-bold')
# urdu:109
ٹیبز = ٹیب_ویو(مرکزی)
# urdu:114
مصنوعات_ٹیب = ٹیبز.ٹیب('مصنوعات')
# urdu:115
مصنوعات_جدول = جدول(مصنوعات_ٹیب, ['ID', 'نام', 'قیمت (Rs)', 'مقدار'])
# urdu:117

def مصنوعات_لوڈ():
    # urdu:118
    مصنوعات_جدول.صاف_کریں()
    # urdu:119
    for ق in سوال('SELECT * FROM مصنوعات ORDER BY id', []):
        # urdu:120
        مصنوعات_جدول.شامل_کریں([ق['id'], ق['نام'], ق['قیمت'], ق['مقدار']])

# urdu:124
م_فریم = فریم(مصنوعات_ٹیب, عنوان = 'نئی مصنوع')
# urdu:125
م_ق = ردیف(م_فریم)
# urdu:126
م_ک1 = کالم(م_ق)
# urdu:126
لیبل(م_ک1, 'نام:')
# urdu:126
م_نام = ان_پٹ(م_ک1, placeholder = 'مصنوع کا نام')
# urdu:127
م_ک2 = کالم(م_ق)
# urdu:127
لیبل(م_ک2, 'قیمت:')
# urdu:127
م_قیمت = ان_پٹ(م_ک2, placeholder = '0.00')
# urdu:128
م_ک3 = کالم(م_ق)
# urdu:128
لیبل(م_ک3, 'مقدار:')
# urdu:128
م_مقدار = ان_پٹ(م_ک3, placeholder = '0')
# urdu:130

def مصنوع_شامل():
    # urdu:131
    ن = م_نام.حاصل_کریں().strip()
    # urdu:132
    if (لمبائی(ن) == 0):
        # urdu:132
        ڈائیلاگ.غلطی('نام ضروری ہے۔')
        # urdu:132
        return
    # urdu:133
    try:
        # urdu:134
        چلائیں('INSERT INTO مصنوعات (نام, قیمت, مقدار) VALUES (%s, %s, %s)', [ن, اعشاریہ((م_قیمت.حاصل_کریں() or '0')), عدد((م_مقدار.حاصل_کریں() or '0'))])
        # urdu:136
        م_نام.صاف_کریں()
        # urdu:136
        م_قیمت.صاف_کریں()
        # urdu:136
        م_مقدار.صاف_کریں()
        # urdu:137
        مصنوعات_لوڈ()
    except Exception as e:
        if not hasattr(e, 'پیغام'): e.پیغام = str(e)
        # urdu:138
        ڈائیلاگ.غلطی(f"خطا: {e}")

# urdu:141
م_ق2 = ردیف(م_فریم)
# urdu:142
بٹن(کالم(م_ق2), 'شامل کریں', کلاس = 'btn btn-success p-2', پر_کلک = مصنوع_شامل)
# urdu:143
بٹن(کالم(م_ق2), 'تازہ کریں', کلاس = 'btn btn-info p-2', پر_کلک = مصنوعات_لوڈ)
# urdu:148
گاہک_ٹیب = ٹیبز.ٹیب('گاہک')
# urdu:149
گاہک_جدول = جدول(گاہک_ٹیب, ['ID', 'نام', 'فون', 'پتہ'])
# urdu:151

def گاہک_لوڈ():
    # urdu:152
    گاہک_جدول.صاف_کریں()
    # urdu:153
    for ق in سوال('SELECT * FROM گاہک ORDER BY id', []):
        # urdu:154
        گاہک_جدول.شامل_کریں([ق['id'], ق['نام'], ق['فون'], ق['پتہ']])

# urdu:158
گ_فریم = فریم(گاہک_ٹیب, عنوان = 'نئے گاہک')
# urdu:159
گ_ق = ردیف(گ_فریم)
# urdu:160
گ_ک1 = کالم(گ_ق)
# urdu:160
لیبل(گ_ک1, 'نام:')
# urdu:160
گ_نام = ان_پٹ(گ_ک1, placeholder = 'نام')
# urdu:161
گ_ک2 = کالم(گ_ق)
# urdu:161
لیبل(گ_ک2, 'فون:')
# urdu:161
گ_فون = ان_پٹ(گ_ک2, placeholder = 'فون')
# urdu:162
گ_ک3 = کالم(گ_ق)
# urdu:162
لیبل(گ_ک3, 'پتہ:')
# urdu:162
گ_پتہ = ان_پٹ(گ_ک3, placeholder = 'پتہ')
# urdu:164

def گاہک_شامل():
    # urdu:165
    ن = گ_نام.حاصل_کریں().strip()
    # urdu:166
    if (لمبائی(ن) == 0):
        # urdu:166
        ڈائیلاگ.غلطی('نام ضروری ہے۔')
        # urdu:166
        return
    # urdu:167
    چلائیں('INSERT INTO گاہک (نام, فون, پتہ) VALUES (%s, %s, %s)', [ن, گ_فون.حاصل_کریں(), گ_پتہ.حاصل_کریں()])
    # urdu:169
    گ_نام.صاف_کریں()
    # urdu:169
    گ_فون.صاف_کریں()
    # urdu:169
    گ_پتہ.صاف_کریں()
    # urdu:170
    گاہک_لوڈ()

# urdu:173
گ_ق2 = ردیف(گ_فریم)
# urdu:174
بٹن(کالم(گ_ق2), 'شامل کریں', کلاس = 'btn btn-success p-2', پر_کلک = گاہک_شامل)
# urdu:175
بٹن(کالم(گ_ق2), 'تازہ کریں', کلاس = 'btn btn-info p-2', پر_کلک = گاہک_لوڈ)
# urdu:180
بل_ٹیب = ٹیبز.ٹیب('بل')
# urdu:181
بل_جدول = جدول(بل_ٹیب, ['ID', 'گاہک', 'تاریخ', 'کل (Rs)'])
# urdu:183

def بل_لوڈ():
    # urdu:184
    بل_جدول.صاف_کریں()
    # urdu:185
    for ق in سوال('SELECT ب.id, گ.نام, ب.تاریخ, ب.کل FROM بل ب JOIN گاہک گ ON گ.id=ب.گاہک_id ORDER BY ب.id DESC', []):
        # urdu:187
        بل_جدول.شامل_کریں([ق['id'], ق['نام'], ق['تاریخ'], ق['کل']])

# urdu:191
ب_فریم = فریم(بل_ٹیب, عنوان = 'نیا بل')
# urdu:192
ب_ق = ردیف(ب_فریم)
# urdu:193
ب_ک1 = کالم(ب_ق)
# urdu:193
لیبل(ب_ک1, 'گاہک ID:')
# urdu:193
ب_گاہک = ان_پٹ(ب_ک1, placeholder = 'ID')
# urdu:194
ب_ک2 = کالم(ب_ق)
# urdu:194
لیبل(ب_ک2, 'اشیاء (نام:مقدار:قیمت،...):')
# urdu:194
ب_اشیاء = ان_پٹ(ب_ک2, placeholder = 'دودھ:2:120،روٹی:5:20')
# urdu:196

def بل_بنائیں():
    # urdu:197
    try:
        # urdu:198
        گ_id = عدد(ب_گاہک.حاصل_کریں())
        # urdu:199
        اشیاء_متن = ب_اشیاء.حاصل_کریں().strip()
        # urdu:200
        کل = 0
        # urdu:201
        فہرست_اشیاء = []
        # urdu:202
        for شے in اشیاء_متن.split('،'):
            # urdu:203
            ح = شے.strip().split(':')
            # urdu:204
            if (لمبائی(ح) == 3):
                # urdu:205
                مق = عدد(ح[1])
                # urdu:205
                قیمت = اعشاریہ(ح[2])
                # urdu:206
                کل += (مق * قیمت)
                # urdu:207
                فہرست_اشیاء.append([ح[0].strip(), مق, قیمت])
        # urdu:210
        بل_id = چلائیں('INSERT INTO بل (گاہک_id, تاریخ, کل) VALUES (%s, %s, %s)', [گ_id, datetime.date.today().isoformat(), کل])
        # urdu:213
        for شے in فہرست_اشیاء:
            # urdu:214
            چلائیں('INSERT INTO بل_اشیاء (بل_id, مصنوع_نام, مقدار, قیمت) VALUES (%s, %s, %s, %s)', [بل_id, شے[0], شے[1], شے[2]])
        # urdu:217
        ڈائیلاگ.معلومات(f"بل بن گیا! کل: Rs {کل}", 'کامیاب')
        # urdu:218
        ب_گاہک.صاف_کریں()
        # urdu:218
        ب_اشیاء.صاف_کریں()
        # urdu:219
        بل_لوڈ()
    except Exception as e:
        if not hasattr(e, 'پیغام'): e.پیغام = str(e)
        # urdu:220
        ڈائیلاگ.غلطی(f"خطا: {e}")

# urdu:223
ب_ق2 = ردیف(ب_فریم)
# urdu:224
بٹن(کالم(ب_ق2), 'بل بنائیں', کلاس = 'btn btn-success p-2', پر_کلک = بل_بنائیں)
# urdu:225
بٹن(کالم(ب_ق2), 'تازہ کریں', کلاس = 'btn btn-info p-2', پر_کلک = بل_لوڈ)
# urdu:227
مصنوعات_لوڈ()
# urdu:227
گاہک_لوڈ()
# urdu:227
بل_لوڈ()
# urdu:228
ونڈو.چلائیں()