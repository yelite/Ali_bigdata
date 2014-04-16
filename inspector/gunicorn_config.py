#coding=utf-8
bind = '0.0.0.0:8083'
backlog = 2048

workers = 2
worker_class = 'gevent'
worker_connections = 1000
timeout = 15
keepalive = 2

debug = False
spew = False

daemon = True
pidfile = 'inspector.pid'
user = 'yelite'

errorlog = 'log/error.log'
loglevel = 'info'
accesslog = 'log/access.log'


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spwawning workers")


def worker_int(worker):
    worker.log.info("worker received INT or TERM signal")

    ## get traceback info
    import threading, sys, traceback

    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""),
                                            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                                                        lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))