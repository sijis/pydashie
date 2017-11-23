class Z:
    pass


xyzzy = Z()
xyzzy.events_queue = {}
xyzzy.last_events = {}
xyzzy.using_events = True
xyzzy.MAX_QUEUE_LENGTH = 20
xyzzy.stopped = False
