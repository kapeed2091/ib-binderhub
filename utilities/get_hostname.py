def get_hostname():
    import socket
    hostname = socket.gethostname()
    return hostname.strip('Jupyter-')
