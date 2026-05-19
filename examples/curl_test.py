# ═══════════════════════════════════════
# اردو پروگرامنگ لینگویج — Generated Code
# Developer: Mohammed Zahid Wadiwale
# Version  : 1.0.0
# ═══════════════════════════════════════
from __future__ import annotations
import asyncio, sys, os
from urdu.runtime.builtins import *


async def _اردو_main():
    # urdu:5
    from urdu.runtime.curl import کرل
    from urdu.runtime.curl import پائی_کرل
    from urdu.runtime.curl import کرل_حاصل
    from urdu.runtime.curl import بھیجو_کرو
    from urdu.runtime.curl import تازہ_کرو
    from urdu.runtime.curl import جزوی_تازہ_کرو
    from urdu.runtime.curl import مٹاؤ_کرو
    # urdu:7
    ن = _UrduObj({'گزرے': 0, 'ناکام': 0})
    # urdu:9
    
    def جانچ(نام, شرط):
        # urdu:10
        if شرط:
            # urdu:11
            print(f"  ✓ {نام}")
            # urdu:12
            ن['گزرے'] = (ن['گزرے'] + 1)
        else:
            # urdu:14
            print(f"  ✗ {نام}")
            # urdu:15
            ن['ناکام'] = (ن['ناکام'] + 1)
    
    # urdu:19
    API = 'https://jsonplaceholder.typicode.com'
    # urdu:20
    BIN = 'https://httpbin.org'
    # urdu:22
    
    async def مرکز():
        # urdu:23
        _r = print('╔══════════════════════════════════════════╗')
        if asyncio.iscoroutine(_r): await _r
        # urdu:24
        _r = print('║  کرل مکمل جانچ                           ║')
        if asyncio.iscoroutine(_r): await _r
        # urdu:25
        _r = print('╚══════════════════════════════════════════╝')
        if asyncio.iscoroutine(_r): await _r
        # urdu:28
        _r = print('\n─── GET ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:29
        try:
            # urdu:30
            جواب = (await کرل_حاصل(f"{API}/posts/1"))
            # urdu:31
            _r = جانچ('GET حالت 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:32
            _r = جانچ('GET ٹھیک', (جواب.ٹھیک == True))
            if asyncio.iscoroutine(_r): await _r
            # urdu:33
            ڈیٹا = جواب.json()
            # urdu:34
            _r = جانچ('GET id درست', (ڈیٹا['id'] == 1))
            if asyncio.iscoroutine(_r): await _r
            # urdu:35
            _r = جانچ('GET body موجود', (لمبائی(ڈیٹا['body']) > 0))
            if asyncio.iscoroutine(_r): await _r
            # urdu:36
            _r = print(f"  ⓘ عنوان: {ڈیٹا['title'][0:40]}")
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:38
            _r = print(f"  ✗ GET غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:39
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:43
        _r = print('\n─── GET + پیرامیٹر ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:44
        try:
            # urdu:45
            جواب = (await کرل_حاصل(f"{API}/posts", _UrduObj({'userId': 1, '_limit': 3})))
            # urdu:46
            _r = جانچ('پیرامیٹر GET 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:47
            فہرست = جواب.json()
            # urdu:48
            _r = جانچ('3 نتائج ملے', (لمبائی(فہرست) == 3))
            if asyncio.iscoroutine(_r): await _r
            # urdu:49
            _r = جانچ('پہلا userId=1', (فہرست[0]['userId'] == 1))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:51
            _r = print(f"  ✗ پیرامیٹر غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:52
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:56
        _r = print('\n─── POST ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:57
        try:
            # urdu:58
            جواب = (await بھیجو_کرو(f"{API}/posts", _UrduObj({'title': 'اردو HTTP جانچ', 'body': 'یہ اردو پروگرامنگ زبان سے POST ہے', 'userId': 1})))
            # urdu:63
            _r = جانچ('POST حالت 201', (جواب.حالت == 201))
            if asyncio.iscoroutine(_r): await _r
            # urdu:64
            نیا = جواب.json()
            # urdu:65
            _r = جانچ('POST id ملا', (['id']() > 0))
            if asyncio.iscoroutine(_r): await _r
            # urdu:66
            _r = جانچ('POST title واپس', (['title']() == 'اردو HTTP جانچ'))
            if asyncio.iscoroutine(_r): await _r
            # urdu:67
            _r = print(f"  ⓘ نیا ID: {['id']()}")
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:69
            _r = print(f"  ✗ POST غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:70
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:74
        _r = print('\n─── PUT ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:75
        try:
            # urdu:76
            جواب = (await تازہ_کرو(f"{API}/posts/1", _UrduObj({'id': 1, 'title': 'تازہ عنوان', 'body': 'تازہ مواد', 'userId': 1})))
            # urdu:82
            _r = جانچ('PUT حالت 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:83
            تازہ = جواب.json()
            # urdu:84
            _r = جانچ('PUT title تازہ', (تازہ['title'] == 'تازہ عنوان'))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:86
            _r = print(f"  ✗ PUT غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:87
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:91
        _r = print('\n─── PATCH ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:92
        try:
            # urdu:93
            جواب = (await جزوی_تازہ_کرو(f"{API}/posts/1", _UrduObj({'title': 'جزوی تازہ عنوان'})))
            # urdu:96
            _r = جانچ('PATCH حالت 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:97
            پیچ = جواب.json()
            # urdu:98
            _r = جانچ('PATCH title بدلا', (پیچ['title'] == 'جزوی تازہ عنوان'))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:100
            _r = print(f"  ✗ PATCH غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:101
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:105
        _r = print('\n─── DELETE ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:106
        try:
            # urdu:107
            جواب = (await مٹاؤ_کرو(f"{API}/posts/1"))
            # urdu:108
            _r = جانچ('DELETE حالت 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:109
            _r = جانچ('DELETE ٹھیک', (جواب.ٹھیک == True))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:111
            _r = print(f"  ✗ DELETE غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:112
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:116
        _r = print('\n─── کرل کلاس + سرخط ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:117
        try:
            # urdu:118
            c = کرل(_UrduObj({'سرخط': _UrduObj({'User-Agent': 'اردو-زبان/1.0', 'Accept': 'application/json', 'X-Custom': 'urdu-test'}), 'ختمی': 15}))
            # urdu:126
            جواب = (await c.حاصل(f"{BIN}/headers"))
            # urdu:127
            _r = جانچ('custom headers 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:128
            ڈیٹا = جواب.json()
            # urdu:129
            _r = جانچ('User-Agent پہنچا', (ڈیٹا['headers']['User-Agent'] == 'اردو-زبان/1.0'))
            if asyncio.iscoroutine(_r): await _r
            # urdu:130
            _r = جانچ('X-Custom پہنچا', (ڈیٹا['headers']['X-Custom'] == 'urdu-test'))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:132
            _r = print(f"  ✗ headers غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:133
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:137
        _r = print('\n─── Bearer Token ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:138
        try:
            # urdu:139
            c = کرل()
            # urdu:140
            _r = c.ٹوکن_مقرر('urdu-secret-token-12345')
            if asyncio.iscoroutine(_r): await _r
            # urdu:141
            جواب = (await c.حاصل(f"{BIN}/bearer"))
            # urdu:142
            _r = جانچ('Bearer 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:143
            ڈیٹا = جواب.json()
            # urdu:144
            _r = جانچ('authenticated سچ', (ڈیٹا['authenticated'] == True))
            if asyncio.iscoroutine(_r): await _r
            # urdu:145
            _r = جانچ('token درست', (ڈیٹا['token'] == 'urdu-secret-token-12345'))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:147
            _r = print(f"  ✗ Bearer غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:148
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:152
        _r = print('\n─── Basic Auth ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:153
        try:
            # urdu:154
            c = کرل()
            # urdu:155
            _r = c.بنیادی_توثیق('zahid', 'pass123')
            if asyncio.iscoroutine(_r): await _r
            # urdu:156
            جواب = (await c.حاصل(f"{BIN}/basic-auth/zahid/pass123"))
            # urdu:157
            _r = جانچ('Basic Auth 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:158
            ڈیٹا = جواب.json()
            # urdu:159
            _r = جانچ('authenticated سچ', (ڈیٹا['authenticated'] == True))
            if asyncio.iscoroutine(_r): await _r
            # urdu:160
            _r = جانچ('user درست', (ڈیٹا['user'] == 'zahid'))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:162
            _r = print(f"  ✗ Basic Auth غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:163
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:167
        _r = print('\n─── POST JSON echo ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:168
        try:
            # urdu:169
            c = کرل()
            # urdu:170
            جواب = (await c.بھیجو(f"{BIN}/post", _UrduObj({'نام': 'احمد', 'عمر': 25, 'شہر': 'کراچی'})))
            # urdu:175
            _r = جانچ('POST echo 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:176
            ڈیٹا = جواب.json()
            # urdu:177
            _r = جانچ('JSON نام پہنچا', (ڈیٹا['json']['نام'] == 'احمد'))
            if asyncio.iscoroutine(_r): await _r
            # urdu:178
            _r = جانچ('JSON عمر پہنچی', (ڈیٹا['json']['عمر'] == 25))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:180
            _r = print(f"  ✗ POST echo غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:181
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:185
        _r = print('\n─── حالت کوڈ ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:186
        try:
            # urdu:187
            r404 = (await کرل_حاصل(f"{BIN}/status/404"))
            # urdu:188
            _r = جانچ('404 حالت', (r404.حالت == 404))
            if asyncio.iscoroutine(_r): await _r
            # urdu:189
            _r = جانچ('404 ٹھیک نہیں', (r404.ٹھیک == False))
            if asyncio.iscoroutine(_r): await _r
            # urdu:191
            r201 = (await کرل_حاصل(f"{BIN}/status/201"))
            # urdu:192
            _r = جانچ('201 حالت', (r201.حالت == 201))
            if asyncio.iscoroutine(_r): await _r
            # urdu:193
            _r = جانچ('201 ٹھیک', (r201.ٹھیک == True))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:195
            _r = print(f"  ✗ حالت کوڈ غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:196
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:200
        _r = print('\n─── HEAD ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:201
        try:
            # urdu:202
            c = کرل()
            # urdu:203
            جواب = (await c.سر(f"{API}/posts/1"))
            # urdu:204
            _r = جانچ('HEAD 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:205
            _r = جانچ('HEAD متن خالی', (لمبائی(جواب.متن) == 0))
            if asyncio.iscoroutine(_r): await _r
            # urdu:206
            _r = جانچ('HEAD Content-Type موجود', ('Content-Type' in جواب.سرخط))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:208
            _r = print(f"  ✗ HEAD غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:209
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:213
        _r = print('\n─── base URL + زنجیر ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:214
        try:
            # urdu:215
            c = کرل(_UrduObj({'بنیادی_url': API}))
            # urdu:216
            جواب = (await c.حاصل('/users/1'))
            # urdu:217
            _r = جانچ('base URL GET 200', (جواب.حالت == 200))
            if asyncio.iscoroutine(_r): await _r
            # urdu:218
            صارف = جواب.json()
            # urdu:219
            _r = جانچ('user id=1', (صارف['id'] == 1))
            if asyncio.iscoroutine(_r): await _r
            # urdu:220
            _r = print(f"  ⓘ صارف: {صارف['name']}")
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:222
            _r = print(f"  ✗ base URL غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:223
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:227
        _r = print('\n─── pycurl ───')
        if asyncio.iscoroutine(_r): await _r
        # urdu:228
        try:
            # urdu:229
            _r = جانچ('pycurl دستیاب', (پائی_کرل.دستیاب() == True))
            if asyncio.iscoroutine(_r): await _r
            # urdu:230
            خام = (await پائی_کرل.حاصل(f"{API}/posts/1"))
            # urdu:231
            _r = جانچ('pycurl GET bytes', (لمبائی(خام) > 0))
            if asyncio.iscoroutine(_r): await _r
            # urdu:232
            _r = print(f"  ⓘ پہلے 50 bytes: {متن(خام)[0:50]}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:234
            خام_post = (await پائی_کرل.بھیجو(f"{BIN}/post", '{"پیغام": "pycurl سے"}', ['Content-Type: application/json']))
            # urdu:239
            _r = جانچ('pycurl POST bytes', (لمبائی(خام_post) > 0))
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            if not hasattr(غ, 'پیغام'): غ.پیغام = str(غ)
            # urdu:241
            _r = print(f"  ✗ pycurl غلطی: {غ}")
            if asyncio.iscoroutine(_r): await _r
            # urdu:242
            ن['ناکام'] = (ن['ناکام'] + 1)
        # urdu:245
        _r = print(f"\n══════════════════════════════════════════")
        if asyncio.iscoroutine(_r): await _r
        # urdu:246
        _r = print(f"  کرل جانچ — گزرے: {ن['گزرے']}  ناکام: {ن['ناکام']}")
        if asyncio.iscoroutine(_r): await _r
        # urdu:247
        _r = print(f"══════════════════════════════════════════")
        if asyncio.iscoroutine(_r): await _r
    
    # urdu:250
    (await مرکز())

asyncio.run(_اردو_main())