/*
 * ALYODCLI C Client Library Header
 * Provides a C interface for communicating with ALYODCLI server via sockets
 */

#ifndef ALYODCLI_H
#define ALYODCLI_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

/* Connection types */
typedef enum {
    ALYODCLI_TCP,      /* TCP socket connection */
    ALYODCLI_UNIX      /* Unix domain socket (Unix/Linux only) */
} AlyodcliConnType;

/* Opaque client handle */
typedef struct AlyodcliClient AlyodcliClient;

/* Connection options */
typedef struct {
    AlyodcliConnType type;
    const char *host;       /* TCP mode: hostname/IP */
    uint16_t port;          /* TCP mode: port number */
    const char *unix_path;  /* Unix mode: socket path */
    int timeout_ms;         /* Connection timeout in milliseconds */
} AlyodcliConnOpts;

/* Response from server */
typedef struct {
    int success;            /* 1 if successful, 0 if error */
    char *result;           /* Result string (or error message if failed) */
    int error_code;         /* JSON-RPC error code (0 if no error) */
    char *error_msg;        /* Error message from server */
} AlyodcliResponse;

/* ============================================
 * Connection Management
 * ============================================ */

/**
 * Create and connect to ALYODCLI server.
 * Returns NULL on failure.
 */
AlyodcliClient *alyodcli_connect(const AlyodcliConnOpts *opts);

/**
 * Create TCP connection with default options.
 * Returns NULL on failure.
 */
AlyodcliClient *alyodcli_connect_tcp(const char *host, uint16_t port);

/**
 * Create Unix socket connection.
 * Returns NULL on failure (or on Windows).
 */
AlyodcliClient *alyodcli_connect_unix(const char *socket_path);

/**
 * Close connection and free resources.
 */
void alyodcli_disconnect(AlyodcliClient *client);

/* ============================================
 * Core Style Functions
 * ============================================ */

/**
 * Apply styles to text.
 * Styles: "red", "green", "yellow", "blue", "cyan", "magenta", "white", "black"
 *         "bold", "underline", "dim", "italic", "strike"
 *         "bg_red", "bg_green", etc.
 */
AlyodcliResponse alyodcli_paint(AlyodcliClient *client, const char *text, 
                                const char **styles, int num_styles);

/**
 * Get standard ANSI code by name.
 */
AlyodcliResponse alyodcli_style_get(AlyodcliClient *client, const char *name);

/**
 * Get 256-color ANSI code.
 */
AlyodcliResponse alyodcli_style_ext(AlyodcliClient *client, int color_index,
                                    int background);

/**
 * Get 24-bit RGB color ANSI code from hex.
 */
AlyodcliResponse alyodcli_style_hex(AlyodcliClient *client, const char *hex_code,
                                    int background);

/* ============================================
 * Text Processing Functions
 * ============================================ */

/**
 * Calculate visual length of text (accounting for wide chars and ANSI codes).
 */
AlyodcliResponse alyodcli_text_visual_len(AlyodcliClient *client, const char *text);

/**
 * Align text within a given width.
 * Align: "left", "center", "right"
 */
AlyodcliResponse alyodcli_text_align(AlyodcliClient *client, const char *text,
                                     int width, const char *align,
                                     const char **styles, int num_styles);

/* ============================================
 * Layout Functions
 * ============================================ */

/**
 * Create a box around content.
 */
AlyodcliResponse alyodcli_layout_box(AlyodcliClient *client, const char *content,
                                     int width, const char *align, const char *color);

/**
 * Render a table from JSON array of objects.
 * JSON format: [{"col1": "val1", "col2": "val2"}, ...]
 */
AlyodcliResponse alyodcli_layout_table(AlyodcliClient *client, const char *json_data,
                                       const char *header_color, const char *border_color);

/* ============================================
 * Widget Functions
 * ============================================ */

/**
 * Draw a horizontal rule.
 */
AlyodcliResponse alyodcli_widgets_hr(AlyodcliClient *client, int width,
                                     const char *character, const char *color);

/**
 * Print a bulleted item.
 */
AlyodcliResponse alyodcli_widgets_bullet(AlyodcliClient *client, const char *text,
                                         const char *character, const char *color,
                                         int indent);

/**
 * Display a progress bar.
 */
AlyodcliResponse alyodcli_widgets_progress(AlyodcliClient *client, int iteration,
                                          int total, const char *prefix,
                                          int length, const char *color);

/* ============================================
 * Utility Functions
 * ============================================ */

/**
 * Get help text.
 */
AlyodcliResponse alyodcli_help(AlyodcliClient *client, const char *topic);

/**
 * Free a response object.
 */
void alyodcli_response_free(AlyodcliResponse *resp);

/**
 * Check if response is successful.
 */
int alyodcli_response_ok(const AlyodcliResponse *resp);

/**
 * Get error message from response.
 */
const char *alyodcli_response_error(const AlyodcliResponse *resp);

/**
 * Get result from response.
 */
const char *alyodcli_response_result(const AlyodcliResponse *resp);

#ifdef __cplusplus
}
#endif

#endif /* ALYODCLI_H */
