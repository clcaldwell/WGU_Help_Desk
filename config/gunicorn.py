# gunicorn configuration
def when_ready(server):
    """Gunicorn hook that runs when the server is ready"""
    open('/tmp/app-initialized', 'w').close()

bind = 'unix:///tmp/nginx.socket'
workers = 4