"""
Socket server for C program integration.
Allows C programs to communicate with ALYODCLI via TCP or Unix sockets.

Protocol: JSON-RPC 2.0 over socket
"""

import socket
import json
import threading
import sys
import os
from typing import Any, Dict, Callable
import argparse

from ALYODCLI import Activate

class AlyodcliSocketServer:
    """Socket server for ALYODCLI C integration."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 5555, unix_socket: str = None):
        self.host = host
        self.port = port
        self.unix_socket = unix_socket
        self.cli = Activate()
        self.server_socket = None
        self.running = False
        
        # Map method names to callable functions
        self.methods: Dict[str, Callable] = {
            "paint": self.cli.paint,
            "style_get": self.cli.style.get,
            "style_ext": self.cli.style.ext,
            "style_hex": self.cli.style.hex,
            "text_align": self.cli.text.align,
            "text_visual_len": self.cli.text.get_visual_len,
            "layout_box": self.layout_box_wrapper,
            "layout_table": self.layout_table_wrapper,
            "widgets_hr": self.cli.widgets.hr,
            "widgets_bullet": self.cli.widgets.bullet,
            "widgets_progress": self.cli.widgets.progress,
            "help": self.cli.help,
        }
    
    def layout_box_wrapper(self, content, **kwargs):
        """Wrapper for layout.box that returns string instead of printing."""
        return self.cli.layout.box(content, **kwargs)
    
    def layout_table_wrapper(self, data, **kwargs):
        """Wrapper for layout.table that returns string instead of printing."""
        return self.cli.layout.table(data, **kwargs)
    
    def handle_json_rpc(self, request: str) -> str:
        """
        Handle JSON-RPC 2.0 request.
        
        Format:
        {
            "jsonrpc": "2.0",
            "method": "paint",
            "params": ["Hello", "cyan", "bold"],
            "id": 1
        }
        """
        try:
            req = json.loads(request)
            
            # Validate JSON-RPC 2.0
            if req.get("jsonrpc") != "2.0":
                return self._error_response(None, -32600, "Invalid JSON-RPC version")
            
            method_name = req.get("method")
            params = req.get("params", [])
            req_id = req.get("id")
            
            if not method_name or method_name not in self.methods:
                return self._error_response(req_id, -32601, f"Method not found: {method_name}")
            
            # Call the method
            if isinstance(params, list):
                result = self.methods[method_name](*params)
            elif isinstance(params, dict):
                result = self.methods[method_name](**params)
            else:
                return self._error_response(req_id, -32602, "Invalid params")
            
            # Return successful response
            return json.dumps({
                "jsonrpc": "2.0",
                "result": result,
                "id": req_id
            })
        
        except json.JSONDecodeError:
            return self._error_response(None, -32700, "Parse error")
        except Exception as e:
            return self._error_response(None, -32000, f"Server error: {str(e)}")
    
    def _error_response(self, req_id: Any, code: int, message: str) -> str:
        """Generate JSON-RPC 2.0 error response."""
        return json.dumps({
            "jsonrpc": "2.0",
            "error": {"code": code, "message": message},
            "id": req_id
        })
    
    def handle_client(self, client_socket: socket.socket, addr: tuple):
        """Handle a single client connection."""
        try:
            # Receive request (up to 64KB)
            request_data = b""
            while len(request_data) < 65536:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                request_data += chunk
                
                # Check for complete message (newline-terminated)
                if b'\n' in request_data:
                    break
            
            request_str = request_data.decode('utf-8').strip()
            
            # Process request
            response = self.handle_json_rpc(request_str)
            
            # Send response
            client_socket.sendall((response + "\n").encode('utf-8'))
        
        except Exception as e:
            error_response = json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": f"Connection error: {str(e)}"}
            })
            try:
                client_socket.sendall((error_response + "\n").encode('utf-8'))
            except:
                pass
        
        finally:
            client_socket.close()
    
    def start_tcp(self):
        """Start TCP socket server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        print(f"[ALYODCLI] Socket server listening on {self.host}:{self.port}")
        self.running = True
        
        try:
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                    thread.daemon = True
                    thread.start()
                except KeyboardInterrupt:
                    break
        
        finally:
            self.shutdown()
    
    def start_unix(self):
        """Start Unix domain socket server (Unix/Linux only)."""
        if sys.platform == "win32":
            print("[ERROR] Unix sockets not supported on Windows")
            return
        
        # Remove socket file if it exists
        if os.path.exists(self.unix_socket):
            os.remove(self.unix_socket)
        
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_socket.bind(self.unix_socket)
        self.server_socket.listen(5)
        
        print(f"[ALYODCLI] Unix socket server listening on {self.unix_socket}")
        self.running = True
        
        try:
            while self.running:
                try:
                    client_socket, _ = self.server_socket.accept()
                    thread = threading.Thread(target=self.handle_client, args=(client_socket, None))
                    thread.daemon = True
                    thread.start()
                except KeyboardInterrupt:
                    break
        
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown the server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        
        if self.unix_socket and os.path.exists(self.unix_socket):
            os.remove(self.unix_socket)
        
        print("[ALYODCLI] Server shutdown")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ALYODCLI Socket Server for C program integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  alyodcli-server --host 127.0.0.1 --port 5555     # TCP mode
  alyodcli-server --unix /tmp/alyodcli.sock         # Unix socket mode
        """
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="TCP host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5555,
        help="TCP port to bind to (default: 5555)"
    )
    parser.add_argument(
        "--unix",
        type=str,
        help="Unix socket path (enables Unix socket mode)"
    )
    parser.add_argument(
        "--daemonize",
        action="store_true",
        help="Run as background daemon"
    )
    
    args = parser.parse_args()
    
    server = AlyodcliSocketServer(
        host=args.host,
        port=args.port,
        unix_socket=args.unix
    )
    
    if args.unix:
        server.start_unix()
    else:
        server.start_tcp()

if __name__ == "__main__":
    main()
