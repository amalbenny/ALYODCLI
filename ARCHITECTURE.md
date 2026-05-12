# ALYODCLI C Integration Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALYODCLI C Integration                       │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────────┐
                    │   Python Application     │
                    │   (Pure Python API)      │
                    └────────────┬─────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
     ┌──────────▼──────────┐        ┌────────────▼────────────┐
     │  Cython Extensions  │        │  Socket Server (JSON-RPC)
     │  (text_core.pyx)    │        │  (c_server.py)         │
     │                     │        │                        │
     │ • get_visual_len()  │        │ TCP: 127.0.0.1:5555   │
     │ • strip_ansi()      │        │ Unix: /tmp/*.sock      │
     │ • hex_to_ansi()     │        │                        │
     │ • batch_strip()     │        │ Methods (28):          │
     └──────────┬──────────┘        │ • paint                │
                │                   │ • style_*              │
                │                   │ • text_*               │
                │                   │ • layout_*             │
                │                   │ • widgets_*            │
                │                   │ • help                 │
                │                   └────────────┬────────────┘
                │                                │
                │   ┌─────────────────────────────┘
                │   │
    ┌───────────▼───▼─────────────────────────────┐
    │  ALYODCLI Python Engine                    │
    │ (Core styling, layout, widgets)            │
    │                                             │
    │  • Style (ANSI codes, colors)              │
    │  • Text (alignment, width calc)            │
    │  • Layout (boxes, tables)                  │
    │  • Widgets (hr, bullet, progress, nav)     │
    └─────────────────────────────────────────────┘


                    ┌──────────────────────────┐
                    │   C Client Library       │
                    │   (alyodcli.c)           │
                    └────────────┬─────────────┘
                                 │
                ┌────────────────▼────────────────┐
                │                                 │
    ┌───────────▼──────────┐      ┌──────────────▼──────────┐
    │  C Programs / C++    │      │   CMake / Make / GCC    │
    │   Applications       │      │   Build Systems         │
    └──────────────────────┘      └────────────────────────┘
```

## Data Flow

### Python → C Integration Path:

```
C Program
    │
    ├─ alyodcli_connect_tcp()
    │       │
    │       └─ Socket Connection to localhost:5555
    │               │
    │               ▼
    │       ALYODCLI Socket Server
    │       (c_server.py)
    │               │
    │               ├─ Parse JSON-RPC Request
    │               │
    │               ├─ Call Python Method
    │               │   • Uses Cython extensions
    │               │   • Uses regular Python functions
    │               │
    │               └─ Return JSON-RPC Response
    │
    ├─ alyodcli_paint() / other functions
    │       │
    │       └─ Send JSON-RPC Message
    │               ▼
    │       Socket Server
    │               ▼
    │       Format Response
    │
    └─ alyodcli_response_* functions
            └─ Parse & Return Result
```

## Performance Layers

```
┌──────────────────────────────────────────────────────────┐
│                    C Program                             │
└──────────────────────────────────────────────────────────┘
                         ↓
                    Layer 1: IPC
                (Network/Unix Socket)
                   ~5-10ms latency
                         ↓
┌──────────────────────────────────────────────────────────┐
│          ALYODCLI Socket Server (Python)                 │
└──────────────────────────────────────────────────────────┘
                         ↓
        Layer 2: JSON-RPC Message Parsing
                  ~0.5-1ms overhead
                         ↓
┌──────────────────────────────────────────────────────────┐
│    Python Engine + Cython Extensions                     │
├──────────────────────────────────────────────────────────┤
│  • text_core.pyx (Cython - compiled C)         <1ms     │
│  • Pure Python (optimized)                    ~1-2ms    │
│  • Regular Python (baseline)                  ~5-10ms   │
└──────────────────────────────────────────────────────────┘
```

## Build Integration Paths

```
┌─────────────────────────────────────────────────────────────┐
│            C Developer Workflow                             │
└─────────────────────────────────────────────────────────────┘

   Path 1: Quick Start (Recommended)
   ──────────────────────────────
   Source: *.c files
       │
       ├─ gcc myapp.c c_bindings/alyodcli.c
       │       │
       │       └─ Executable (myapp)
       │
       └─ Runtime: Connect to alyodcli-server
           (no compilation needed for server)

   Path 2: Using Make
   ──────────────────
   Source: c_bindings/Makefile
       │
       ├─ make all
       │       │
       │       ├─ libalyodcli.a (static lib)
       │       └─ example_client (binary)
       │
       └─ make install (system-wide)

   Path 3: Using CMake
   ───────────────────
   Source: c_bindings/CMakeLists.txt
       │
       ├─ cmake .
       │
       ├─ make
       │       │
       │       ├─ libalyodcli.a (static lib)
       │       └─ example_client (binary)
       │
       └─ make install

   Path 4: Shared Library
   ──────────────────────
   Source: c_bindings/alyodcli.c
       │
       ├─ gcc -shared -fPIC -o libalyodcli.so alyodcli.c
       │
       └─ Link with: -lalyodcli -L./c_bindings
```

## Deployment Scenarios

### Scenario 1: Development
```
┌──────────────┐
│ C Program    │
│ (compiled)   │
└──────┬───────┘
       │
       │ TCP/Socket
       ▼
┌──────────────────────┐
│ alyodcli-server      │
│ (running locally)    │
└──────────────────────┘
```

### Scenario 2: Shared Library
```
┌────────────────────────────────┐
│ C Program (statically linked)  │
│ libalyodcli.a (embedded)       │
└────────────────────────────────┘
```

### Scenario 3: System Integration
```
/usr/local/lib/
  ├─ libalyodcli.a
  └─ libalyodcli.so

/usr/local/include/
  └─ alyodcli.h

C Program ──links to──> libalyodcli.so
```

## API Surface

```
C Program
    │
    ├─ Connection Functions (3)
    │   ├─ alyodcli_connect()
    │   ├─ alyodcli_connect_tcp()
    │   ├─ alyodcli_connect_unix()
    │   └─ alyodcli_disconnect()
    │
    ├─ Style Functions (4)
    │   ├─ alyodcli_paint()
    │   ├─ alyodcli_style_get()
    │   ├─ alyodcli_style_ext()
    │   └─ alyodcli_style_hex()
    │
    ├─ Text Functions (2)
    │   ├─ alyodcli_text_visual_len()
    │   └─ alyodcli_text_align()
    │
    ├─ Layout Functions (2)
    │   ├─ alyodcli_layout_box()
    │   └─ alyodcli_layout_table()
    │
    ├─ Widget Functions (3)
    │   ├─ alyodcli_widgets_hr()
    │   ├─ alyodcli_widgets_bullet()
    │   └─ alyodcli_widgets_progress()
    │
    ├─ Utility Functions (1)
    │   └─ alyodcli_help()
    │
    └─ Response Functions (4)
        ├─ alyodcli_response_free()
        ├─ alyodcli_response_ok()
        ├─ alyodcli_response_error()
        └─ alyodcli_response_result()

Total: 26 Core Functions
```

## Error Handling Flow

```
C Call
    │
    ├─ Validation ─────► Invalid? ─► Return Error Response
    │
    ├─ Socket Send ────► Failed? ─► Network Error
    │
    ├─ Server Process ──► JSON-RPC Error? ─► Method Error
    │
    ├─ Method Execution ► Python Error? ─► Exception Caught
    │
    └─ Response Received
            │
            ├─ Parse ──────► Parse Error? ─► Return Parse Error
            │
            └─ Return to Caller
                    │
                    ├─ alyodcli_response_ok() ──► Check Success
                    │
                    └─ alyodcli_response_error() ─► Get Error Message
```
