# encoding: UTF-8
import calendar
import datetime
import json
import os

def config():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'kpi.json')))
  return key

def sk_daily_target_pv():
  kpi = config()
  return kpi["sk"]["daily"]["pv"]

def bk_daily_target_pv():
  kpi = config()
  return kpi["bk"]["daily"]["pv"]

def sk_daily_target_uu():
  kpi = config()
  return kpi["sk"]["daily"]["uu"]

def bk_daily_target_uu():
  kpi = config()
  return kpi["bk"]["daily"]["uu"]

def sk_monthly_target_pv():
  kpi = config()
  return kpi["sk"]["monthly"]["pv"]

def bk_monthly_target_pv():
  kpi = config()
  return kpi["bk"]["monthly"]["pv"]

def sk_monthly_target_uu():
  kpi = config()
  return kpi["sk"]["monthly"]["uu"]

def bk_monthly_target_uu():
  kpi = config()
  return kpi["bk"]["monthly"]["uu"]

def format_sk_basic_kpi(kpi):
  pv = kpi["data"]["events"]
  uu = kpi["data"]["uniqueUsers"]
  achievement_rate_of_pv = float(pv)/sk_daily_target_pv()
  diff_of_pv = pv - sk_daily_target_pv()
  achievement_rate_of_uu = float(uu)/sk_daily_target_uu()
  diff_of_uu = uu - sk_daily_target_uu()

  messages = []
  messages.append("＜基本KPI＞\n")
  messages.append("　PV:" + format(pv, ",d"))
  messages.append("(目標:" + format(sk_daily_target_pv(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_pv, ".1%"))
  messages.append("、差分:" + format(diff_of_pv, ",d") + ")\n")
  messages.append("　UU:" + format(uu, ",d"))
  messages.append("(目標:" + format(sk_daily_target_uu(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_uu, ".1%"))
  messages.append("、差分:" + format(diff_of_uu, ",d") + ")\n")
  return "".join(messages)

def format_bk_basic_kpi(kpi):
  pv = kpi["data"]["events"]
  uu = kpi["data"]["uniqueUsers"]
  achievement_rate_of_pv = float(pv)/bk_daily_target_pv()
  diff_of_pv = pv - bk_daily_target_pv()
  achievement_rate_of_uu = float(uu)/bk_daily_target_uu()
  diff_of_uu = uu - bk_daily_target_uu()

  messages = []
  messages.append("＜基本KPI＞\n")
  messages.append("　PV:" + format(pv, ",d"))
  messages.append("(目標:" + format(bk_daily_target_pv(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_pv, ".1%"))
  messages.append("、差分:" + format(diff_of_pv, ",d") + ")\n")
  messages.append("　UU:" + format(uu, ",d"))
  messages.append("(目標:" + format(bk_daily_target_uu(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_uu, ".1%"))
  messages.append("、差分:" + format(diff_of_uu, ",d") + ")\n")
  return "".join(messages)

def format_sk_montyly_kpi(date_str, kpi):
  pv = kpi["data"]["events"]
  uu = kpi["data"]["uniqueUsers"]

  achievement_rate_of_pv = float(pv)/sk_monthly_target_pv()
  diff_of_pv = pv - sk_monthly_target_pv()
  achievement_rate_of_uu = float(uu)/sk_monthly_target_uu()
  diff_of_uu = uu - sk_monthly_target_uu()

  target_date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
  days = calendar.monthrange(target_date.year,target_date.month)[1]
  remaining_days = days - target_date.day
  lapsed_days = days - remaining_days

  estimate_pv = (pv/lapsed_days) * remaining_days + pv
  estimate_uu = (uu/lapsed_days) * remaining_days + uu
  estimate_achievement_rate_of_pv = float(estimate_pv)/sk_monthly_target_pv()
  estimate_achievement_rate_of_uu = float(estimate_uu)/sk_monthly_target_uu()

  messages = []
  messages.append("＜Monthly KPI＞\n")
  messages.append("　残り日数:" + str(remaining_days) + "日\n")
  messages.append("　累積PV:" + format(pv, ",d"))
  messages.append("(目標:" + format(sk_monthly_target_pv(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_pv, ".1%"))
  messages.append("、差分:" + format(diff_of_pv, ",d"))
  if remaining_days != 0:
    messages.append("、着地予測:" + format(estimate_pv, ",d") + "[" + format(estimate_achievement_rate_of_pv, ".1%") + "]")
  messages.append(")\n")
  messages.append("　累積UU:" + format(uu, ",d"))
  messages.append("(目標:" + format(sk_monthly_target_uu(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_uu, ".1%"))
  messages.append("、差分:" + format(diff_of_uu, ",d"))
  if remaining_days != 0:
    messages.append("、着地予測:" + format(estimate_uu, ",d") + "[" + format(estimate_achievement_rate_of_uu, ".1%") + "]")
  messages.append(")\n")
  return "".join(messages)

def format_bk_montyly_kpi(date_str, kpi):
  pv = kpi["data"]["events"]
  uu = kpi["data"]["uniqueUsers"]

  achievement_rate_of_pv = float(pv)/bk_monthly_target_pv()
  diff_of_pv = pv - bk_monthly_target_pv()
  achievement_rate_of_uu = float(uu)/bk_monthly_target_uu()
  diff_of_uu = uu - bk_monthly_target_uu()

  target_date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
  days = calendar.monthrange(target_date.year,target_date.month)[1]
  remaining_days = days - target_date.day
  lapsed_days = days - remaining_days

  estimate_pv = (pv/lapsed_days) * remaining_days + pv
  estimate_uu = (uu/lapsed_days) * remaining_days + uu
  estimate_achievement_rate_of_pv = float(estimate_pv)/bk_monthly_target_pv()
  estimate_achievement_rate_of_uu = float(estimate_uu)/bk_monthly_target_uu()

  messages = []
  messages.append("＜Monthly KPI＞\n")
  messages.append("　残り日数:" + str(remaining_days) + "日\n")
  messages.append("　累積PV:" + format(pv, ",d"))
  messages.append("(目標:" + format(bk_monthly_target_pv(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_pv, ".1%"))
  messages.append("、差分:" + format(diff_of_pv, ",d"))
  if remaining_days != 0:
    messages.append("、着地予測:" + format(estimate_pv, ",d") + "[" + format(estimate_achievement_rate_of_pv, ".1%") + "]")
  messages.append(")\n")
  messages.append("　累積UU:" + format(uu, ",d"))
  messages.append("(目標:" + format(bk_monthly_target_uu(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_uu, ".1%"))
  messages.append("、差分:" + format(diff_of_uu, ",d"))
  if remaining_days != 0:
    messages.append("、着地予測:" + format(estimate_uu, ",d") + "[" + format(estimate_achievement_rate_of_uu, ".1%") + "]")
  messages.append(")\n")
  return "".join(messages)

def format_kpi_for_each_referrer(each_referrer_response, search_response, social_response, other_response):
  all_pv = 0
  all_uu = 0
  for host in each_referrer_response:
    all_pv += host["data"]["events"]
    all_uu += host["data"]["uniqueUsers"]
  messages = []
  messages.append("＜参照元種別＞\n")
  for host in each_referrer_response:
    host_name = host["item"].encode('ascii')
    pv = host["data"]["events"]
    uu = host["data"]["uniqueUsers"]
    rate_of_pv = float(pv)/all_pv
    rate_of_uu = float(uu)/all_uu
    messages.append("　[" + host_name + "] ")
    messages.append("PV:" + format(pv, ",d") + "[" + format(rate_of_pv, ".1%") + "] ")
    messages.append("UU:" + format(uu, ",d") + "[" + format(rate_of_uu, ".1%") + "]\n")
    if host_name == 'search':
      messages.append(format_kpi_from_search(search_response, pv, uu))
    elif host_name == 'social':
      messages.append(format_kpi_from_social(social_response, pv, uu))
    elif host_name == 'other':
      messages.append(format_kpi_from_other(other_response, pv, uu))
  return "".join(messages)

def format_kpi_from_search(response, all_pv, all_uu):
  messages = []
  for idx,elem in enumerate(response):
    name = elem["item"].encode('ascii')
    pv = elem["data"]["events"] 
    uu = elem["data"]["uniqueUsers"] 
    rate_of_pv = float(pv)/all_pv
    rate_of_uu = float(uu)/all_uu
    messages.append("　　" + name + " ")
    messages.append("PV:" + format(pv, ",d") + "[" + format(rate_of_pv, ".1%") + "] ")
    messages.append("UU:" + format(uu, ",d") + "[" + format(rate_of_uu, ".1%") + "]\n")
    if idx == 4:
      break
  return "".join(messages)

def format_kpi_from_social(response, all_pv, all_uu):
  messages = []
  for idx,elem in enumerate(response):
    name = elem["item"].encode('ascii')
    pv = elem["data"]["events"] 
    uu = elem["data"]["uniqueUsers"] 
    rate_of_pv = float(pv)/all_pv
    rate_of_uu = float(uu)/all_uu
    messages.append("　　" + name + " ")
    messages.append("PV:" + format(pv, ",d") + "[" + format(rate_of_pv, ".1%") + "] ")
    messages.append("UU:" + format(uu, ",d") + "[" + format(rate_of_uu, ".1%") + "]\n")
    if idx == 4:
      break
  return "".join(messages)

def format_kpi_from_other(response, all_pv, all_uu):
  messages = []
  for idx,elem in enumerate(response):
    name = elem["item"].encode('ascii')
    pv = elem["data"]["events"] 
    uu = elem["data"]["uniqueUsers"] 
    rate_of_pv = float(pv)/all_pv
    rate_of_uu = float(uu)/all_uu
    messages.append("　　" + name + " ")
    messages.append("PV:" + format(pv, ",d") + "[" + format(rate_of_pv, ".1%") + "] ")
    messages.append("UU:" + format(uu, ",d") + "[" + format(rate_of_uu, ".1%") + "]\n")
    if idx == 4:
      break
  return "".join(messages)

def format_segment_kpi(kpi):
  fly_bys_pv = kpi["fly_bys"]["events"]
  fly_bys_uu = kpi["fly_bys"]["uniqueUsers"]
  occasionals_pv = kpi["occasionals"]["events"]
  occasionals_uu = kpi["occasionals"]["uniqueUsers"]
  regulars_pv = kpi["regulars"]["events"]
  regulars_uu = kpi["regulars"]["uniqueUsers"]
  fan_pv = kpi["fan"]["events"]
  fan_uu = kpi["fan"]["uniqueUsers"]
  all_pv = fly_bys_pv + occasionals_pv + regulars_pv + fan_pv
  all_uu = fly_bys_uu + occasionals_uu + regulars_uu + fan_uu

  rate_of_flybys_pv = float(fly_bys_pv)/all_pv
  rate_of_occasionals_pv = float(occasionals_pv)/all_pv
  rate_of_regulars_pv = float(regulars_pv)/all_pv
  rate_of_fan_pv = float(fan_pv)/all_pv
  rate_of_flybys_uu = float(fly_bys_uu)/all_uu
  rate_of_occasionals_uu = float(occasionals_uu)/all_uu
  rate_of_regulars_uu = float(regulars_uu)/all_uu
  rate_of_fan_uu = float(fan_uu)/all_uu

  messages = []
  messages.append("＜セグメント別＞\n")
  messages.append("　[Fly-bys(月間1 - 2PV)] ")
  messages.append("PV:" + format(fly_bys_pv, ",d") + "[" + format(rate_of_flybys_pv, ".1%") + "] ")
  messages.append("UU:" + format(fly_bys_uu, ",d") + "[" + format(rate_of_flybys_uu, ".1%") + "]\n")
  messages.append("　[Occasionals(月間3 - 8PV)] ")
  messages.append("PV:" + format(occasionals_pv, ",d") + "[" + format(rate_of_occasionals_pv, ".1%") + "] ")
  messages.append("UU:" + format(occasionals_uu, ",d") + "[" + format(rate_of_occasionals_uu, ".1%") + "]\n")
  messages.append("　[Regulars(月間9 – 18PV)] ")
  messages.append("PV:" + format(regulars_pv, ",d") + "[" + format(rate_of_regulars_pv, ".1%") + "] ")
  messages.append("UU:" + format(regulars_uu, ",d") + "[" + format(rate_of_regulars_uu, ".1%") + "]\n")
  messages.append("　[Fan(月間19PV以上)] ")
  messages.append("PV:" + format(fan_pv, ",d") + "[" + format(rate_of_fan_pv, ".1%") + "] ")
  messages.append("UU:" + format(fan_uu, ",d") + "[" + format(rate_of_fan_uu, ".1%") + "]\n")
  return "".join(messages)

def format_smartnews_kpi(kpi):
  basic_kpi = kpi["basic"]
  ranking = kpi["ranking"]
  all_pv = basic_kpi["data"]["events"]
  all_uu = basic_kpi["data"]["uniqueUsers"]

  messages = []
  messages.append("＜SmartNews＞（PV:" + format(all_pv, ",d") + " UU:" + format(all_uu, ",d") + "）\n")
  messages.append("　[UUランキング]\n")
  for idx,elem in enumerate(ranking):
    title = elem["title"].encode('utf-8')
    pv = elem["data"]["events"] 
    uu = elem["data"]["uniqueUsers"] 
    messages.append("　　PV:" + format(pv, ",d") + " UU:" + format(uu, ",d") + " " + title + "\n")
    if idx == 4:
      break
  return "".join(messages)

def format_yahoo_kpi(kpi):
  basic_kpi = kpi["basic"]
  ranking = kpi["ranking"]
  all_pv = basic_kpi["data"]["events"]
  all_uu = basic_kpi["data"]["uniqueUsers"]

  messages = []
  messages.append("＜Yahoo＞（PV:" + format(all_pv, ",d") + " UU:" + format(all_uu, ",d") + "）\n")
  messages.append("　[UUランキング]\n")
  for idx,elem in enumerate(ranking):
    title = elem["title"].encode('utf-8')
    pv = elem["data"]["events"] 
    uu = elem["data"]["uniqueUsers"] 
    messages.append("　　PV:" + format(pv, ",d") + " UU:" + format(uu, ",d") + " " + title + "\n")
    if idx == 4:
      break
  return "".join(messages)

def format_twitter_kpi(kpi):
  basic_kpi = kpi["basic"]
  ranking = kpi["ranking"]
  all_pv = basic_kpi["data"]["events"]
  all_uu = basic_kpi["data"]["uniqueUsers"]

  messages = []
  messages.append("＜Twitter＞（PV:" + format(all_pv, ",d") + " UU:" + format(all_uu, ",d") + "）\n")
  messages.append("　[UUランキング]\n")
  for idx,elem in enumerate(ranking):
    title = elem["title"].encode('utf-8')
    pv = elem["data"]["events"] 
    uu = elem["data"]["uniqueUsers"] 
    messages.append("　　PV:" + format(pv, ",d") + " UU:" + format(uu, ",d") + " " + title + "\n")
    if idx == 4:
      break
  return "".join(messages)

def format_facebook_kpi(kpi):
  basic_kpi = kpi["basic"]
  ranking = kpi["ranking"]
  all_pv = basic_kpi["data"]["events"]
  all_uu = basic_kpi["data"]["uniqueUsers"]

  messages = []
  messages.append("＜Facebook＞（PV:" + format(all_pv, ",d") + " UU:" + format(all_uu, ",d") + "）\n")
  messages.append("　[UUランキング]\n")
  for idx,elem in enumerate(ranking):
    title = elem["title"].encode('utf-8')
    pv = elem["data"]["events"] 
    uu = elem["data"]["uniqueUsers"] 
    messages.append("　　PV:" + format(pv, ",d") + " UU:" + format(uu, ",d") + " " + title + "\n")
    if idx == 4:
      break
  return "".join(messages)

def format_for_sk_slack(date_str, kpi):
  basic_kpi = kpi["daily"]["basic"]
  monthly_kpi = kpi["monthly"]["basic"]
  segment_kpi = kpi["daily"]["segment"]
  all_referrer_kpi = kpi["daily"]["referrer"]["all"]
  search_referrer_kpi = kpi["daily"]["referrer"]["search"]
  social_referrer_kpi = kpi["daily"]["referrer"]["social"]
  other_referrer_kpi = kpi["daily"]["referrer"]["other"]
  smartnews_kpi = kpi["daily"]["smartnews"]
  yahoo_kpi = kpi["daily"]["yahoo"]
  twitter_kpi = kpi["daily"]["twitter"]
  facebook_kpi = kpi["daily"]["facebook"]

  messages = []
  messages.append(date_str + "\n")
  messages.append(format_sk_basic_kpi(basic_kpi))
  messages.append(format_segment_kpi(segment_kpi))
  messages.append(format_kpi_for_each_referrer(all_referrer_kpi, search_referrer_kpi, social_referrer_kpi, other_referrer_kpi))
  messages.append(format_smartnews_kpi(smartnews_kpi))
  messages.append(format_yahoo_kpi(yahoo_kpi))
  messages.append(format_twitter_kpi(twitter_kpi))
  messages.append(format_facebook_kpi(facebook_kpi))
  messages.append(format_sk_montyly_kpi(date_str, monthly_kpi))
  return "".join(messages)

def format_for_bk_slack(date_str, kpi):
  basic_kpi = kpi["daily"]["basic"]
  monthly_kpi = kpi["monthly"]["basic"]
  segment_kpi = kpi["daily"]["segment"]
  all_referrer_kpi = kpi["daily"]["referrer"]["all"]
  search_referrer_kpi = kpi["daily"]["referrer"]["search"]
  social_referrer_kpi = kpi["daily"]["referrer"]["social"]
  other_referrer_kpi = kpi["daily"]["referrer"]["other"]
  smartnews_kpi = kpi["daily"]["smartnews"]
  yahoo_kpi = kpi["daily"]["yahoo"]
  twitter_kpi = kpi["daily"]["twitter"]
  facebook_kpi = kpi["daily"]["facebook"]

  messages = []
  messages.append(date_str + "\n")
  messages.append(format_bk_basic_kpi(basic_kpi))
  messages.append(format_segment_kpi(segment_kpi))
  messages.append(format_kpi_for_each_referrer(all_referrer_kpi, search_referrer_kpi, social_referrer_kpi, other_referrer_kpi))
  messages.append(format_smartnews_kpi(smartnews_kpi))
  messages.append(format_yahoo_kpi(yahoo_kpi))
  messages.append(format_twitter_kpi(twitter_kpi))
  messages.append(format_facebook_kpi(facebook_kpi))
  messages.append(format_bk_montyly_kpi(date_str, monthly_kpi))
  return "".join(messages)
