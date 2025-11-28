import http.server
import socketserver

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
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print("\n\n\u2554" + "\u2550"*42 + "\u2557")
        print("\u2551   StartHub Frontend Server Started      \u2551")
        print("\u255A" + "\u2550"*42 + "\u255D\n")
        print(f"\U0001F30D Server running at: http://localhost:{PORT}")
        print("\ud83d\udd17 Backend API at: http://localhost:8081\n")
        print("Pages available:")
        print(f"  • http://localhost:{PORT}/home.html")
        print(f"  • http://localhost:{PORT}/login.html")
        print(f"  • http://localhost:{PORT}/signup.html")
        print(f"  • http://localhost:{PORT}/profile.html\n")
        print("Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✋ Server stopped")