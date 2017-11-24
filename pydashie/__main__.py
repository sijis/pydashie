import socketserver

from .app import app, run
from .utils.xyzzy import xyzzy
from .routes import close_stream


def run_app():
    socketserver.BaseServer.handle_error = close_stream
    run(app, xyzzy)


if __name__ == "__main__":
    run_app()
