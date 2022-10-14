# Gunicorn config file.


bind = '...' # TODO: Path to socket
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'
