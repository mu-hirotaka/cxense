# encoding: UTF-8
import commands
import json
import os

def config():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'cxense_key.json')))
  return key

def segments():
  return ["fly_bys", "occasionals", "regulars", "fan"]

def sk_site_id():
  key = config()
  return key["sk"]["site_id"]

def bk_site_id():
  key = config()
  return key["bk"]["site_id"]

def bbk_site_id():
  key = config()
  return key["bbk"]["site_id"]

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

def bbk_flybys_id():
  key = config()
  return key["bbk"]["segment"]["fly_bys"]["id"]

def bbk_occasionals_id():
  key = config()
  return key["bbk"]["segment"]["occasionals"]["id"]

def bbk_regulars_id():
  key = config()
  return key["bbk"]["segment"]["regulars"]["id"]

def bbk_fan_id():
  key = config()
  return key["bbk"]["segment"]["fan"]["id"]

def sk_segment_name_to_segment_id(segment_name):
  if segment_name == 'fly_bys':
    return sk_flybys_id()
  elif segment_name == 'occasionals':
    return sk_occasionals_id()
  elif segment_name == 'regulars':
    return sk_regulars_id()
  else:
    return sk_fan_id()

def bk_segment_name_to_segment_id(segment_name):
  if segment_name == 'fly_bys':
    return bk_flybys_id()
  elif segment_name == 'occasionals':
    return bk_occasionals_id()
  elif segment_name == 'regulars':
    return bk_regulars_id()
  else:
    return bk_fan_id()

def bbk_segment_name_to_segment_id(segment_name):
  if segment_name == 'fly_bys':
    return bbk_flybys_id()
  elif segment_name == 'occasionals':
    return bbk_occasionals_id()
  elif segment_name == 'regulars':
    return bbk_regulars_id()
  else:
    return bbk_fan_id()

def segment_id_by_media_type_and_segment_name(media_type, segment_name):
  if media_type == 'SK':
    return sk_segment_name_to_segment_id(segment_name)
  elif media_type == 'BK':
    return bk_segment_name_to_segment_id(segment_name)
  elif media_type == 'BBK':
    return bbk_segment_name_to_segment_id(segment_name)

def api_script_path():
  return os.path.join(os.path.dirname(__file__), 'cx.py')

def media_type_to_site_id(media_type):
  if media_type == 'SK':
    return sk_site_id()
  elif media_type == 'BK':
    return bk_site_id()
  elif media_type == 'BBK':
    return bbk_site_id()

def basic_kpi(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def segment_kpi(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  res = {}
  for segment_name in segments():
    segment_id = segment_id_by_media_type_and_segment_name(media_type, segment_name)
    request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers","activeTime"], "filters":[{"type":"segment", "item":"%s"}]}\'' % (path, site_id, start_time, end_time, segment_id)
    response = commands.getoutput(request_command)
    decoded = json.loads(response)
    res.update({segment_name: decoded["data"]})
  return res

def basic_kpi_for_each_referrer(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHostClass"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers"}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def basic_kpi_from_search(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"search"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def basic_kpi_from_social(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"social"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def basic_kpi_from_other(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"other"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def basic_kpi_from_smartnews(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerHost","item":"smartnews.com"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def url_uu_ranking_from_smartnews(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHost","item":"smartnews.com"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def basic_kpi_from_yahoo(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerHost","item":"headlines.yahoo.co.jp"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def url_uu_ranking_from_yahoo(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHost","item":"headlines.yahoo.co.jp"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def basic_kpi_from_twitter(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerSocialNetwork"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Twitter"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def url_uu_ranking_from_twitter(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Twitter"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def basic_kpi_from_facebook(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerSocialNetwork"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Facebook"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def url_uu_ranking_from_facebook(media_type, start_time, end_time):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Facebook"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def pv_and_uu_by_url(media_type, start_time, end_time, url):
  site_id = media_type_to_site_id(media_type)
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "filters":[{"type":"event","group":"url","item":"%s"}]}\'' % (path, site_id, start_time, end_time, url)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]
