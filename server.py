#!/usr/bin/env python3
"""
Simple HTTP server for serving the Shroomy Sticker Editor static site.
Serves on port 5000 with proper cache control headers.
"""

import http.server
import socketserver
import os

PORT = 5000
DIRECTORY = "."

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with no-cache headers to prevent stale content."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        """Add cache control headers to all responses."""
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def run_server():
    """Start the HTTP server."""
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), NoCacheHTTPRequestHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"🍄 Shroomy Sticker Editor server running at http://0.0.0.0:{PORT}")
        print(f"📁 Serving directory: {os.path.abspath(DIRECTORY)}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    run_server()
