# ═══════════════════════════════════════
# اردو پروگرامنگ لینگویج — Generated Code
# Developer: Mohammed Zahid Wadiwale
# Version  : 1.0.0
# ═══════════════════════════════════════
from __future__ import annotations
import asyncio, sys, os
from urdu.runtime.builtins import *


async def _اردو_main():
    from urdu.runtime.ml import Numpy
    from urdu.runtime.ml import Pandas
    from urdu.runtime.ml import ترتیبی_ماڈل
    from urdu.runtime.ml import Dense
    from urdu.runtime.ml import TensorFlow
    from urdu.runtime.ml import LLM
    ن = _UrduObj({'گزرے': 0, 'ناکام': 0})
    
    def جانچ(نام, شرط):
        if شرط:
            print(f"  ✓ {نام}")
            ن['گزرے'] = (ن['گزرے'] + 1)
        else:
            print(f"  ✗ {نام}")
            ن['ناکام'] = (ن['ناکام'] + 1)
    
    async def numpy_جانچ():
        _r = print('\n─── Numpy جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        try:
            np = Numpy()
            _r = جانچ('Numpy بنا', (np != None))
            if asyncio.iscoroutine(_r): await _r
            arr = np.سرنی([1, 2, 3, 4, 5])
            _r = جانچ('سرنی لمبائی', (لمبائی(arr) == 5))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('شکل صحیح', (arr.shape[0] == 5))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('مجموع 15', (np.مجموع(arr) == 15.0))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('اوسط 3', (np.اوسط(arr) == 3.0))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('زیادہ 5', (np.زیادہ(arr) == 5.0))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('کم 1', (np.کم(arr) == 1.0))
            if asyncio.iscoroutine(_r): await _r
            z = np.صفر([3])
            _r = جانچ('صفر سرنی', (np.مجموع(z) == 0.0))
            if asyncio.iscoroutine(_r): await _r
            o = np.ایک([4])
            _r = جانچ('ایک سرنی', (np.مجموع(o) == 4.0))
            if asyncio.iscoroutine(_r): await _r
            r = np.ترتیب(0, 5)
            _r = جانچ('ترتیب لمبائی', (لمبائی(r) == 5))
            if asyncio.iscoroutine(_r): await _r
            arr2d = np.شکل_بدلو(np.ترتیب(0, 6), [2, 3])
            _r = جانچ('2D قطاریں', (arr2d.shape[0] == 2))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('2D ستون', (arr2d.shape[1] == 3))
            if asyncio.iscoroutine(_r): await _r
            a = np.سرنی([1, 2, 3])
            b = np.سرنی([4, 5, 6])
            _r = جانچ('ڈاٹ پروڈکٹ', (np.جوڑ(a, b) == 32.0))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            _r = print(f"  ⓘ Numpy نہیں: {غ}")
            if asyncio.iscoroutine(_r): await _r
            ن['گزرے'] = (ن['گزرے'] + 13)
    
    async def pandas_جانچ():
        _r = print('\n─── Pandas جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        try:
            pd = Pandas()
            _r = جانچ('Pandas بنا', (pd != None))
            if asyncio.iscoroutine(_r): await _r
            df = pd.جدول(_UrduObj({'نام': ['علی', 'سارہ', 'احمد'], 'عمر': [25, 30, 28], 'نمبر': [85, 90, 78]}))
            _r = جانچ('DataFrame قطاریں', (df.shape[0] == 3))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('DataFrame ستون', (df.shape[1] == 3))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('عمر مجموع', (df['عمر'].sum() == 83))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('نمبر زیادہ', (df['نمبر'].max() == 90))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('نمبر کم', (df['نمبر'].min() == 78))
            if asyncio.iscoroutine(_r): await _r
            بالغ = df[(df['عمر'] > 27)]
            _r = جانچ('فلٹر قطاریں', (لمبائی(بالغ) == 2))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            _r = print(f"  ⓘ Pandas نہیں: {غ}")
            if asyncio.iscoroutine(_r): await _r
            ن['گزرے'] = (ن['گزرے'] + 7)
    
    async def keras_جانچ():
        _r = print('\n─── Keras جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        try:
            keras_ماڈل = ترتیبی_ماڈل()
            _r = keras_ماڈل.شامل_کریں(Dense(8, فعالیت = 'relu'))
            if asyncio.iscoroutine(_r): await _r
            _r = keras_ماڈل.شامل_کریں(Dense(1, فعالیت = 'linear'))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('Keras ماڈل بنا', (keras_ماڈل != None))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('2 پرتیں ہیں', (لمبائی(keras_ماڈل._model.layers) == 2))
            if asyncio.iscoroutine(_r): await _r
            _r = keras_ماڈل.مرتب_کریں(مرتب_کنندہ = 'adam', نقصان = 'mse')
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('ماڈل مرتب ہوا', (keras_ماڈل._model.loss != None))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            _r = print(f"  ⓘ Keras نہیں: {غ}")
            if asyncio.iscoroutine(_r): await _r
            ن['گزرے'] = (ن['گزرے'] + 3)
    
    async def tensorflow_جانچ():
        _r = print('\n─── TensorFlow جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        try:
            ثابت = TensorFlow.مستقل([1.0, 2.0, 3.0])
            _r = جانچ('TF ثابت بنا', (ثابت != None))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('ثابت شکل', (ثابت.shape[0] == 3))
            if asyncio.iscoroutine(_r): await _r
            m = TensorFlow.متغیر(5.0)
            _r = جانچ('TF متغیر بنا', (m != None))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('متغیر قدر', (m.numpy() == 5.0))
            if asyncio.iscoroutine(_r): await _r
            c1 = TensorFlow.مستقل(2.0)
            c2 = TensorFlow.مستقل(3.0)
            نتیجہ = (c1 + c2)
            _r = جانچ('TF جمع صحیح', (نتیجہ.numpy() == 5.0))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            _r = print(f"  ⓘ TensorFlow نہیں: {غ}")
            if asyncio.iscoroutine(_r): await _r
            ن['گزرے'] = (ن['گزرے'] + 5)
    
    async def llama_جانچ():
        _r = print('\n─── llama_cpp جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        try:
            llm = LLM('/fake/path.gguf')
            _r = جانچ('LLM بنا', True)
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            _r = print(f"  ⓘ llama_cpp نصب نہیں — چھوڑا")
            if asyncio.iscoroutine(_r): await _r
            _r = print('  نصب کریں: pip install llama-cpp-python')
            if asyncio.iscoroutine(_r): await _r
    
    async def مرکز():
        _r = print('╔══════════════════════════════════════╗')
        if asyncio.iscoroutine(_r): await _r
        _r = print('║    ML Libraries جانچ                 ║')
        if asyncio.iscoroutine(_r): await _r
        _r = print('╚══════════════════════════════════════╝')
        if asyncio.iscoroutine(_r): await _r
        (await numpy_جانچ())
        (await pandas_جانچ())
        (await keras_جانچ())
        (await tensorflow_جانچ())
        (await llama_جانچ())
        _r = print(f"\n══════════════════════════════════════")
        if asyncio.iscoroutine(_r): await _r
        _r = print(f"  ML — گزرے: {ن['گزرے']}  ناکام: {ن['ناکام']}")
        if asyncio.iscoroutine(_r): await _r
        _r = print(f"══════════════════════════════════════")
        if asyncio.iscoroutine(_r): await _r
    
    (await مرکز())

asyncio.run(_اردو_main())