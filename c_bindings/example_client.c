/*
 * Example C Program using ALYODCLI Client Library
 * 
 * Compile:
 *   gcc -o example_client example_client.c alyodcli.c -lws2_32 (Windows)
 *   gcc -o example_client example_client.c alyodcli.c (Unix/Linux)
 */

#include "alyodcli.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    printf("=== ALYODCLI C Client Example ===\n\n");

    /* Connect to ALYODCLI server (assumes it's running on localhost:5555) */
    printf("Connecting to ALYODCLI server at 127.0.0.1:5555...\n");
    AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);

    if (!client) {
        fprintf(stderr, "Failed to connect to ALYODCLI server.\n");
        fprintf(stderr, "Make sure to start the server first:\n");
        fprintf(stderr, "  python -m ALYODCLI.c_server --host 127.0.0.1 --port 5555\n");
        return 1;
    }

    printf("Connected successfully!\n\n");

    /* ============================================
     * Example 1: Paint text with styles
     * ============================================ */
    {
        printf("Example 1: Applying styles to text\n");
        printf("-----------------------------------\n");

        const char *styles[] = {"cyan", "bold"};
        AlyodcliResponse resp = alyodcli_paint(client, "Hello, ALYODCLI!", styles, 2);

        if (alyodcli_response_ok(&resp)) {
            printf("Result: %s\n\n", alyodcli_response_result(&resp));
        } else {
            fprintf(stderr, "Error: %s\n\n", alyodcli_response_error(&resp));
        }

        alyodcli_response_free(&resp);
    }

    /* ============================================
     * Example 2: Get visual text length
     * ============================================ */
    {
        printf("Example 2: Calculate visual text length\n");
        printf("-----------------------------------\n");

        AlyodcliResponse resp = alyodcli_text_visual_len(client, "Test 😀 String");

        if (alyodcli_response_ok(&resp)) {
            printf("Visual length: %s\n\n", alyodcli_response_result(&resp));
        } else {
            fprintf(stderr, "Error: %s\n\n", alyodcli_response_error(&resp));
        }

        alyodcli_response_free(&resp);
    }

    /* ============================================
     * Example 3: Align text
     * ============================================ */
    {
        printf("Example 3: Align text\n");
        printf("-----------------------------------\n");

        const char *styles[] = {"yellow"};
        AlyodcliResponse resp = alyodcli_text_align(client, "Centered", 40, "center", styles, 1);

        if (alyodcli_response_ok(&resp)) {
            printf("Aligned text:\n%s\n\n", alyodcli_response_result(&resp));
        } else {
            fprintf(stderr, "Error: %s\n\n", alyodcli_response_error(&resp));
        }

        alyodcli_response_free(&resp);
    }

    /* ============================================
     * Example 4: Get color codes
     * ============================================ */
    {
        printf("Example 4: Get standard ANSI color codes\n");
        printf("-----------------------------------\n");

        AlyodcliResponse resp = alyodcli_style_get(client, "red");

        if (alyodcli_response_ok(&resp)) {
            printf("Red color code: %s (hex: %s)\n\n", 
                   alyodcli_response_result(&resp), 
                   alyodcli_response_result(&resp));
        } else {
            fprintf(stderr, "Error: %s\n\n", alyodcli_response_error(&resp));
        }

        alyodcli_response_free(&resp);
    }

    /* ============================================
     * Example 5: Get hex color code
     * ============================================ */
    {
        printf("Example 5: Convert hex color to ANSI code\n");
        printf("-----------------------------------\n");

        AlyodcliResponse resp = alyodcli_style_hex(client, "#ff6b6b", 0);

        if (alyodcli_response_ok(&resp)) {
            printf("Hex color (#ff6b6b) ANSI code:\n%s\n\n", alyodcli_response_result(&resp));
        } else {
            fprintf(stderr, "Error: %s\n\n", alyodcli_response_error(&resp));
        }

        alyodcli_response_free(&resp);
    }

    /* ============================================
     * Example 6: Draw a horizontal rule
     * ============================================ */
    {
        printf("Example 6: Draw horizontal rule\n");
        printf("-----------------------------------\n");

        AlyodcliResponse resp = alyodcli_widgets_hr(client, 50, "═", "green");

        if (alyodcli_response_ok(&resp)) {
            printf("Horizontal rule:\n%s\n\n", alyodcli_response_result(&resp));
        } else {
            fprintf(stderr, "Error: %s\n\n", alyodcli_response_error(&resp));
        }

        alyodcli_response_free(&resp);
    }

    /* ============================================
     * Example 7: Print bullet points
     * ============================================ */
    {
        printf("Example 7: Print bullet points\n");
        printf("-----------------------------------\n");

        AlyodcliResponse resp = alyodcli_widgets_bullet(client, "First item", "•", "cyan", 0);
        if (alyodcli_response_ok(&resp)) {
            printf("Bullet:\n%s\n\n", alyodcli_response_result(&resp));
        }
        alyodcli_response_free(&resp);
    }

    /* ============================================
     * Example 8: Get help
     * ============================================ */
    {
        printf("Example 8: Get help\n");
        printf("-----------------------------------\n");

        AlyodcliResponse resp = alyodcli_help(client, "all");

        if (alyodcli_response_ok(&resp)) {
            const char *help_text = alyodcli_response_result(&resp);
            if (help_text && strlen(help_text) > 200) {
                printf("Help (first 200 chars):\n%.200s...\n\n", help_text);
            } else {
                printf("Help:\n%s\n\n", help_text);
            }
        } else {
            fprintf(stderr, "Error: %s\n\n", alyodcli_response_error(&resp));
        }

        alyodcli_response_free(&resp);
    }

    /* Clean up */
    printf("=== Example Complete ===\n");
    alyodcli_disconnect(client);

    return 0;
}
