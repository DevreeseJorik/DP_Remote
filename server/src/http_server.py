from flask import Flask, Response, request
from flask_classful import FlaskView, route

from .payload_handler import PayloadHandler
from .http_helper import B64SCCrypto
from .loghandler import LogHandler
import logging

http_logging = LogHandler('http_server', 'network.log', level=logging.INFO).get_logger()
gts_logging = LogHandler('gts_server', 'network.log', level=logging.INFO).get_logger()

werkzeug_logging = logging.getLogger('werkzeug')
werkzeug_logging.setLevel(logging.ERROR)

AUTH_TOKEN = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'

class GTSResponse(Response):
    def __init__(self, response=None, status=None, headers=None, content_type=None, **kwargs):
        default_headers = {
            "Server": "Microsoft-IIS/6.0",
            "P3P": "CP='NOI ADMa OUR STP'",
            "cluster-server": "aphexweb3",
            "X-Server-Name": "AW4",
            "X-Powered-By": "ASP.NET",
            "Content-Type": "text/html",
            "Set-Cookie": "ASPSESSIONIDQCDBDDQS=JFDOAMPAGACBDMLNLFBCCNCI; path=/",
            "Cache-control": "private"
        }

        if headers:
            headers.update(default_headers)
        else:
            headers = default_headers

        super().__init__(response, status, headers, content_type, **kwargs)

app = Flask(__name__)

@app.before_request
def handle_request():
    if request.url_rule is None:
        http_logging.warning(f"No route found for {request.url}")
        return None
    gts_logging.info(f"Incoming Request: {request.url} {request.args.to_dict()}")
    if len(request.args.to_dict()) == 1:
        return GTSResponse(AUTH_TOKEN)

class GTSServer(FlaskView):
    route_base = '/pokemondpds/worldexchange'

    def __init__(self):
        self.token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'
        self.payload_handler = PayloadHandler()
        self.b64sc = B64SCCrypto()

    @route('/info.asp', methods=['GET'])
    def info(self):
        gts_logging.info('Connection Established.')
        return GTSResponse(b'\x01\x00')

    @route('/common/setProfile.asp', methods=['GET'])
    def set_profile(self):
        return GTSResponse(b'\x00' * 8)

    @route('/post.asp', methods=['GET'])
    def post(self):
        data = self.b64sc.decrypt(request.args.get('data'))
        gts_logging.info(f"POST data: {data.hex()}")
        self.payload_handler.handle_post(data)
        return GTSResponse(b'\x0c\x00')

    @route('/search.asp', methods=['GET'])
    def search(self):
        return GTSResponse(b'')

    @route('/result.asp', methods=['GET'])
    def result(self):
        payload = self.payload_handler.get_payload()
        return GTSResponse(payload)

    @route('/delete.asp', methods=['GET'])
    def delete(self):
        return GTSResponse(b'\x01\x00')

GTSServer.register(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
