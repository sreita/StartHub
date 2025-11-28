#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StartHub Frontend Development Server
Serves static files with CORS headers enabled
"""

import http.server
import socketserver
import sys
import io
import os

PORT = 3000

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, 'ok')
        self.end_headers()

if __name__ == "__main__":
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # Change to frontend directory to serve files from there
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    frontend_dir = os.path.join(project_root, 'frontend')
    os.chdir(frontend_dir)
    
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print("\n\n" + "="*46)
        print("  StartHub Frontend Server Started")
        print("="*46 + "\n")
        print(f"Server running at: http://localhost:{PORT}")
        print(f"Serving files from: {frontend_dir}")
        print("Backend API at: http://localhost:8081\n")
        print("Pages available:")
        print(f"  - http://localhost:{PORT}/home.html")
        print(f"  - http://localhost:{PORT}/login.html")
        print(f"  - http://localhost:{PORT}/signup.html")
        print(f"  - http://localhost:{PORT}/profile.html\n")
        print("Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped")
