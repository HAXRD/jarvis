from tornado.web import RequestHandler
import json

class HealthHandler(RequestHandler):

    def get(self):
        """Return a health status."""
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({
            "status": "healthy",
            "service": "tornado_ws"
        }))