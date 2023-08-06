import logging
import os
from flask import Response
from .files_utils import directory_to_zipstream

logger = logging.getLogger('pydirl')


def stream_zipped_dir(path, zipname=None, exclude=None):
    if zipname is None:
        zipname = basename(path)
        if zipname:
            zipname += '.zip'
    z = directory_to_zipstream(path, exclude=exclude)
    response = Response(z, mimetype='application/zip')
    response.headers['Content-Disposition'] = 'attachment; filename="{0}"'.format(zipname)
    return response


def basename(path):
    """Returns the basename of this path

    /my/path/ -> path
    /my/path/. -> path
    """
    path = os.path.normpath(path)
    path = path.rstrip('/')
    return os.path.basename(path)


def init_loggers(logLevel=logging.WARNING, logNames=None):
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
    streamHandler.setFormatter(formatter)
    loggers = list(map(logging.getLogger, logNames))
    for logger in loggers:
        logger.setLevel(logLevel)
        if not logger.handlers:
            logger.addHandler(streamHandler)


def gevent_run(app, address, port, debugger=False, reloader=False):
    from gevent.wsgi import WSGIServer
    from werkzeug.debug import DebuggedApplication
    import gevent.monkey
    gevent.monkey.patch_all()

    run_app = app
    if debugger:
        run_app = DebuggedApplication(app)

    def run_server():
        import logging
        from gevent import version_info

        logger = logging.getLogger('pydirl')
        logger.info('Listening on http://{}:{}/'.format(address, port))
        server_params = dict()
        # starting from gevent version 1.1b1 we can pass custom logger to gevent
        if version_info[:2] >= (1, 1):
            server_params['log'] = logger
        http_server = WSGIServer((address, port), run_app, **server_params)
        http_server.serve_forever()

    if reloader:
        from werkzeug._reloader import run_with_reloader
        run_with_reloader(run_server)
    else:
        run_server()
