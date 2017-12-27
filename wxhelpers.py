# coding: utf-8

import time

def text_reply(username, sender, content):
    shared = _shared_reply(username, sender, 'text')
    template = '<xml>%s<Content><![CDATA[%s]]></Content></xml>'
    return template % (shared, content)


def music_reply(username, sender, **kwargs):
    kwargs['shared'] = _shared_reply(username, sender, 'music')

    template = (
        '<xml>'
        '%(shared)s'
        '<Music>'
        '<Title><![CDATA[%(title)s]]></Title>'
        '<Description><![CDATA[%(description)s]]></Description>'
        '<MusicUrl><![CDATA[%(music_url)s]]></MusicUrl>'
        '<HQMusicUrl><![CDATA[%(hq_music_url)s]]></HQMusicUrl>'
        '</Music>'
        '</xml>'
    )
    return template % kwargs


def news_reply(username, sender, *items):
    item_template = (
        '<item>'
        '<Title><![CDATA[%(title)s]]></Title>'
        '<Description><![CDATA[%(description)s]]></Description>'
        '<PicUrl><![CDATA[%(picurl)s]]></PicUrl>'
        '<Url><![CDATA[%(url)s]]></Url>'
        '</item>'
    )
    articles = [item_template % o for o in items]

    template = (
        '<xml>'
        '%(shared)s'
        '<ArticleCount>%(count)d</ArticleCount>'
        '<Articles>%(articles)s</Articles>'
        '</xml>'
    )
    dct = {
        'shared': _shared_reply(username, sender, 'news'),
        'count': len(items),
        'articles': ''.join(articles)
    }
    return template % dct


def transfer_customer_service_reply(username, sender, service_account):
    template = (
        '<xml>%(shared)s'
        '%(transfer_info)s</xml>')
    transfer_info = ''
    if service_account:
        transfer_info = (
            '<TransInfo>'
            '<KfAccount>![CDATA[%s]]</KfAccount>'
            '</TransInfo>') % service_account

    dct = {
        'shared': _shared_reply(username, sender,
                                message_type='transfer_customer_service'),
        'transfer_info': transfer_info
    }
    return template % dct


def image_reply(username, sender, media_id):
    shared = _shared_reply(username, sender, 'image')
    template = '<xml>%s<Image><MediaId><![CDATA[%s]]></MediaId></Image></xml>'
    return template % (shared, media_id)


def voice_reply(username, sender, media_id):
    shared = _shared_reply(username, sender, 'voice')
    template = '<xml>%s<Voice><MediaId><![CDATA[%s]]></MediaId></Voice></xml>'
    return template % (shared, media_id)


def video_reply(username, sender, **kwargs):
    kwargs['shared'] = _shared_reply(username, sender, 'video')

    template = (
        '<xml>'
        '%(shared)s'
        '<Video>'
        '<MediaId><![CDATA[%(media_id)s]]></MediaId>'
        '<Title><![CDATA[%(title)s]]></Title>'
        '<Description><![CDATA[%(description)s]]></Description>'
        '</Video>'
        '</xml>'
    )
    return template % kwargs

def _shared_reply(username, sender, message_type):
    dct = {
        'username': username,
        'sender': sender,
        'type': message_type,
        'timestamp': int(time.time()),
    }
    template = (
        '<ToUserName><![CDATA[%(username)s]]></ToUserName>'
        '<FromUserName><![CDATA[%(sender)s]]></FromUserName>'
        '<CreateTime>%(timestamp)d</CreateTime>'
        '<MsgType><![CDATA[%(type)s]]></MsgType>'
    )
    return template % dct
