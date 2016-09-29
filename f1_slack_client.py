# encoding: UTF-8
import json
import requests
import os

def config():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'slack_key.json')))
  return key

def webhook_url():
  key = config()
  return key["webhook_url"]

def media_type_to_channel_name(media_type):
  if media_type == 'SK':
    return '#sk_analytics'
  elif media_type == 'BK':
    return '#bk_analytics'
  elif media_type == 'BBK':
    return '#bbk_analytics'

def post_to_channel(media_type, content):
  channel_name = media_type_to_channel_name(media_type)
  payload_dic = {
    "channel": channel_name,
    "username": 'webhookbot',
    "text": content,
    "icon_emoji": ':ghost:',
  }
  r = requests.post(webhook_url(), data=json.dumps(payload_dic))
