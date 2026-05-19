# ═══════════════════════════════════════
# اردو پروگرامنگ لینگویج — Generated Code
# Developer: Mohammed Zahid Wadiwale
# Version  : 1.0.0
# ═══════════════════════════════════════
from __future__ import annotations
import asyncio, sys, os
from urdu.runtime.builtins import *

# urdu:6
from urdu.runtime.gui import گوئی
from urdu.runtime.gui import کنٹینر
from urdu.runtime.gui import ردیف
from urdu.runtime.gui import کالم
from urdu.runtime.gui import فریم
from urdu.runtime.gui import لیبل
from urdu.runtime.gui import بٹن
from urdu.runtime.gui import ان_پٹ
from urdu.runtime.gui import ٹیکسٹ_ایریا
from urdu.runtime.gui import ڈراپ_ڈاؤن
from urdu.runtime.gui import چیک_بکس
from urdu.runtime.gui import پروگریس_بار
from urdu.runtime.gui import الرٹ
from urdu.runtime.gui import ٹیب_ویو
from urdu.runtime.gui import ڈائیلاگ
from urdu.runtime.gui import جدول
# urdu:14
ایپ = گوئی('اردو ٹاسک مینیجر', 900, 650)
# urdu:17
nav = فریم(ایپ, کلاس = '')
# urdu:21
ٹیبس = ٹیب_ویو(ایپ)
# urdu:24
ٹیب1 = ٹیبس.ٹیب('طالب علم رجسٹریشن')
# urdu:26
عنوان = لیبل(ٹیب1, 'طالب علم رجسٹریشن فارم', کلاس = 'h3 text-primary fw-bold')
# urdu:29
ردیف1 = ردیف(ٹیب1)
# urdu:30
کل1 = کالم(ردیف1, 'col-6')
# urdu:31
کل2 = کالم(ردیف1, 'col-6')
# urdu:33
لیبل(کل1, 'نام:')
# urdu:34
نام_ان_پٹ = ان_پٹ(کل1, placeholder = 'پورا نام لکھیں', کلاس = 'form-control')
# urdu:37
لیبل(کل2, 'عمر:')
# urdu:38
عمر_ان_پٹ = ان_پٹ(کل2, placeholder = 'عمر', کلاس = 'form-control')
# urdu:41
ردیف2 = ردیف(ٹیب1)
# urdu:42
کل3 = کالم(ردیف2, 'col-6')
# urdu:43
کل4 = کالم(ردیف2, 'col-6')
# urdu:45
لیبل(کل3, 'درجہ:')
# urdu:46
درجہ_ڈراپ = ڈراپ_ڈاؤن(کل3, ['پہلا', 'دوسرا', 'تیسرا', 'چوتھا', 'پانچواں'], کلاس = 'form-select')
# urdu:50
لیبل(کل4, 'جنس:')
# urdu:51
جنس_ڈراپ = ڈراپ_ڈاؤن(کل4, ['مرد', 'عورت', 'دیگر'], کلاس = 'form-select')
# urdu:56
بٹن_ردیف = ردیف(ٹیب1)
# urdu:57
بٹن_کل = کالم(بٹن_ردیف)
# urdu:59

def رجسٹر_کریں():
    # urdu:60
    ن = نام_ان_پٹ.حاصل_کریں()
    # urdu:61
    ع = عمر_ان_پٹ.حاصل_کریں()
    # urdu:62
    د = درجہ_ڈراپ.حاصل_کریں()
    # urdu:64
    if ((not ن) or (not ع)):
        # urdu:65
        ڈائیلاگ.تنبیہ('برائے کرم تمام خانے بھریں')
        # urdu:66
        return
    # urdu:69
    جدول_ڈیٹا.شامل_کریں([ن, ع, د])
    # urdu:70
    نام_ان_پٹ.صاف_کریں()
    # urdu:71
    عمر_ان_پٹ.صاف_کریں()
    # urdu:72
    print(f"رجسٹریشن: {ن}, عمر: {ع}, درجہ: {د}")

# urdu:75
بٹن(بٹن_کل, 'رجسٹر کریں', کلاس = 'btn btn-success', پر_کلک = رجسٹر_کریں)
# urdu:79
def _fn_0():
    # urdu:82
    نام_ان_پٹ.صاف_کریں()
    # urdu:83
    عمر_ان_پٹ.صاف_کریں()

بٹن(بٹن_کل, 'صاف کریں', کلاس = 'btn btn-secondary', پر_کلک = _fn_0)
# urdu:87
لیبل(ٹیب1, '\nرجسٹرڈ طلبہ:', کلاس = 'fw-bold')
# urdu:88
جدول_ڈیٹا = جدول(ٹیب1, ['نام', 'عمر', 'درجہ'], کلاس = 'table')
# urdu:93
ٹیب2 = ٹیبس.ٹیب('کیلکولیٹر')
# urdu:95
لیبل(ٹیب2, 'سادہ کیلکولیٹر', کلاس = 'h3 text-info fw-bold')
# urdu:97
calc_ردیف = ردیف(ٹیب2)
# urdu:98
calc_کل1 = کالم(calc_ردیف, 'col-4')
# urdu:99
calc_کل2 = کالم(calc_ردیف, 'col-4')
# urdu:100
calc_کل3 = کالم(calc_ردیف, 'col-4')
# urdu:102
لیبل(calc_کل1, 'پہلا عدد:')
# urdu:103
پہلا_ان_پٹ = ان_پٹ(calc_کل1, placeholder = '0', کلاس = 'form-control')
# urdu:105
لیبل(calc_کل2, 'دوسرا عدد:')
# urdu:106
دوسرا_ان_پٹ = ان_پٹ(calc_کل2, placeholder = '0', کلاس = 'form-control')
# urdu:108
لیبل(calc_کل3, 'نتیجہ:')
# urdu:109
نتیجہ_لیبل = لیبل(calc_کل3, '0', کلاس = 'h4 text-success')
# urdu:111
calc_بٹن_ردیف = ردیف(ٹیب2)
# urdu:112
calc_بٹن_کل = کالم(calc_بٹن_ردیف)
# urdu:114

def حساب_کرو(آپریشن):
    # urdu:115
    try:
        # urdu:116
        الف = اعشاریہ(پہلا_ان_پٹ.حاصل_کریں())
        # urdu:117
        ب = اعشاریہ(دوسرا_ان_پٹ.حاصل_کریں())
        # urdu:118
        نتیجہ = None
        # urdu:120
        if (آپریشن == '+'):
            # urdu:120
            نتیجہ = (الف + ب)
        elif (آپریشن == '-'):
            # urdu:121
            نتیجہ = (الف - ب)
        elif (آپریشن == '*'):
            # urdu:122
            نتیجہ = (الف * ب)
        elif (آپریشن == '/'):
            # urdu:124
            if (ب == 0):
                # urdu:124
                raise غلطی('صفر سے تقسیم ممکن نہیں')
            # urdu:125
            نتیجہ = (الف / ب)
        # urdu:128
        نتیجہ_لیبل.متن(گول(نتیجہ, 4))
    except Exception as غ:
        if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
        # urdu:130
        ڈائیلاگ.غلطی(غ.پیغام)

# urdu:134
def _fn_1():
    # urdu:134
    حساب_کرو('+')

بٹن(calc_بٹن_کل, '+ جمع', کلاس = 'btn btn-primary', پر_کلک = _fn_1)
# urdu:135
def _fn_2():
    # urdu:135
    حساب_کرو('-')

بٹن(calc_بٹن_کل, '- تفریق', کلاس = 'btn btn-warning', پر_کلک = _fn_2)
# urdu:136
def _fn_3():
    # urdu:136
    حساب_کرو('*')

بٹن(calc_بٹن_کل, '× ضرب', کلاس = 'btn btn-success', پر_کلک = _fn_3)
# urdu:137
def _fn_4():
    # urdu:137
    حساب_کرو('/')

بٹن(calc_بٹن_کل, '÷ تقسیم', کلاس = 'btn btn-danger', پر_کلک = _fn_4)
# urdu:140
ایپ.مرکز()
# urdu:141
ایپ.چلائیں()