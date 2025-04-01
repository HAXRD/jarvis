import os
import asyncio
import signal
import logging
from tornado.web import Application
from tornado.ioloop import IOLoop
import tornado.options

from handlers.websocket_handler import ChatWebSocketHandler
from handlers.health_handler import HealthHandler
from config import get_config

def make_app(config):
    """Create the Tornado application"""
    return Application([
        (r"/ws/chat", ChatWebSocketHandler),
        (r"/health", HealthHandler),
    ],
    debug=config.DEBUG,
    websocket_ping_interval=30)

async def shutdown(signal, loop):
    """Graceful shutdown of the server"""
    logging.info(f"Received exit signal {signal.name}...")

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    logging.info(f"Cancelling {len(tasks)} outstanding tasks")

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    logging.info("Shutdown complete")

def setup_shutdown_handlers():
    """Set up signal handlers for graceful shutdown."""
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)

    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.create_task(shutdown(s, loop))
        )

def main():
    """Start the Tornado server."""
    tornado.options.parse_command_line()

    config = get_config()
    app = make_app(config)

    port = int(os.environ.get("PORT", 8888))
    app.listen(port)

    logging.info(f"Tornado server started on port {port}")

    setup_shutdown_handlers()
    IOLoop.current().start()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()