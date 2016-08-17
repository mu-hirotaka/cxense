# encoding: UTF-8
import commands
import json
import os

def config():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'cxense_key.json')))
  return key

def segments():
  return ["fly_bys", "occasionals", "regulars", "fan"]

def bk_site_id():
  key = config()
  return key["bk"]["site_id"]

def sk_site_id():
  key = config()
  return key["sk"]["site_id"]

def bk_flybys_id():
  key = config()
  return key["bk"]["segment"]["fly_bys"]["id"]

def bk_occasionals_id():
  key = config()
  return key["bk"]["segment"]["occasionals"]["id"]

def bk_regulars_id():
  key = config()
  return key["bk"]["segment"]["regulars"]["id"]

def bk_fan_id():
  key = config()
  return key["bk"]["segment"]["fan"]["id"]

def bk_segment_name_to_segment_id(segment_name):
  if segment_name == 'fly_bys':
    return bk_flybys_id()
  elif segment_name == 'occasionals':
    return bk_occasionals_id()
  elif segment_name == 'regulars':
    return bk_regulars_id()
  else:
    return bk_fan_id()

def sk_flybys_id():
  key = config()
  return key["sk"]["segment"]["fly_bys"]["id"]

def sk_occasionals_id():
  key = config()
  return key["sk"]["segment"]["occasionals"]["id"]

def sk_regulars_id():
  key = config()
  return key["sk"]["segment"]["regulars"]["id"]

def sk_fan_id():
  key = config()
  return key["sk"]["segment"]["fan"]["id"]

def sk_segment_name_to_segment_id(segment_name):
  if segment_name == 'fly_bys':
    return sk_flybys_id()
  elif segment_name == 'occasionals':
    return sk_occasionals_id()
  elif segment_name == 'regulars':
    return sk_regulars_id()
  else:
    return sk_fan_id()

def api_script_path():
  return os.path.join(os.path.dirname(__file__), 'cx.py')

def bk_daily_kpi(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def bk_daily_segment_kpi(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  res = {}
  for segment_name in segments():
    segment = bk_segment_name_to_segment_id(segment_name)
    request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"], "filters":[{"type":"segment", "item":"%s"}]}\'' % (path, site_id, start_time, end_time, segment)
    response = commands.getoutput(request_command)
    decoded = json.loads(response)
    res.update({segment_name: decoded["data"]})
  return res

def bk_monthly_kpi(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def bk_monthly_segment_kpi(start_time, end_time):
  return bk_daily_segment_kpi(start_time, end_time)

def sk_daily_kpi(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def sk_daily_segment_kpi(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  res = {}
  for segment_name in segments():
    segment = sk_segment_name_to_segment_id(segment_name)
    request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"], "filters":[{"type":"segment", "item":"%s"}]}\'' % (path, site_id, start_time, end_time, segment)
    response = commands.getoutput(request_command)
    decoded = json.loads(response)
    res.update({segment_name: decoded["data"]})
  return res

def sk_monthly_kpi(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)
