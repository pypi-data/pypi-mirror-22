# -*- coding: utf-8 -*-

# by @yxwzaxns, @pandolia

import sys, os
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if p not in sys.path:
    sys.path.insert(0, p)

import os, flask, time, logging

from qqbot.common import StartDaemonThread
from qqbot.utf8logger import INFO

class QrcodeServer(object):
    def __init__(self, ip, port, tmpDir):
        self.ip = ip
        self.port = int(port)
        self.tmpDir = os.path.abspath(tmpDir)
        self.qrcodeURL = 'http://%s:%s/' % (ip, port)
        StartDaemonThread(self.run)
        time.sleep(0.5)
        INFO('二维码 HTTP 服务器已在子线程中开启')
    
    def QrcodeURL(self, qrcodeId):
        self.qrcodeId = qrcodeId
        return self.qrcodeURL + qrcodeId
    
    def run(self):
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        app = flask.Flask(__name__)
        app.route('/<randcode>')(self.route_qrcode)
        app.run(host=self.ip, port=self.port, debug=False)
    
    def route_qrcode(self, randcode):
        lastfile = os.path.join(self.tmpDir, self.qrcodeId+'.png')
        # INFO(lastfile)
        if os.path.exists(lastfile):
            return flask.send_file(lastfile, mimetype='image/png')
        else:
            flask.abort(404)

    # def route_qrcode(self):        
    #     last, lastfile = 0, ''
    #     for f in os.listdir(self.tmpDir):
    #         if f.endswith('.png'):
    #             p = os.path.join(self.tmpDir, f)
    #             cur = os.path.getmtime(p)
    #             if cur > last:
    #                 last = cur
    #                 lastfile = p 
    # 
    #     if lastfile:
    #         return flask.send_file(lastfile, mimetype='image/png')
    #     else:
    #         flask.abort(404)

if __name__ == '__main__':
    QrcodeServer('127.0.0.1', 8189, '.')
    while True:
        time.sleep(100)
