from src.dns_server import DNSServer
from src.http_server import app

if __name__ == '__main__':
    dns_server = DNSServer()
    dns_server.start()

    app.run(host='0.0.0.0', port=80, debug=False)

