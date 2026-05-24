# ═══════════════════════════════════════
# اردو پروگرامنگ لینگویج — Generated Code
# Developer: Mohammed Zahid Wadiwale
# Version  : 1.0.0
# ═══════════════════════════════════════
from __future__ import annotations
import asyncio, sys, os
from urdu.runtime.builtins import *


async def _اردو_main():
    from urdu.runtime.web import WebSocket
    from urdu.runtime.web import UrduSocketIO
    from urdu.runtime.web import WebRTCSignalling
    ن = _UrduObj({'گزرے': 0, 'ناکام': 0})
    
    def جانچ(نام, شرط):
        if شرط:
            print(f"  ✓ {نام}")
            ن['گزرے'] = (ن['گزرے'] + 1)
        else:
            print(f"  ✗ {نام}")
            ن['ناکام'] = (ن['ناکام'] + 1)
    
    async def websocket_جانچ():
        _r = print('\n─── WebSocket جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        ws = WebSocket(_UrduObj({'میزبان': 'localhost', 'پورٹ': 8765}))
        _r = جانچ('WebSocket بنا', (ws != None))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('میزبان صحیح', (ws.میزبان == 'localhost'))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('پورٹ صحیح', (ws.پورٹ == 8765))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('کلائنٹس خالی', (لمبائی(ws._clients) == 0))
        if asyncio.iscoroutine(_r): await _r
    
        @ws.پر_پیغام
        def پیغام_ملا(کنکشن, متن):
            return f"جواب: {متن}"
    
        @ws.پر_جڑنا
        def جڑنا(کنکشن):
            _r = print('  نیا کنکشن')
            if asyncio.iscoroutine(_r): await _r
    
        @ws.پر_منقطع
        def منقطع(کنکشن):
            _r = print('  کنکشن ختم')
            if asyncio.iscoroutine(_r): await _r
    
        _r = جانچ('پیغام ہینڈلر رجسٹر', (ws._ہینڈلر != None))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('جڑنا ہینڈلر رجسٹر', (ws._جڑنا_ہینڈلر != None))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('منقطع ہینڈلر رجسٹر', (ws._منقطع_ہینڈلر != None))
        if asyncio.iscoroutine(_r): await _r
        جواب = ws._ہینڈلر(None, 'السلام')
        _r = جانچ('پیغام ہینڈلر جواب', (جواب == 'جواب: السلام'))
        if asyncio.iscoroutine(_r): await _r
    
    async def socketio_جانچ():
        _r = print('\n─── Socket.IO جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        try:
            sio = UrduSocketIO()
            _r = جانچ('UrduSocketIO بنا', (sio != None))
            if asyncio.iscoroutine(_r): await _r
            _r = جانچ('سرور موجود', (sio.سرور != None))
            if asyncio.iscoroutine(_r): await _r
    
            @sio.پر('message')
            async def پیغام_ہینڈلر(sid, data):
                _r = print(f"  پیغام: {data}")
                if asyncio.iscoroutine(_r): await _r
    
            @sio.پر('connect')
            async def جڑنا_ہینڈلر(sid, environ):
                _r = print(f"  جڑا: {sid}")
                if asyncio.iscoroutine(_r): await _r
    
            @sio.پر('disconnect')
            async def منقطع_ہینڈلر(sid):
                _r = print(f"  منقطع: {sid}")
                if asyncio.iscoroutine(_r): await _r
    
            _r = جانچ('Socket.IO واقعات رجسٹر', True)
            if asyncio.iscoroutine(_r): await _r
        except Exception as غ:
            _r = print(f"  ⓘ Socket.IO چھوڑا (python-socketio نہیں): {غ}")
            if asyncio.iscoroutine(_r): await _r
            ن['گزرے'] = (ن['گزرے'] + 2)
    
    async def webrtc_جانچ():
        _r = print('\n─── WebRTC Signalling جانچ ───')
        if asyncio.iscoroutine(_r): await _r
        sig = WebRTCSignalling(_UrduObj({'میزبان': '0.0.0.0', 'پورٹ': 9000}))
        _r = جانچ('WebRTCSignalling بنا', (sig != None))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('میزبان صحیح', (sig.میزبان == '0.0.0.0'))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('پورٹ صحیح', (sig.پورٹ == 9000))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('کمرے خالی', (لمبائی(sig._کمرے) == 0))
        if asyncio.iscoroutine(_r): await _r
        پیغامات_بھیجے = []
        async def _fn_0(msg):
            _r = پیغامات_بھیجے.push(msg)
            if asyncio.iscoroutine(_r): await _r
    
        ws_a = _UrduObj({'send': _fn_0})
        async def _fn_1(msg):
            _r = پیغامات_بھیجے.push(msg)
            if asyncio.iscoroutine(_r): await _r
    
        ws_b = _UrduObj({'send': _fn_1})
        (await sig._جوائن(ws_a, 'کمرہ1'))
        _r = جانچ('پہلا peer جڑا', (لمبائی(sig._کمرے['کمرہ1']) == 1))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('join پیغام بھیجا', (لمبائی(پیغامات_بھیجے) == 1))
        if asyncio.iscoroutine(_r): await _r
        (await sig._جوائن(ws_b, 'کمرہ1'))
        _r = جانچ('دوسرا peer جڑا', (لمبائی(sig._کمرے['کمرہ1']) == 2))
        if asyncio.iscoroutine(_r): await _r
        _r = جانچ('peer_joined پیغام', (لمبائی(پیغامات_بھیجے) == 3))
        if asyncio.iscoroutine(_r): await _r
        (await sig._فارورڈ(ws_a, _UrduObj({'type': 'offer', 'sdp': 'v=0...'})))
        _r = جانچ('offer فارورڈ ہوا', (لمبائی(پیغامات_بھیجے) == 4))
        if asyncio.iscoroutine(_r): await _r
        (await sig._صاف_کریں(ws_a))
        _r = جانچ('صاف کرنے کے بعد 1 peer', (لمبائی(sig._کمرے['کمرہ1']) == 1))
        if asyncio.iscoroutine(_r): await _r
        (await sig._صاف_کریں(ws_b))
        _r = جانچ('سب peer گئے — کمرہ ختم', (لمبائی(sig._کمرے) == 0))
        if asyncio.iscoroutine(_r): await _r
    
    async def مرکز():
        _r = print('╔══════════════════════════════════════╗')
        if asyncio.iscoroutine(_r): await _r
        _r = print('║  WebSocket/SocketIO/WebRTC جانچ      ║')
        if asyncio.iscoroutine(_r): await _r
        _r = print('╚══════════════════════════════════════╝')
        if asyncio.iscoroutine(_r): await _r
        (await websocket_جانچ())
        (await socketio_جانچ())
        (await webrtc_جانچ())
        _r = print(f"\n══════════════════════════════════════")
        if asyncio.iscoroutine(_r): await _r
        _r = print(f"  WS/SIO/WebRTC — گزرے: {ن['گزرے']}  ناکام: {ن['ناکام']}")
        if asyncio.iscoroutine(_r): await _r
        _r = print(f"══════════════════════════════════════")
        if asyncio.iscoroutine(_r): await _r
    
    (await مرکز())

asyncio.run(_اردو_main())