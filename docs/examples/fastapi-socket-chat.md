# FastAPI Socket.IO Chat App — اردو چیٹ

A real-time multi-user chat application built with FastAPI and Socket.IO. Demonstrates ASGI integration, Socket.IO event handlers, broadcasting to all clients, and an embedded HTML/JS frontend served from the same server.

> **اردو:** FastAPI اور Socket.IO سے بنی ایک حقیقی وقت کی کثیر صارف چیٹ ایپلیکیشن۔ یہ مثال ASGI انضمام، Socket.IO ایونٹ ہینڈلرز، تمام کلائنٹس کو نشر، اور ایمبیڈڈ HTML/JS فرنٹ اینڈ ظاہر کرتی ہے۔

---

## چلانے کا طریقہ / How to Run

```bash
pip install fastapi uvicorn python-socketio
cd examples/FASTAPI_SOCKET_CHAT_APP
urdu run chat.urdu
```

Then open **http://localhost:5000** in two or more browser tabs, enter different names, and chat.

---

## Features

| Feature | Description |
|---------|-------------|
| Real-time messaging | Socket.IO pushes messages to all connected clients instantly |
| User join/leave | System messages when users connect or disconnect |
| Embedded frontend | HTML + Socket.IO JS client served from the same FastAPI server |
| No threading | Sync handlers + `غیر_متزامن_چلائیں()` bridge for safe async broadcasting |

---

## Architecture

```
Browser (Socket.IO JS client)
        ↕  Socket.IO over HTTP/WebSocket
FastAPI + python-socketio (ASGI)
        ↕  sio.چلائیں(ایپ, پورٹ=5000)
        uvicorn
```

The key insight: `socketio.ASGIApp` wraps both the Socket.IO server and the FastAPI app into a single ASGI application. All HTTP requests go to FastAPI; all Socket.IO events go to the Socket.IO handlers.

---

## Code Walkthrough

### 1. Imports and Setup

```urdu
درآمد { فاسٹ_اے_پی_آئی, ایچ_ٹی_ایم_ایل_جواب } سے "اردو/ویب";
درآمد { ساکٹ_آئی_او } سے "اردو/ویب";
درآمد { غیر_متزامن_چلائیں } سے "اردو/دھاگہ";

متغیر ایپ = نیا فاسٹ_اے_پی_آئی({ عنوان: "اردو چیٹ" });
متغیر sio = نیا ساکٹ_آئی_او({ کورس: ["*"] });
متغیر صارفین = {};
```

- `فاسٹ_اے_پی_آئی` — FastAPI HTTP server (serves the HTML page)
- `ساکٹ_آئی_او` — python-socketio `AsyncServer` (handles WebSocket events)
- `غیر_متزامن_چلائیں` — bridge that schedules a coroutine on the running event loop
- `صارفین` — in-memory dict mapping `sid → نام` (session ID → user name)

---

### 2. Serving the HTML Page

```urdu
متغیر صفحہ = `<!DOCTYPE html>
<html dir="rtl" lang="ur">
...
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
...
</html>`;

@ایپ.حاصل("/")
فنکشن جڑ() {
    واپس نیا ایچ_ٹی_ایم_ایل_جواب(صفحہ);
}
```

The entire frontend (HTML + CSS + JavaScript) is stored in a template literal and returned as an `ایچ_ٹی_ایم_ایل_جواب`. The Socket.IO client JS is loaded from CDN.

**Template literal rules:**
- Multi-line backtick strings are supported
- `${variable}` for server-side interpolation (processed at startup, not per-request)
- CSS `{` and `}` are auto-escaped by the transpiler

---

### 3. Socket.IO Event Handlers

```urdu
// ─── جڑنا ─────────────────────────────────────────
@sio.پر_جڑنا()
فنکشن جڑنا(sid, environ) {
    صارفین[sid] = "مہمان";
    لکھو("جڑا: " + sid);
}

// ─── نام سیٹ کرنا ─────────────────────────────────
@sio.پر("نام_سیٹ")
فنکشن نام_سیٹ(sid, data) {
    متغیر نام = data["نام"];
    صارفین[sid] = نام;
    غیر_متزامن_چلائیں(sio.نشر("پیغام", { "نام": نام, "متن": "چیٹ میں شامل ہوا", "نوع": "شامل" }));
}

// ─── پیغام ────────────────────────────────────────
@sio.پر("پیغام")
فنکشن پیغام_ملا(sid, data) {
    متغیر نام = صارفین.get(sid, "مہمان");
    غیر_متزامن_چلائیں(sio.نشر("پیغام", { "نام": نام, "متن": data["متن"], "نوع": "پیغام" }));
}

// ─── منقطع ────────────────────────────────────────
@sio.پر_منقطع()
فنکشن منقطع(sid) {
    متغیر نام = صارفین.get(sid, "صارف");
    غیر_متزامن_چلائیں(sio.نشر("پیغام", { "نام": نام, "متن": "چیٹ سے چلا گیا", "نوع": "گیا" }));
}
```

| Decorator | Event | Description |
|-----------|-------|-------------|
| `@sio.پر_جڑنا()` | `connect` | Fires when a client connects |
| `@sio.پر("event")` | custom | Fires when client emits that event |
| `@sio.پر_منقطع()` | `disconnect` | Fires when a client disconnects |

---

### 4. Sync Handlers + Async Broadcasting

This is the most important design decision in the app.

**The problem:** `sio.نشر()` is an `async` coroutine. But using `غیر_متزامن فنکشن` handlers triggers `_has_async=True` in the Urdu PL transpiler, which wraps the entire module in `asyncio.run()`. When `sio.چلائیں()` then starts uvicorn (which has its own event loop), a nested `asyncio.run()` crash occurs.

**The solution:** Keep all Socket.IO handlers as plain sync functions. Use `غیر_متزامن_چلائیں()` to schedule the broadcast coroutine onto the already-running uvicorn event loop:

```urdu
// ✓ صحیح — sync handler + غیر_متزامن_چلائیں
فنکشن پیغام_ملا(sid, data) {
    غیر_متزامن_چلائیں(sio.نشر("پیغام", { ... }));
}

// ✗ غلط — async handler causes nested asyncio.run() crash
غیر_متزامن فنکشن پیغام_ملا(sid, data) {
    انتظار sio.نشر("پیغام", { ... });
}
```

`غیر_متزامن_چلائیں()` (from `اردو/دھاگہ`) detects whether an event loop is already running (it is, inside uvicorn) and uses `asyncio.ensure_future()` to schedule the coroutine safely.

---

### 5. Starting the Server

```urdu
sio.چلائیں(ایپ, پورٹ=5000);
```

`ساکٹ_آئی_او.چلائیں()` auto-detects the framework: when passed a `فاسٹ_اے_پی_آئی` wrapper it unwraps it automatically, calls `socketio.ASGIApp(sio_server, raw_fastapi_app)`, and starts uvicorn. You can pass the wrapper directly — `.ایپ` is no longer needed.

---

### 6. Browser-Side JavaScript

The embedded JS uses the Socket.IO client to connect, emit events, and listen for messages:

```javascript
var socket = null;
var اپنا_نام = '';

function جوڑو() {
  socket = io();
  socket.on('connect', function() {
    socket.emit('نام_سیٹ', { نام: اپنا_نام });
  });
  socket.on('پیغام', function(data) {
    پیغام_شامل(data);
  });
}

function بھیجو() {
  socket.emit('پیغام', { متن: متن });
}
```

Socket.IO event names (`'نام_سیٹ'`, `'پیغام'`) are Urdu strings — they match exactly with the server-side `@sio.پر("نام_سیٹ")` decorators.

---

## Message Flow

```
User types message → browser emits 'پیغام'
    → server: پیغام_ملا(sid, data)
        → غیر_متزامن_چلائیں(sio.نشر('پیغام', {...}))
            → all connected browsers receive 'پیغام' event
                → پیغام_شامل(data) renders it in the chat box
```

---

## File Structure

```
examples/FASTAPI_SOCKET_CHAT_APP/
  chat.urdu     ← main application (server + embedded frontend)
  chat.html     ← standalone HTML frontend (alternative, connects to same server)
  chat.urduc    ← compiled Python (auto-generated, do not edit)
```

---

## Stopping the Server — سرور بند کرنا

> ⚠️ **Ctrl+C does not stop this server.** uvicorn keeps running after the signal. Kill the process from another terminal:
>
> ```
> taskkill /F /IM urdu.exe        # CMD / PowerShell
> Stop-Process -Name urdu -Force  # PowerShell
> ```
>
> **اردو:** `Ctrl+C` uvicorn سرور نہیں روکتا — اوپر دی گئی کمانڈ استعمال کریں۔

---

## Known Limitations

| Limitation | Reason | Workaround |
|------------|--------|------------|
| No message history | In-memory only | Store messages in a list and send history on connect |
| No rooms | Single global broadcast | Use `sio.کمرہ_میں_شامل()` and emit to specific rooms |
| No persistence | Resets on restart | Connect `اردو/ڈیٹا_بیس` for message storage |

---

## Next Steps

- Add chat rooms: `sio.کمرہ_میں_شامل(sid, کمرہ)` then emit to room only
- Persist messages in SQLite: `اردو/ڈیٹا_بیس`
- Add username uniqueness validation in `نام_سیٹ` handler
- Deploy with: `uvicorn main:app --host 0.0.0.0 --port 5000`
