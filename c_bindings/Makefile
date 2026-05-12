# Makefile for ALYODCLI C Client
# Usage: make or make all

CC = gcc
CFLAGS = -Wall -Wextra -O3 -std=c99
LDFLAGS = 

# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    LDFLAGS += -lm
endif
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -lm
endif
ifeq ($(OS),Windows_NT)
    LDFLAGS += -lws2_32
    EXE_EXT = .exe
endif

# Files
SOURCES = alyodcli.c
HEADERS = alyodcli.h
LIB = libalyodcli.a
EXAMPLE_PROG = example_client$(EXE_EXT)
EXAMPLE_SRC = example_client.c

# Default target
.PHONY: all
all: $(LIB) $(EXAMPLE_PROG)

# Build static library
$(LIB): $(SOURCES) $(HEADERS)
	@echo "Building static library..."
	$(CC) $(CFLAGS) -c $(SOURCES) -o alyodcli.o
	ar rcs $(LIB) alyodcli.o
	@echo "✓ $(LIB) created"

# Build example program
$(EXAMPLE_PROG): $(EXAMPLE_SRC) $(LIB) $(HEADERS)
	@echo "Building example program..."
	$(CC) $(CFLAGS) $(EXAMPLE_SRC) $(LIB) -o $(EXAMPLE_PROG) $(LDFLAGS)
	@echo "✓ $(EXAMPLE_PROG) created"

# Build shared library (optional)
.PHONY: shared
shared: $(SOURCES) $(HEADERS)
	@echo "Building shared library..."
ifeq ($(OS),Windows_NT)
	$(CC) $(CFLAGS) -shared -o alyodcli.dll $(SOURCES) $(LDFLAGS)
	@echo "✓ alyodcli.dll created"
else
	$(CC) $(CFLAGS) -fPIC -shared -o libalyodcli.so $(SOURCES) $(LDFLAGS)
	@echo "✓ libalyodcli.so created"
endif

# Run example
.PHONY: run
run: $(EXAMPLE_PROG)
	@echo "Running example (make sure alyodcli-server is running)..."
	@echo ""
	./$(EXAMPLE_PROG)

# Clean
.PHONY: clean
clean:
	@echo "Cleaning build files..."
	rm -f *.o $(LIB) $(EXAMPLE_PROG) libalyodcli.so alyodcli.dll
	@echo "✓ Clean complete"

# Install (Unix/Linux)
.PHONY: install
install: $(LIB) $(HEADERS)
	@echo "Installing ALYODCLI C library..."
	install -d /usr/local/include
	install -m 644 $(HEADERS) /usr/local/include/
	install -d /usr/local/lib
	install -m 644 $(LIB) /usr/local/lib/
	@echo "✓ Installation complete"
	@echo "  Headers: /usr/local/include/$(HEADERS)"
	@echo "  Library: /usr/local/lib/$(LIB)"

# Uninstall
.PHONY: uninstall
uninstall:
	@echo "Uninstalling ALYODCLI C library..."
	rm -f /usr/local/include/$(HEADERS)
	rm -f /usr/local/lib/$(LIB)
	@echo "✓ Uninstallation complete"

# Help
.PHONY: help
help:
	@echo "ALYODCLI C Client - Makefile targets:"
	@echo ""
	@echo "  make all       - Build static library and example program"
	@echo "  make shared    - Build shared library (libalyodcli.so / alyodcli.dll)"
	@echo "  make run       - Run example program"
	@echo "  make clean     - Remove build files"
	@echo "  make install   - Install library system-wide (Unix/Linux)"
	@echo "  make uninstall - Uninstall library"
	@echo "  make help      - Show this help message"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Start ALYODCLI server: alyodcli-server --host 127.0.0.1 --port 5555"
	@echo "  2. Build and run example: make run"
	@echo ""

.PHONY: status
status:
	@echo "ALYODCLI C Client Build Status"
	@echo "==============================="
	@echo "Platform: $(UNAME_S)"
	@echo "Compiler: $(CC)"
	@echo "Flags: $(CFLAGS)"
	@echo "Linker flags: $(LDFLAGS)"
	@echo ""
	@echo "Files:"
	@echo "  Source: $(SOURCES)"
	@echo "  Headers: $(HEADERS)"
	@echo "  Library: $(LIB)"
	@echo "  Example: $(EXAMPLE_SRC) -> $(EXAMPLE_PROG)"
	@echo ""

# Info
.PHONY: info
info: status help

.DEFAULT_GOAL := help
