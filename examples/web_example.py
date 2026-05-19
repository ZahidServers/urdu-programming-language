# ═══════════════════════════════════════
# اردو پروگرامنگ لینگویج — Generated Code
# Developer: Mohammed Zahid Wadiwale
# Version  : 1.0.0
# ═══════════════════════════════════════
from __future__ import annotations
import asyncio, sys, os
from urdu.runtime.builtins import *


async def _اردو_main():
    # urdu:7
    from urdu.runtime.web import UrduFastAPI
    from urdu.runtime.web import JSONResponse
    # urdu:9
    ایپ = UrduFastAPI(عنوان = 'اردو طلبہ API', نسخہ = '1.0.0', تفصیل = 'اردو پروگرامنگ لینگویج سے بنی API')
    # urdu:16
    طلبہ = [_UrduObj({'شناخت': 1, 'نام': 'احمد علی', 'درجہ': 'دسواں', 'نمبر': 92}), _UrduObj({'شناخت': 2, 'نام': 'فاطمہ خان', 'درجہ': 'گیارہویں', 'نمبر': 88}), _UrduObj({'شناخت': 3, 'نام': 'محمد عمر', 'درجہ': 'نواں', 'نمبر': 95})]
    # urdu:23
    async def صفحہ_اول():
        # urdu:25
        return _UrduObj({'پیغام': 'السلام علیکم! اردو API میں خوش آمدید', 'نسخہ': '1.0.0', 'ڈویلپر': 'Mohammed Zahid Wadiwale'})
    
    ایپ.حاصل('/')(صفحہ_اول)
    # urdu:34
    async def سبھی_طلبہ():
        # urdu:36
        return _UrduObj({'گنتی': لمبائی(طلبہ), 'طلبہ': طلبہ})
    
    ایپ.حاصل('/طلبہ')(سبھی_طلبہ)
    # urdu:41
    async def ایک_طالب(شناخت):
        # urdu:43
        def _fn_3(ط):
            # urdu:43
            return (ط.شناخت == عدد(شناخت))
        
        نتیجہ = next((_x for _x in طلبہ if _fn_3(_x)), None)
        # urdu:44
        if (not نتیجہ):
            # urdu:45
            return JSONResponse(_UrduObj({'غلطی': 'طالب علم نہیں ملا'}), 404)
        # urdu:47
        return نتیجہ
    
    ایپ.حاصل('/طالب/{شناخت}')(ایک_طالب)
    # urdu:52
    async def اوسط_نمبر():
        # urdu:54
        def _fn_5(ط):
            # urdu:54
            return ط.نمبر
        
        کل = مجموع(نقشہ(_fn_5, طلبہ))
        # urdu:55
        return _UrduObj({'اوسط': گول((کل / لمبائی(طلبہ)), 2)})
    
    ایپ.حاصل('/نمبر/اوسط')(اوسط_نمبر)
    # urdu:60
    async def طالب_شامل(درخواست):
        # urdu:62
        ڈیٹا = (await درخواست.json())
        # urdu:63
        نیا_طالب = _UrduObj({'شناخت': (لمبائی(طلبہ) + 1), 'نام': (ڈیٹا.نام or 'نامعلوم'), 'درجہ': (ڈیٹا.درجہ or 'نامعلوم'), 'نمبر': (ڈیٹا.نمبر or 0)})
        # urdu:69
        _r = طلبہ.append(نیا_طالب)
        if asyncio.iscoroutine(_r): await _r
        # urdu:70
        return _UrduObj({'پیغام': 'طالب علم شامل ہوا', 'طالب': نیا_طالب})
    
    ایپ.بھیجیں('/طالب/شامل')(طالب_شامل)
    # urdu:75
    async def طالب_حذف(شناخت):
        # urdu:77
        def _fn_8(ط):
            # urdu:77
            return (ط.شناخت == عدد(شناخت))
        
        اشاریہ = next((_i for _i, _x in enumerate(طلبہ) if _fn_8(_x)), -1)
        # urdu:78
        if (اشاریہ == (-1)):
            # urdu:79
            return JSONResponse(_UrduObj({'غلطی': 'نہیں ملا'}), 404)
        # urdu:81
        _r = _urdu_splice(طلبہ, اشاریہ, 1)
        if asyncio.iscoroutine(_r): await _r
        # urdu:82
        return _UrduObj({'پیغام': 'حذف ہوگیا'})
    
    _r = ایپ.حذف('/طالب/{شناخت}')(طالب_حذف)
    if asyncio.iscoroutine(_r): await _r
    # urdu:87
    _r = print('اردو FastAPI سرور شروع ہو رہا ہے...')
    if asyncio.iscoroutine(_r): await _r
    # urdu:88
    _r = print('براؤزر میں کھولیں: http://localhost:8000')
    if asyncio.iscoroutine(_r): await _r
    # urdu:89
    _r = print('API دستاویز: http://localhost:8000/docs')
    if asyncio.iscoroutine(_r): await _r
    # urdu:90
    _r = ایپ.چلائیں(میزبان = '0.0.0.0', پورٹ = 8000, دوبارہ_لوڈ = True)
    if asyncio.iscoroutine(_r): await _r

asyncio.run(_اردو_main())