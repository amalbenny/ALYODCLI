# ALYODCLI C Integration - Quick Reference

## Overview

ALYODCLI is now compatible with C/C++ programs through:
1. **Performance-optimized Cython extensions** (3-5x faster text processing)
2. **Socket server interface** (JSON-RPC 2.0 protocol)
3. **C client library** with 40+ functions

## Installation & Setup

### Step 1: Install ALYODCLI
```bash
pip install alyodcli
```

### Step 2: Start the Socket Server
```bash
# TCP mode (default)
alyodcli-server --host 127.0.0.1 --port 5555

# Unix socket mode (Linux/macOS)
alyodcli-server --unix /tmp/alyodcli.sock

# Run in background
alyodcli-server --host 127.0.0.1 --port 5555 &
```

### Step 3: Build Your C Program

**Using Make (Recommended):**
```bash
cd c_bindings
make all
./example_client  # Run the example
```

**Using CMake:**
```bash
cd c_bindings
cmake .
make
./example_client
```

**Using GCC directly:**
```bash
gcc -o myapp myapp.c c_bindings/alyodcli.c -lws2_32  # Windows
gcc -o myapp myapp.c c_bindings/alyodcli.c           # Linux/macOS
```

## Basic C Example

```c
#include "c_bindings/alyodcli.h"
#include <stdio.h>

int main() {
    // Connect to server
    AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);
    if (!client) {
        fprintf(stderr, "Connection failed\n");
        return 1;
    }

    // Example 1: Paint text with styles
    const char *styles[] = {"cyan", "bold"};
    AlyodcliResponse resp = alyodcli_paint(client, "Hello!", styles, 2);
    printf("%s\n", alyodcli_response_result(&resp));
    alyodcli_response_free(&resp);

    // Example 2: Text alignment
    resp = alyodcli_text_align(client, "Centered", 40, "center", NULL, 0);
    printf("%s\n", alyodcli_response_result(&resp));
    alyodcli_response_free(&resp);

    // Example 3: Horizontal rule
    resp = alyodcli_widgets_hr(client, 50, "═", "green");
    printf("%s\n", alyodcli_response_result(&resp));
    alyodcli_response_free(&resp);

    // Clean up
    alyodcli_disconnect(client);
    return 0;
}
```

## Common Functions

### Text Styling
```c
alyodcli_paint(client, "Text", styles, num_styles);
alyodcli_style_get(client, "red");
alyodcli_style_hex(client, "#ff6b6b", 0);
alyodcli_style_ext(client, 196, 0);  // 256-color
```

### Text Processing
```c
alyodcli_text_visual_len(client, "Test");
alyodcli_text_align(client, "Text", 40, "center", NULL, 0);
```

### Layouts
```c
alyodcli_layout_box(client, "Content", 40, "center", "cyan");
alyodcli_layout_table(client, json_array, "cyan", "dim");
```

### Widgets
```c
alyodcli_widgets_hr(client, 40, "─", "dim");
alyodcli_widgets_bullet(client, "Item", "•", "green", 0);
alyodcli_widgets_progress(client, 50, 100, "Loading", 30, "cyan");
```

## Available Styles

### Colors
- `red`, `green`, `yellow`, `blue`, `cyan`, `magenta`, `white`, `black`
- `bg_red`, `bg_green`, `bg_yellow`, etc. (backgrounds)

### Effects
- `bold`, `underline`, `dim`, `italic`, `strike`

### Special
- `reset` - Reset to default

## Response Handling

```c
AlyodcliResponse resp = alyodcli_paint(client, "Text", styles, 1);

// Check if successful
if (alyodcli_response_ok(&resp)) {
    printf("Result: %s\n", alyodcli_response_result(&resp));
} else {
    fprintf(stderr, "Error: %s (code: %d)\n", 
            alyodcli_response_error(&resp), 
            resp.error_code);
}

// Always free responses
alyodcli_response_free(&resp);
```

## Connection Types

### TCP (Cross-Platform)
```c
AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);
```

### Unix Socket (Linux/macOS)
```c
AlyodcliClient *client = alyodcli_connect_unix("/tmp/alyodcli.sock");
```

### Custom Options
```c
AlyodcliConnOpts opts = {
    .type = ALYODCLI_TCP,
    .host = "127.0.0.1",
    .port = 5555,
    .timeout_ms = 5000
};
AlyodcliClient *client = alyodcli_connect(&opts);
```

## Troubleshooting

### Connection Refused
**Problem**: `Failed to connect`  
**Solution**: Start the server first:
```bash
alyodcli-server --host 127.0.0.1 --port 5555
```

### Parse Errors
**Problem**: `Parse error` response  
**Solution**: Check parameter formatting (strings must be quoted in JSON)

### Method Not Found
**Problem**: `Method not found` response  
**Solution**: Verify method name spelling. See API reference.

### Windows Socket Error
**Problem**: Link error with socket functions  
**Solution**: Compile with `-lws2_32`:
```bash
gcc -o app app.c c_bindings/alyodcli.c -lws2_32
```

## Performance Tips

1. **Batch Operations**: Group multiple calls in a single request
2. **Reuse Connections**: Keep client connected, don't reconnect for each call
3. **Use Cython Extensions**: Build with Cython for 3-5x faster operations
4. **Connection Pooling**: For high-throughput, maintain multiple connections

## Documentation

For complete documentation, see:
- [c_bindings/README.md](c_bindings/README.md) - Full API reference
- [c_bindings/example_client.c](c_bindings/example_client.c) - Working examples
- [c_bindings/alyodcli.h](c_bindings/alyodcli.h) - Function prototypes

## Server Command Options

```bash
alyodcli-server --help

Options:
  --host ADDR       TCP host (default: 127.0.0.1)
  --port PORT       TCP port (default: 5555)
  --unix PATH       Enable Unix socket mode
  --daemonize       Run as background daemon
```

## Platform Support

| Platform | TCP | Unix Socket | Status |
|----------|-----|-------------|--------|
| Windows  | ✅  | ❌          | ✅ Tested |
| Linux    | ✅  | ✅          | ✅ Tested |
| macOS    | ✅  | ✅          | ✅ Tested |

## Building with Cython (Optional)

For 3-5x performance improvement on text processing:

```bash
pip install cython setuptools wheel
cd /path/to/alyodcli
python setup.py build_ext --inplace
```

## License

Apache License 2.0 - See LICENSE.txt

## Quick Links

- **Repository**: https://github.com/amalb1883/alyodcli
- **PyPI**: https://pypi.org/project/alyodcli/
- **Issues**: Report bugs on GitHub
