import queue

from .routes import *


class Z:
    pass

xyzzy = Z()
xyzzy.events_queue = {}
xyzzy.last_events = {}
xyzzy.using_events = True
xyzzy.MAX_QUEUE_LENGTH = 20
xyzzy.stopped = False

@app.route('/events')
def events():
    if xyzzy.using_events:
        event_stream_port = request.environ['REMOTE_PORT']
        current_event_queue = queue.Queue()
        xyzzy.events_queue[event_stream_port] = current_event_queue
        current_app.logger.info('New Client %s connected. Total Clients: %s' %
                                (event_stream_port, len(xyzzy.events_queue)))

        #Start the newly connected client off by pushing the current last events
        for event in xyzzy.last_events.values():
            current_event_queue.put(event)
        return Response(pop_queue(current_event_queue), mimetype='text/event-stream')

    return response(xyzzy.last_events.values(), mimetype='text/event-stream')

def pop_queue(current_event_queue):
    while not xyzzy.stopped:
        try:
            data = current_event_queue.get(timeout=0.1)
            yield data
        except queue.Empty:
            #this makes the server quit nicely - previously the queue threads would block and never exit. This makes it keep checking for dead application
            pass

def purge_streams():
    big_queues = [port for port, queue in xyzzy.events_queue if len(queue) > xyzzy.MAX_QUEUE_LENGTH]
    for big_queue in big_queues:
        current_app.logger.info('Client %s is stale. Disconnecting. Total Clients: %s' %
                                (big_queue, len(xyzzy.events_queue)))
        del queue[big_queue]

def close_stream(*args, **kwargs):
    event_stream_port = args[2][1]
    del xyzzy.events_queue[event_stream_port]
    log.info('Client %s disconnected. Total Clients: %s' % (event_stream_port, len(xyzzy.events_queue)))


def run_sample_app():
    import socketserver
    socketserver.BaseServer.handle_error = close_stream
    from .example_app import run
    run(app, xyzzy)


if __name__ == "__main__":
    run_sample_app()
