#!/usr/bin/env python3
"""
Single Page Application (SPA) HTTP Server
Serves index.html for all non-file routes to support client-side routing
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class SPAHandler(SimpleHTTPRequestHandler):
    """HTTP request handler that supports SPA routing"""
    
    def do_GET(self):
        """Handle GET requests with SPA fallback"""
        # Get the path
        path = self.path.split('?')[0]  # Remove query parameters
        
        # If the path doesn't have a file extension and isn't a known API path
        if not '.' in path.split('/')[-1] and not path.startswith('/api'):
            # Check if the file exists
            file_path = Path(self.translate_path(path))
            if not file_path.is_file():
                # Serve index.html for SPA routing
                self.path = '/index.html'
        
        # Call parent class to handle the request
        super().do_GET()
    
    def end_headers(self):
        """Add headers to prevent caching"""
        # Disable caching for HTML files
        if self.path.endswith('.html') or '.' not in self.path.split('/')[-1]:
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Log requests in a cleaner format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    # Change to frontend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Server configuration
    HOST = '0.0.0.0'
    PORT = 3000
    
    # Create server
    server = HTTPServer((HOST, PORT), SPAHandler)
    
    print(f"🚀 SPA Server running on http://localhost:{PORT}")
    print(f"📁 Serving files from: {os.getcwd()}")
    print(f"Press Ctrl+C to stop\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)
