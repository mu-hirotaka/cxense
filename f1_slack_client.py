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

def post_to_bk_analytics_channel(content):
  payload_dic = {
    "channel": '#bk_analytics',
    "username": 'webhookbot',
    "text": content,
    "icon_emoji": ':ghost:',
  }
  r = requests.post(webhook_url(), data=json.dumps(payload_dic))

def post_to_sk_analytics_channel(content):
  payload_dic = {
    "channel": '#sk_analytics',
    "username": 'webhookbot',
    "text": content,
    "icon_emoji": ':ghost:',
  }
  r = requests.post(webhook_url(), data=json.dumps(payload_dic))
