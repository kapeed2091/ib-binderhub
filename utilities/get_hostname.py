def get_hostname():
    import socket
    hostname = socker.gethostname()
    return hostname.strip('Jupyter-')
