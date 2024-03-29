#!/usr/bin/python
import web,sys
import os
import urllib2
import base64
import binascii
from datetime import datetime
import calendar, time
import hashlib
import hmac
import sys
import random

urls = (
    '/record/(.*)', 'record'
    )
app = web.application(urls, globals())

# Developer specific parameters copy it from your vidyo.io dashboard
# https://developer.vidyo.io/dashboard

VIDYO_IO_DEVELOPER_KEY    = "your developer key"
VIDYO_IO_APPLICATION_ID   = "your application id"
TOKEN_VALID_DURATION_SECS = 600
EPOCH_SECONDS             = 62167219200

def getVidyoIOToken():
    type    = 'provision'
    key     = VIDYO_IO_DEVELOPER_KEY
    jid     = "recorder@" + VIDYO_IO_APPLICATION_ID
    expires = TOKEN_VALID_DURATION_SECS + EPOCH_SECONDS + int(time.mktime(datetime.now().timetuple()))
    vCard   = ""

    def to_bytes(o):
        return str(o).encode("utf-8")

    sep = b"\0" # Separator is a NULL character
    body = to_bytes(type) + sep + to_bytes(jid) + sep + to_bytes(expires) + sep + to_bytes(vCard)
    mac = hmac.new(bytearray(key, 'utf8'), msg=body, digestmod=hashlib.sha384).digest()
    ## Combine the body with the hex version of the mac
    serialized = body + sep + binascii.hexlify(mac)
    b64 = base64.b64encode(serialized)
    token = b64.encode("utf8")
    encoded_token = urllib2.quote(token)
    return encoded_token;

class record:
    def GET(self, roomId):
        encoded_token = getVidyoIOToken()
        os.system ("cp /home/webapp/config /opt/vidyo")
        with open("/opt/vidyo/config", "a") as myfile:
            myfile.write("resourceId=%s" %(roomId))
            myfile.write("token=%s" %(encoded_token))
        os.system ("/opt/vidyo/connect &")
        return roomId

if __name__ == '__main__' :
    app = web.application(urls, globals())
    app.run()
