# encoding: UTF-8
import commands
import json
import os

def config():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'cxense_key.json')))
  return key

def bk_site_id():
  key = config()
  return key["bk"]["site_id"]

def sk_site_id():
  key = config()
  return key["sk"]["site_id"]

def api_script_path():
  return os.path.join(os.path.dirname(__file__), 'cx.py')

def bk_daily_kpi(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def bk_monthly_kpi(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def sk_daily_kpi(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def sk_monthly_kpi(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)
