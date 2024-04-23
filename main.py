# -*- coding: utf-8 -*-
# Mock data server,used for clients.
import os
import socket
import tornado.web
import tornado.websocket
import tornado.netutil
import tornado.httpserver
import tornado.ioloop
import flutterData, rnGameCenter, uploadFile, princeSpa, testPage
from tornado.httpserver import HTTPServer
from tornado.process import fork_processes

current_path = os.path.dirname(__file__)
port = 9999

settings = {
    "template_path": os.path.join(current_path, "template"),
    "static_path": os.path.join(current_path, "static"),
    # "static_url_prefix":"/static/",
    "debug": True,
    "cookie_secret": "__TODO:LIU_ZHAN_WEI"
}


class BaseHandler(tornado.web.StaticFileHandler):
    def write_error(self, status_code, **kwargs):
        self.finish({
            'error': {
                'code': status_code,
                'message': self._reason,
            }
        })


def get_host_ip():
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def create_server():
    return tornado.web.Application([
        (r"/test", testPage.IndexHandler),
        (r"/test/user", testPage.UserHandler),
        (r"/socket/test", testPage.WebSocketHandler),
        (r"/prince", princeSpa.princeIndex),
        (r"^/prince/mock.+", princeSpa.princeMockMsg),
        (r"/dy/getHourRank", princeSpa.getRankList),
        (r"/socket/dy/flutter", flutterData.dyFlutterSocket),
        (r"^/dy/flutter.+", flutterData.dyFlutter),
        (r"^/dy/rn/gameCenter.+.+", rnGameCenter.dyReactNativeGameCenter),
        (r"/upload", uploadFile.upload),
        (r"/(.*)", BaseHandler,
         {
             "path": os.path.join(current_path, "flutter_web_bundle"),
             "default_filename": "index.html"
         }
         ),
    ], **settings)


if __name__ == "__main__":
    app = create_server()
    # app.listen(port)

    sockets = tornado.netutil.bind_sockets(port)

    proc_num = fork_processes(0)

    if proc_num == 0:  # 子进程
        server = HTTPServer(app)
        server.add_sockets(sockets)
        print('address -> ' + get_host_ip() + ':' + str(port))
        print('tornado start.')
        tornado.ioloop.IOLoop.current().start()






