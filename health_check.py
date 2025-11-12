from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health_data = {
                "status": "healthy",
                "timestamp": time.time(),
                "service": "SSOD Detection App"
            }
            
            self.wsgi_write(json.dumps(health_data))
        else:
            self.send_response(404)
            self.end_headers()
    
    def wsgi_write(self, content):
        self.wfile.write(content.encode('utf-8'))

def start_health_check_server(port=8081):
    """Start a simple health check server on a separate thread"""
    try:
        server = HTTPServer(('localhost', port), HealthCheckHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        print(f"Health check server started on port {port}")
        return server
    except Exception as e:
        print(f"Failed to start health check server: {e}")
        return None

if __name__ == "__main__":
    server = start_health_check_server()
    if server:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.shutdown()