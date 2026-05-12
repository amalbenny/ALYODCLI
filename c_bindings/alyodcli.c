/*
 * ALYODCLI C Client Library Implementation
 * Provides a C interface for communicating with ALYODCLI server via sockets
 */

#include "alyodcli.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>

#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #pragma comment(lib, "ws2_32.lib")
    typedef int socklen_t;
    #define SOCKET_ERROR INVALID_SOCKET
#else
    #include <sys/socket.h>
    #include <sys/un.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    #include <sys/time.h>
    #define INVALID_SOCKET -1
    #define SOCKET_ERROR -1
    #define closesocket close
    typedef int SOCKET;
#endif

#define ALYODCLI_BUFFER_SIZE 65536
#define ALYODCLI_MAX_JSON 8192

/* Client structure */
struct AlyodcliClient {
    SOCKET socket;
    AlyodcliConnType type;
    struct sockaddr_in tcp_addr;
    char *unix_path;
    int timeout_ms;
};

/* ============================================
 * Internal Utilities
 * ============================================ */

static void _alyodcli_init_winsock() {
#ifdef _WIN32
    static int initialized = 0;
    if (!initialized) {
        WSADATA wsa;
        WSAStartup(MAKEWORD(2, 2), &wsa);
        initialized = 1;
    }
#endif
}

static AlyodcliResponse _alyodcli_json_rpc_call(AlyodcliClient *client,
                                                const char *method,
                                                const char *json_params) {
    AlyodcliResponse resp = {0};
    char request_buf[ALYODCLI_MAX_JSON];
    char response_buf[ALYODCLI_BUFFER_SIZE];
    int n;

    if (!client || client->socket == INVALID_SOCKET) {
        resp.success = 0;
        resp.error_code = -32099;
        resp.error_msg = "Not connected";
        return resp;
    }

    /* Build JSON-RPC request */
    static int request_id = 1;
    snprintf(request_buf, sizeof(request_buf),
             "{\"jsonrpc\":\"2.0\",\"method\":\"%s\",\"params\":%s,\"id\":%d}\n",
             method, json_params, request_id++);

    /* Send request */
    if (send(client->socket, request_buf, strlen(request_buf), 0) == SOCKET_ERROR) {
        resp.success = 0;
        resp.error_code = -32000;
        resp.error_msg = "Failed to send request";
        return resp;
    }

    /* Receive response */
    memset(response_buf, 0, sizeof(response_buf));
    n = recv(client->socket, response_buf, sizeof(response_buf) - 1, 0);

    if (n == SOCKET_ERROR || n == 0) {
        resp.success = 0;
        resp.error_code = -32000;
        resp.error_msg = "Failed to receive response";
        return resp;
    }

    response_buf[n] = '\0';

    /* Parse response (basic JSON parsing) */
    /* This is a simple implementation - production code might use jsmn or similar */
    if (strstr(response_buf, "\"error\"")) {
        resp.success = 0;
        /* Extract error message if present */
        char *msg_start = strstr(response_buf, "\"message\":\"");
        if (msg_start) {
            msg_start += 11;
            char *msg_end = strchr(msg_start, '"');
            if (msg_end) {
                int len = msg_end - msg_start;
                resp.error_msg = (char *)malloc(len + 1);
                strncpy(resp.error_msg, msg_start, len);
                resp.error_msg[len] = '\0';
            }
        }
    } else {
        resp.success = 1;
        /* Extract result - find "result": and get the string value */
        char *result_start = strstr(response_buf, "\"result\":");
        if (result_start) {
            result_start += 9;
            /* Skip whitespace */
            while (*result_start == ' ' || *result_start == '\t') result_start++;

            /* Handle different result types */
            if (*result_start == '"') {
                /* String result */
                result_start++;
                char *result_end = strchr(result_start, '"');
                if (result_end) {
                    int len = result_end - result_start;
                    resp.result = (char *)malloc(len + 1);
                    strncpy(resp.result, result_start, len);
                    resp.result[len] = '\0';
                }
            } else if (*result_start == '[' || *result_start == '{') {
                /* JSON object/array result */
                char *result_end = strchr(result_start, ',');
                if (!result_end) result_end = strchr(result_start, '}');
                if (!result_end) result_end = strchr(result_start, ']');
                if (result_end) {
                    int len = result_end - result_start;
                    resp.result = (char *)malloc(len + 1);
                    strncpy(resp.result, result_start, len);
                    resp.result[len] = '\0';
                }
            } else {
                /* Numeric/boolean result */
                char *result_end = strpbrk(result_start, ",\n}");
                if (result_end) {
                    int len = result_end - result_start;
                    resp.result = (char *)malloc(len + 1);
                    strncpy(resp.result, result_start, len);
                    resp.result[len] = '\0';
                }
            }
        }
    }

    return resp;
}

static AlyodcliResponse _alyodcli_simple_call(AlyodcliClient *client,
                                              const char *method) {
    return _alyodcli_json_rpc_call(client, method, "[]");
}

static char *_alyodcli_escape_json_string(const char *str) {
    if (!str) return calloc(3, 1);  /* "null" without the null chars */

    size_t len = strlen(str);
    char *escaped = malloc(len * 2 + 3);  /* Worst case + quotes + null */
    char *p = escaped;

    *p++ = '"';
    for (size_t i = 0; i < len; i++) {
        switch (str[i]) {
            case '"': *p++ = '\\'; *p++ = '"'; break;
            case '\\': *p++ = '\\'; *p++ = '\\'; break;
            case '\n': *p++ = '\\'; *p++ = 'n'; break;
            case '\r': *p++ = '\\'; *p++ = 'r'; break;
            case '\t': *p++ = '\\'; *p++ = 't'; break;
            default:
                *p++ = str[i];
        }
    }
    *p++ = '"';
    *p = '\0';

    return escaped;
}

/* ============================================
 * Connection Management
 * ============================================ */

AlyodcliClient *alyodcli_connect(const AlyodcliConnOpts *opts) {
    if (!opts) return NULL;

    _alyodcli_init_winsock();

    AlyodcliClient *client = (AlyodcliClient *)calloc(1, sizeof(AlyodcliClient));
    if (!client) return NULL;

    client->type = opts->type;
    client->timeout_ms = opts->timeout_ms > 0 ? opts->timeout_ms : 5000;

    if (opts->type == ALYODCLI_TCP) {
        client->socket = socket(AF_INET, SOCK_STREAM, 0);
        if (client->socket == INVALID_SOCKET) {
            free(client);
            return NULL;
        }

        struct sockaddr_in addr;
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(opts->port);
        inet_pton(AF_INET, opts->host ? opts->host : "127.0.0.1", &addr.sin_addr);

        if (connect(client->socket, (struct sockaddr *)&addr, sizeof(addr)) == SOCKET_ERROR) {
            closesocket(client->socket);
            free(client);
            return NULL;
        }
    } else if (opts->type == ALYODCLI_UNIX) {
#ifdef _WIN32
        free(client);
        return NULL;  /* Unix sockets not supported on Windows */
#else
        client->socket = socket(AF_UNIX, SOCK_STREAM, 0);
        if (client->socket == INVALID_SOCKET) {
            free(client);
            return NULL;
        }

        struct sockaddr_un addr;
        memset(&addr, 0, sizeof(addr));
        addr.sun_family = AF_UNIX;
        strncpy(addr.sun_path, opts->unix_path, sizeof(addr.sun_path) - 1);

        if (connect(client->socket, (struct sockaddr *)&addr, sizeof(addr)) == SOCKET_ERROR) {
            closesocket(client->socket);
            free(client);
            return NULL;
        }
#endif
    }

    return client;
}

AlyodcliClient *alyodcli_connect_tcp(const char *host, uint16_t port) {
    AlyodcliConnOpts opts = {
        .type = ALYODCLI_TCP,
        .host = host ? host : "127.0.0.1",
        .port = port,
        .timeout_ms = 5000
    };
    return alyodcli_connect(&opts);
}

AlyodcliClient *alyodcli_connect_unix(const char *socket_path) {
#ifdef _WIN32
    return NULL;
#else
    AlyodcliConnOpts opts = {
        .type = ALYODCLI_UNIX,
        .unix_path = socket_path,
        .timeout_ms = 5000
    };
    return alyodcli_connect(&opts);
#endif
}

void alyodcli_disconnect(AlyodcliClient *client) {
    if (!client) return;
    if (client->socket != INVALID_SOCKET) {
        closesocket(client->socket);
    }
    if (client->unix_path) free(client->unix_path);
    free(client);
}

/* ============================================
 * Style Functions
 * ============================================ */

AlyodcliResponse alyodcli_paint(AlyodcliClient *client, const char *text,
                                const char **styles, int num_styles) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *text_escaped = _alyodcli_escape_json_string(text);

    strcpy(json_buf, "[");
    strcat(json_buf, text_escaped);

    for (int i = 0; i < num_styles; i++) {
        strcat(json_buf, ",");
        char *style_escaped = _alyodcli_escape_json_string(styles[i]);
        strcat(json_buf, style_escaped);
        free(style_escaped);
    }
    strcat(json_buf, "]");

    free(text_escaped);
    return _alyodcli_json_rpc_call(client, "paint", json_buf);
}

AlyodcliResponse alyodcli_style_get(AlyodcliClient *client, const char *name) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *name_escaped = _alyodcli_escape_json_string(name);
    snprintf(json_buf, sizeof(json_buf), "[\"%s\"]", name_escaped);
    free(name_escaped);
    return _alyodcli_json_rpc_call(client, "style_get", json_buf);
}

AlyodcliResponse alyodcli_style_ext(AlyodcliClient *client, int color_index, int background) {
    char json_buf[ALYODCLI_MAX_JSON];
    snprintf(json_buf, sizeof(json_buf), "[%d, %s]", color_index, background ? "true" : "false");
    return _alyodcli_json_rpc_call(client, "style_ext", json_buf);
}

AlyodcliResponse alyodcli_style_hex(AlyodcliClient *client, const char *hex_code, int background) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *hex_escaped = _alyodcli_escape_json_string(hex_code);
    snprintf(json_buf, sizeof(json_buf), "[\"%s\", %s]", hex_escaped, background ? "true" : "false");
    free(hex_escaped);
    return _alyodcli_json_rpc_call(client, "style_hex", json_buf);
}

/* ============================================
 * Text Functions
 * ============================================ */

AlyodcliResponse alyodcli_text_visual_len(AlyodcliClient *client, const char *text) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *text_escaped = _alyodcli_escape_json_string(text);
    snprintf(json_buf, sizeof(json_buf), "[%s]", text_escaped);
    free(text_escaped);
    return _alyodcli_json_rpc_call(client, "text_visual_len", json_buf);
}

AlyodcliResponse alyodcli_text_align(AlyodcliClient *client, const char *text,
                                     int width, const char *align,
                                     const char **styles, int num_styles) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *text_escaped = _alyodcli_escape_json_string(text);
    char *align_escaped = _alyodcli_escape_json_string(align);

    strcpy(json_buf, "[");
    strcat(json_buf, text_escaped);
    strcat(json_buf, ",");
    strcat(json_buf, align_escaped);

    for (int i = 0; i < num_styles; i++) {
        strcat(json_buf, ",");
        char *style_escaped = _alyodcli_escape_json_string(styles[i]);
        strcat(json_buf, style_escaped);
        free(style_escaped);
    }
    strcat(json_buf, "]");

    free(text_escaped);
    free(align_escaped);
    return _alyodcli_json_rpc_call(client, "text_align", json_buf);
}

/* ============================================
 * Layout Functions
 * ============================================ */

AlyodcliResponse alyodcli_layout_box(AlyodcliClient *client, const char *content,
                                     int width, const char *align, const char *color) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *content_escaped = _alyodcli_escape_json_string(content);
    char *align_escaped = _alyodcli_escape_json_string(align);
    char *color_escaped = _alyodcli_escape_json_string(color);

    snprintf(json_buf, sizeof(json_buf),
             "[%s, {\"width\": %d, \"align\": %s, \"color\": %s}]",
             content_escaped, width, align_escaped, color_escaped);

    free(content_escaped);
    free(align_escaped);
    free(color_escaped);
    return _alyodcli_json_rpc_call(client, "layout_box", json_buf);
}

AlyodcliResponse alyodcli_layout_table(AlyodcliClient *client, const char *json_data,
                                       const char *header_color, const char *border_color) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *header_escaped = _alyodcli_escape_json_string(header_color);
    char *border_escaped = _alyodcli_escape_json_string(border_color);

    snprintf(json_buf, sizeof(json_buf),
             "[%s, {\"header_color\": %s, \"border_color\": %s}]",
             json_data, header_escaped, border_escaped);

    free(header_escaped);
    free(border_escaped);
    return _alyodcli_json_rpc_call(client, "layout_table", json_buf);
}

/* ============================================
 * Widget Functions
 * ============================================ */

AlyodcliResponse alyodcli_widgets_hr(AlyodcliClient *client, int width,
                                     const char *character, const char *color) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *char_escaped = _alyodcli_escape_json_string(character);
    char *color_escaped = _alyodcli_escape_json_string(color);

    snprintf(json_buf, sizeof(json_buf),
             "[{\"width\": %d, \"char\": %s, \"color\": %s}]",
             width, char_escaped, color_escaped);

    free(char_escaped);
    free(color_escaped);
    return _alyodcli_json_rpc_call(client, "widgets_hr", json_buf);
}

AlyodcliResponse alyodcli_widgets_bullet(AlyodcliClient *client, const char *text,
                                         const char *character, const char *color,
                                         int indent) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *text_escaped = _alyodcli_escape_json_string(text);
    char *char_escaped = _alyodcli_escape_json_string(character);
    char *color_escaped = _alyodcli_escape_json_string(color);

    snprintf(json_buf, sizeof(json_buf),
             "[%s, {\"char\": %s, \"color\": %s, \"indent\": %d}]",
             text_escaped, char_escaped, color_escaped, indent);

    free(text_escaped);
    free(char_escaped);
    free(color_escaped);
    return _alyodcli_json_rpc_call(client, "widgets_bullet", json_buf);
}

AlyodcliResponse alyodcli_widgets_progress(AlyodcliClient *client, int iteration,
                                          int total, const char *prefix,
                                          int length, const char *color) {
    char json_buf[ALYODCLI_MAX_JSON];
    char *prefix_escaped = _alyodcli_escape_json_string(prefix);
    char *color_escaped = _alyodcli_escape_json_string(color);

    snprintf(json_buf, sizeof(json_buf),
             "[%d, %d, %s, {\"length\": %d, \"color\": %s}]",
             iteration, total, prefix_escaped, length, color_escaped);

    free(prefix_escaped);
    free(color_escaped);
    return _alyodcli_json_rpc_call(client, "widgets_progress", json_buf);
}

/* ============================================
 * Utility Functions
 * ============================================ */

AlyodcliResponse alyodcli_help(AlyodcliClient *client, const char *topic) {
    char json_buf[256];
    char *topic_escaped = _alyodcli_escape_json_string(topic);
    snprintf(json_buf, sizeof(json_buf), "[%s]", topic_escaped);
    free(topic_escaped);
    return _alyodcli_json_rpc_call(client, "help", json_buf);
}

void alyodcli_response_free(AlyodcliResponse *resp) {
    if (!resp) return;
    if (resp->result) free(resp->result);
    if (resp->error_msg) free(resp->error_msg);
}

int alyodcli_response_ok(const AlyodcliResponse *resp) {
    return resp && resp->success;
}

const char *alyodcli_response_error(const AlyodcliResponse *resp) {
    return resp ? resp->error_msg : "Unknown error";
}

const char *alyodcli_response_result(const AlyodcliResponse *resp) {
    return resp ? resp->result : NULL;
}
