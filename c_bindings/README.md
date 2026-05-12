# ALYODCLI C Integration Guide

This directory contains C language bindings and utilities for integrating ALYODCLI with C/C++ programs.

## Architecture

There are two ways to use ALYODCLI from C:

### 1. **Socket Server (Recommended)**
- Run ALYODCLI as a socket server (TCP or Unix domain socket)
- C programs connect and communicate via JSON-RPC 2.0 protocol
- **Advantages**: No compilation needed, platform-independent, process-isolated
- **Disadvantages**: Requires server to be running, network latency

### 2. **Direct C Library (Advanced)**
- Link directly with compiled C library
- Requires Cython compilation
- **Advantages**: Faster, no network overhead
- **Disadvantages**: More complex build setup

## Getting Started

### Step 1: Start the ALYODCLI Socket Server

```bash
# Install ALYODCLI first
pip install alyodcli

# Start TCP socket server (default)
alyodcli-server --host 127.0.0.1 --port 5555

# Or use Unix socket (Linux/macOS)
alyodcli-server --unix /tmp/alyodcli.sock
```

### Step 2: Build Your C Program

```bash
# Compile with the C client library
gcc -o my_program my_program.c alyodcli.c

# Windows (requires WinSock)
gcc -o my_program.exe my_program.c alyodcli.c -lws2_32
```

### Step 3: Write Your C Code

```c
#include "alyodcli.h"
#include <stdio.h>

int main() {
    // Connect to server
    AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);
    if (!client) {
        fprintf(stderr, "Failed to connect\n");
        return 1;
    }

    // Paint styled text
    const char *styles[] = {"cyan", "bold"};
    AlyodcliResponse resp = alyodcli_paint(client, "Hello World!", styles, 2);
    
    if (alyodcli_response_ok(&resp)) {
        printf("%s\n", alyodcli_response_result(&resp));
    } else {
        fprintf(stderr, "Error: %s\n", alyodcli_response_error(&resp));
    }

    // Clean up
    alyodcli_response_free(&resp);
    alyodcli_disconnect(client);
    
    return 0;
}
```

## API Reference

### Connection Management

```c
AlyodcliClient *alyodcli_connect_tcp(const char *host, uint16_t port);
AlyodcliClient *alyodcli_connect_unix(const char *socket_path);  // Unix/Linux only
void alyodcli_disconnect(AlyodcliClient *client);
```

### Style Functions

```c
AlyodcliResponse alyodcli_paint(AlyodcliClient *client, const char *text,
                                const char **styles, int num_styles);
AlyodcliResponse alyodcli_style_get(AlyodcliClient *client, const char *name);
AlyodcliResponse alyodcli_style_ext(AlyodcliClient *client, int color_index,
                                    int background);
AlyodcliResponse alyodcli_style_hex(AlyodcliClient *client, const char *hex_code,
                                    int background);
```

### Text Functions

```c
AlyodcliResponse alyodcli_text_visual_len(AlyodcliClient *client, const char *text);
AlyodcliResponse alyodcli_text_align(AlyodcliClient *client, const char *text,
                                     int width, const char *align,
                                     const char **styles, int num_styles);
```

### Layout Functions

```c
AlyodcliResponse alyodcli_layout_box(AlyodcliClient *client, const char *content,
                                     int width, const char *align, const char *color);
AlyodcliResponse alyodcli_layout_table(AlyodcliClient *client, const char *json_data,
                                       const char *header_color, const char *border_color);
```

### Widget Functions

```c
AlyodcliResponse alyodcli_widgets_hr(AlyodcliClient *client, int width,
                                     const char *character, const char *color);
AlyodcliResponse alyodcli_widgets_bullet(AlyodcliClient *client, const char *text,
                                         const char *character, const char *color,
                                         int indent);
AlyodcliResponse alyodcli_widgets_progress(AlyodcliClient *client, int iteration,
                                          int total, const char *prefix,
                                          int length, const char *color);
```

### Utility Functions

```c
AlyodcliResponse alyodcli_help(AlyodcliClient *client, const char *topic);
void alyodcli_response_free(AlyodcliResponse *resp);
int alyodcli_response_ok(const AlyodcliResponse *resp);
const char *alyodcli_response_error(const AlyodcliResponse *resp);
const char *alyodcli_response_result(const AlyodcliResponse *resp);
```

## Available Styles

### Colors
- `red`, `green`, `yellow`, `blue`, `cyan`, `magenta`, `white`, `black`
- `bg_red`, `bg_green`, `bg_yellow`, `bg_blue`, `bg_cyan`, `bg_magenta`, `bg_white`, `bg_black`

### Text Effects
- `bold`, `underline`, `dim`, `italic`, `strike`

### Special
- `reset` - Reset to default style

## Examples

### Example 1: Styled Text

```c
#include "alyodcli.h"
#include <stdio.h>

int main() {
    AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);
    
    const char *styles[] = {"green", "bold"};
    AlyodcliResponse resp = alyodcli_paint(client, "Success!", styles, 2);
    printf("%s\n", alyodcli_response_result(&resp));
    
    alyodcli_response_free(&resp);
    alyodcli_disconnect(client);
    return 0;
}
```

### Example 2: Color Conversion

```c
#include "alyodcli.h"
#include <stdio.h>

int main() {
    AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);
    
    // Convert hex color
    AlyodcliResponse resp = alyodcli_style_hex(client, "#ff6b6b", 0);
    if (alyodcli_response_ok(&resp)) {
        printf("ANSI Code: %s\n", alyodcli_response_result(&resp));
    }
    
    alyodcli_response_free(&resp);
    alyodcli_disconnect(client);
    return 0;
}
```

### Example 3: Text Alignment

```c
#include "alyodcli.h"
#include <stdio.h>

int main() {
    AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);
    
    const char *styles[] = {"yellow"};
    AlyodcliResponse resp = alyodcli_text_align(
        client, "Centered Text", 50, "center", styles, 1
    );
    
    printf("%s\n", alyodcli_response_result(&resp));
    
    alyodcli_response_free(&resp);
    alyodcli_disconnect(client);
    return 0;
}
```

### Example 4: Progress Bar

```c
#include "alyodcli.h"
#include <stdio.h>

int main() {
    AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);
    
    for (int i = 0; i <= 100; i += 10) {
        AlyodcliResponse resp = alyodcli_widgets_progress(
            client, i, 100, "Loading", 30, "cyan"
        );
        alyodcli_response_free(&resp);
    }
    
    alyodcli_disconnect(client);
    return 0;
}
```

## JSON-RPC Protocol

The socket server communicates using JSON-RPC 2.0. Here's the request format:

```json
{
    "jsonrpc": "2.0",
    "method": "paint",
    "params": ["Hello", "cyan", "bold"],
    "id": 1
}
```

Response:

```json
{
    "jsonrpc": "2.0",
    "result": "\u001b[96mHello\u001b[0m",
    "id": 1
}
```

Error response:

```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32601,
        "message": "Method not found: invalid_method"
    },
    "id": 1
}
```

## Building as Shared Library (Advanced)

To build ALYODCLI as a shared library:

```bash
# Install build dependencies
pip install cython setuptools wheel

# Build extension
python setup.py build_ext --inplace

# This creates:
# - Windows: ALYODCLI\text_core.pyd
# - Unix: ALYODCLI/text_core.so

# For standalone shared library
python -m cython ALYODCLI/text_core.pyx
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
    -I/usr/include/python3.x \
    -o text_core.so text_core.c
```

## Platform Support

| Platform | TCP | Unix Socket | Direct Library |
|----------|-----|-------------|----------------|
| Windows  | ✅  | ❌          | ✅ (.pyd)      |
| Linux    | ✅  | ✅          | ✅ (.so)       |
| macOS    | ✅  | ✅          | ✅ (.dylib)    |

## Troubleshooting

### Connection Refused
```
Error: Connection refused
```
**Solution**: Make sure the server is running:
```bash
alyodcli-server --host 127.0.0.1 --port 5555
```

### Parse Errors
```
Error: Parse error
```
**Cause**: Invalid JSON format in request  
**Solution**: Check that all parameters are properly formatted

### Method Not Found
```
Error: Method not found
```
**Cause**: Typo in method name or using unsupported method  
**Solution**: Check available methods in `alyodcli.h`

## Performance Considerations

- **Socket server**: ~5-10ms per call (network roundtrip)
- **Direct library**: <1ms per call (no network)
- For high-performance needs, use direct library with precompiled extensions

## License

Same as ALYODCLI (Apache License 2.0)

## Contributing

Contributions welcome! Please submit pull requests to the main repository.
