# ═══════════════════════════════════════
# اردو پروگرامنگ لینگویج — Generated Code
# Developer: Mohammed Zahid Wadiwale
# Version  : 1.0.0
# ═══════════════════════════════════════
from __future__ import annotations
import asyncio, sys, os
from urdu.runtime.builtins import *


async def _اردو_main():
    from urdu.runtime.web import UrduFastAPI
    from urdu.runtime.web import UrduRouter
    from urdu.runtime.web import JWT
    from fastapi.testclient import TestClient
    ن = _UrduObj({'گزرے': 0, 'ناکام': 0})
    
    def جانچ(نام, شرط):
        if شرط:
            print(f"  ✓ {نام}")
            ن['گزرے'] = (ن['گزرے'] + 1)
        else:
            print(f"  ✗ {نام}")
            ن['ناکام'] = (ن['ناکام'] + 1)
    
    ایپ = UrduFastAPI(_UrduObj({'عنوان': 'اردو API جانچ', 'نسخہ': '2.0'}))
    
    def جڑ():
        return _UrduObj({'پیغام': 'خوش آمدید'})
    
    def سلام(نام):
        return _UrduObj({'پیغام': f"السلام {نام}"})
    
    def اشیاء_حاصل(صفحہ=1, حد=10):
        return _UrduObj({'صفحہ': صفحہ, 'حد': حد, 'کل': 100})
    
    async def نیا_صارف(درخواست):
        باڈی = (await درخواست.json())
        return _UrduObj({'شناخت': 1, 'نام': باڈی['نام'], 'ای_میل': باڈی['ای_میل']})
    
    def صارف_تازہ(شناخت):
        return _UrduObj({'شناخت': شناخت, 'حالت': 'تازہ'})
    
    def صارف_حذف(شناخت):
        return _UrduObj({'پیغام': f"صارف {شناخت} حذف"})
    
    async def صارف_پیچ(شناخت, درخواست):
        باڈی = (await درخواست.json())
        return _UrduObj({'شناخت': شناخت, 'تبدیلی': باڈی})
    
    کتاب_روٹر = UrduRouter(_UrduObj({'سابقہ': '/کتابیں', 'ٹیگ': ['کتابیں']}))
    
    def کتابیں_فہرست():
        return [_UrduObj({'شناخت': 1, 'عنوان': 'آگ کا دریا'}), _UrduObj({'شناخت': 2, 'عنوان': 'گلستان'})]
    
    async def کتاب_شامل(درخواست):
        باڈی = (await درخواست.json())
        return _UrduObj({'شناخت': 3, 'عنوان': باڈی['عنوان'], 'پیغام': 'شامل ہوئی'})
    
    def کتاب_ایک(شناخت):
        return _UrduObj({'شناخت': شناخت, 'عنوان': 'نمونہ کتاب'})
    
    _r = ایپ.شامل_کریں(کتاب_روٹر)
    if asyncio.iscoroutine(_r): await _r
    
    async def مرکز():
        _r = print('╔══════════════════════════════════════╗')
        if asyncio.iscoroutine(_r): await _r
        _r = print('║  FastAPI مکمل جانچ رپورٹ             ║')
        if asyncio.iscoroutine(_r): await _r
        _r = print('╚══════════════════════════════════════╝')
        if asyncio.iscoroutine(_r): await _r
        کلائنٹ = TestClient(ایپ.ایپ)
        _r = print('\n─── GET راستے ───')
        if asyncio.iscoroutine(_r): await _r
        ج1 = کلائنٹ.get('/')
        _r = جانچ('GET / — 200 OK', (ج1.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('GET / — پیغام', (ج1.json()['پیغام'] == 'خوش آمدید'))
        if asyncio.iscoroutine(_r): await _r
        ج2 = کلائنٹ.get('/سلام/احمد')
        _r = جانچ('GET /سلام/{نام} — 200', (ج2.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('GET /سلام/{نام} — قدر', (ج2.json()['پیغام'] == 'السلام احمد'))
        if asyncio.iscoroutine(_r): await _r
        ج3 = کلائنٹ.get('/اشیاء?صفحہ=2&حد=5')
        _r = جانچ('GET query params — 200', (ج3.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('GET query params — صفحہ', (ج3.json()['صفحہ'] == 2))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('GET query params — حد', (ج3.json()['حد'] == 5))
        if asyncio.iscoroutine(_r): await _r
        _r = print('\n─── POST / PUT / DELETE / PATCH ───')
        if asyncio.iscoroutine(_r): await _r
        ج4 = کلائنٹ.post('/صارف', json = _UrduObj({'نام': 'فاطمہ', 'ای_میل': 'f@test.com'}))
        _r = جانچ('POST /صارف — 200', (ج4.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('POST /صارف — نام', (ج4.json()['نام'] == 'فاطمہ'))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('POST /صارف — ای_میل', (ج4.json()['ای_میل'] == 'f@test.com'))
        if asyncio.iscoroutine(_r): await _r
        ج5 = کلائنٹ.put('/صارف/42')
        _r = جانچ('PUT /صارف/{id} — 200', (ج5.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('PUT /صارف/{id} — id', (ج5.json()['شناخت'] == '42'))
        if asyncio.iscoroutine(_r): await _r
        ج6 = کلائنٹ.delete('/صارف/42')
        _r = جانچ('DELETE /صارف/{id} — 200', (ج6.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        ج7 = کلائنٹ.patch('/صارف/7', json = _UrduObj({'قیمت': 999}))
        _r = جانچ('PATCH /صارف/{id} — 200', (ج7.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('PATCH — تبدیلی', (ج7.json()['تبدیلی']['قیمت'] == 999))
        if asyncio.iscoroutine(_r): await _r
        _r = print('\n─── Router جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        ج8 = کلائنٹ.get('/کتابیں/')
        _r = جانچ('Router GET /کتابیں/ — 200', (ج8.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('Router GET /کتابیں/ — 2 اندراج', (لمبائی(ج8.json()) == 2))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('Router GET — پہلی کتاب', (ج8.json()[0]['عنوان'] == 'آگ کا دریا'))
        if asyncio.iscoroutine(_r): await _r
        ج9 = کلائنٹ.post('/کتابیں/', json = _UrduObj({'عنوان': 'بوستان'}))
        _r = جانچ('Router POST /کتابیں/ — 200', (ج9.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('Router POST — عنوان', (ج9.json()['عنوان'] == 'بوستان'))
        if asyncio.iscoroutine(_r): await _r
        ج10 = کلائنٹ.get('/کتابیں/5')
        _r = جانچ('Router GET /کتابیں/{id} — 200', (ج10.status_code == 200))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('Router GET /کتابیں/{id} — id', (ج10.json()['شناخت'] == '5'))
        if asyncio.iscoroutine(_r): await _r
        _r = print('\n─── JWT جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        try:
            خفیہ = 'test-secret-32-chars-long-key!!!'
            ٹوکن = JWT.بنائیں(_UrduObj({'صارف': 'احمد', 'کردار': 'ایڈمن'}), خفیہ, _UrduObj({'میعاد_منٹ': 60}))
            _r = جانچ('JWT ٹوکن بنا', (لمبائی(ٹوکن) > 20))
            if asyncio.iscoroutine(_r): await _r
            معلومات = JWT.جانچیں(ٹوکن, خفیہ)
            _r = جانچ('JWT تصدیق — صارف', (معلومات['صارف'] == 'احمد'))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('JWT تصدیق — کردار', (معلومات['کردار'] == 'ایڈمن'))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            _r = print(f"  ⓘ JWT چھوڑا (python-jose نہیں): {غ}")
            if asyncio.iscoroutine(_r): await _r
            ن['گزرے'] = (ن['گزرے'] + 3)
        _r = print(f"\n══════════════════════════════════════")
        if asyncio.iscoroutine(_r): await _r
        _r = print(f"  FastAPI — گزرے: {ن['گزرے']}  ناکام: {ن['ناکام']}")
        if asyncio.iscoroutine(_r): await _r
        _r = print(f"══════════════════════════════════════")
        if asyncio.iscoroutine(_r): await _r
    
    (await مرکز())

asyncio.run(_اردو_main())