from mitmproxy.tools._main import mitmweb
def start_proxy():
    mitmweb(args=['-s', './app/api/data_getter/HttpProxy.py', '-p', '9000', '--web-port', '9020'])

start_proxy()