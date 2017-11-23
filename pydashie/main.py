import socketserver

from .app import run
from .routes import *


def run_sample_app():
    socketserver.BaseServer.handle_error = close_stream
    run(app, xyzzy)


if __name__ == "__main__":
    run_sample_app()
