#!/usr/bin/env python
#coding:utf-8

import logging
import logging.config
import os
import hashlib
import sys
import toml

reload(sys)
sys.setdefaultencoding('utf-8')
sys.dont_write_bytecode = True
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ['PATH'] = os.path.dirname(sys.executable) + os.pathsep + os.getenv('PATH')
config = toml.load(os.getenv('PYTHON_ENV', 'development') + '.toml')
logging.basicConfig(format='%(asctime)s [%(levelname)s] process@%(process)s thread@%(thread)s %(filename)s@%(lineno)s - %(funcName)s(): %(message)s', level=logging.INFO)

import xmltodict
from flask import Flask, request, Response
from wxhelpers import text_reply

app = Flask(__name__)

@app.route('/')
def index():
    return 'greeting from weixin'


@app.route('/weixin', methods=['GET', 'POST'])
def weixin_entrypoint():
    if request.args.get('echostr'):
        return weixin_echostr()
    else:
        return weixin_messasge()


def weixin_echostr():
    token = config['weixin']['token']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    signature = request.args['signature']
    echostr = request.args['echostr']
    if signature != hashlib.sha1(''.join(sorted([token, timestamp, nonce]))).hexdigest():
        return 'signature failed'
    return echostr


def weixin_messasge():
    message = xmltodict.parse(request.data)['xml']
    message_type = message['MsgType']
    if message_type == 'text':
        xml = weixin_handle_text(message)
    elif message_type == 'image':
        xml = weixin_handle_image(message)
    elif message_type == 'location':
        xml = weixin_handle_location(message)
    elif message_type == 'link':
        xml = weixin_handle_link(message)
    elif message_type == 'voice':
        xml = weixin_handle_voice(message)
    elif message_type == 'event':
        xml = weixin_handle_event(message)
    else:
        raise ValueError('Unknown message_type(%r) message=%s', message_type, message)
    logging.info('respone xml=%s', xml)
    return Response(xml, mimetype='text/xml')


def weixin_handle_text(message):
    logging.info('weixin_handle_text message=%s', message)
    sender = message['ToUserName']
    username = message['FromUserName']
    content = message['Content']
    return text_reply(username, sender, 'hello, you said "%s"' % content)


def weixin_handle_image(message):
    logging.info('weixin_handle_image message=%s', message)
    sender = message['ToUserName']
    username = message['FromUserName']
    return text_reply(username, sender, 'not implemented')


def weixin_handle_location(message):
    logging.info('weixin_handle_location message=%s', message)
    sender = message['ToUserName']
    username = message['FromUserName']
    return text_reply(username, sender, 'not implemented')


def weixin_handle_link(message):
    logging.info('weixin_handle_link message=%s', message)
    sender = message['ToUserName']
    username = message['FromUserName']
    return text_reply(username, sender, 'not implemented')


def weixin_handle_voice(message):
    logging.info('weixin_handle_voice message=%s', message)
    sender = message['ToUserName']
    username = message['FromUserName']
    return text_reply(username, sender, 'not implemented')


def weixin_handle_event(message):
    logging.info('weixin_handle_event message=%s', message)
    sender = message['ToUserName']
    username = message['FromUserName']
    return text_reply(username, sender, 'not implemented')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
