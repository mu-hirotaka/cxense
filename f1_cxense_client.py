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

def bk_basic_kpi(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def bk_segment_kpi(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  res = {}
  for segment_name in segments():
    segment = bk_segment_name_to_segment_id(segment_name)
    request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers","activeTime"], "filters":[{"type":"segment", "item":"%s"}]}\'' % (path, site_id, start_time, end_time, segment)
    response = commands.getoutput(request_command)
    decoded = json.loads(response)
    res.update({segment_name: decoded["data"]})
  return res

def sk_basic_kpi(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers"]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  return json.loads(response)

def sk_segment_kpi(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  res = {}
  for segment_name in segments():
    segment = sk_segment_name_to_segment_id(segment_name)
    request_command = 'python %s /traffic \'{"siteId":%s, "start":%d, "stop":%d, "fields":["uniqueUsers","activeTime"], "filters":[{"type":"segment", "item":"%s"}]}\'' % (path, site_id, start_time, end_time, segment)
    response = commands.getoutput(request_command)
    decoded = json.loads(response)
    res.update({segment_name: decoded["data"]})
  return res

def sk_basic_kpi_for_each_referrer(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHostClass"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers"}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def bk_basic_kpi_for_each_referrer(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHostClass"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers"}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def sk_basic_kpi_from_search(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"search"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def bk_basic_kpi_from_search(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"search"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def sk_basic_kpi_from_social(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"social"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def bk_basic_kpi_from_social(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"social"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def sk_basic_kpi_from_other(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"other"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def bk_basic_kpi_from_other(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHostClass","item":"other"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def sk_basic_kpi_from_smartnews(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerHost","item":"smartnews.com"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def bk_basic_kpi_from_smartnews(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerHost"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerHost","item":"smartnews.com"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def sk_url_uu_ranking_from_smartnews(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHost","item":"smartnews.com"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def bk_url_uu_ranking_from_smartnews(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerHost","item":"smartnews.com"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def sk_basic_kpi_from_yahoo(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerSearchEngine"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerSearchEngine","item":"Yahoo"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def bk_basic_kpi_from_yahoo(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerSearchEngine"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerSearchEngine","item":"Yahoo"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def sk_url_uu_ranking_from_yahoo(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerSearchEngine","item":"Yahoo"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def bk_url_uu_ranking_from_yahoo(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerSearchEngine","item":"Yahoo"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def sk_basic_kpi_from_twitter(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerSocialNetwork"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Twitter"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def bk_basic_kpi_from_twitter(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerSocialNetwork"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Twitter"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def sk_url_uu_ranking_from_twitter(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Twitter"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def bk_url_uu_ranking_from_twitter(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Twitter"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def sk_basic_kpi_from_facebook(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerSocialNetwork"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Facebook"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def bk_basic_kpi_from_facebook(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["referrerSocialNetwork"], "fields":["uniqueUsers"], "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Facebook"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"][0]

def sk_url_uu_ranking_from_facebook(start_time, end_time):
  site_id = sk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Facebook"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]

def bk_url_uu_ranking_from_facebook(start_time, end_time):
  site_id = bk_site_id()
  path = api_script_path()
  request_command = 'python %s /traffic/event \'{"siteId":%s, "start":%d, "stop":%d, "groups":["url"], "fields":["uniqueUsers","title"], "orderBy": "uniqueUsers", "filters":[{"type":"event","group":"referrerSocialNetwork","item":"Facebook"}]}\'' % (path, site_id, start_time, end_time)
  response = commands.getoutput(request_command)
  tmp = json.loads(response)
  return tmp["groups"][0]["items"]
