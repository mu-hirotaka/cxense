# encoding: UTF-8
import calendar
import datetime
import json
import os

BOT_COMMENT = [
  "目標までもう一踏ん張り。今日こそ達成を目指そう。\n",
  "昨日の結果は散々だったな。今日は頑張ろうな。\n"
]

def config():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'kpi.json')))
  return key

def bk_daily_target_pv():
  kpi = config()
  return kpi["bk"]["daily"]["pv"]

def sk_daily_target_uu():
  kpi = config()
  return kpi["sk"]["daily"]["uu"]

def bk_daily_target_uu():
  kpi = config()
  return kpi["bk"]["daily"]["uu"]

def bk_monthly_target_pv():
  kpi = config()
  return kpi["bk"]["monthly"]["pv"]

def bk_monthly_target_uu():
  kpi = config()
  return kpi["bk"]["monthly"]["uu"]

def for_bk_slack(find_str, daily_kpi, monthly_kpi, daily_segment_kpi, monthly_segment_kpi):
  achievement_rate_of_daily_pv = float(daily_kpi["events"])/bk_daily_target_pv()
  achievement_rate_of_monthly_pv = float(monthly_kpi["events"])/bk_monthly_target_pv()
  achievement_rate_of_monthly_uu = float(monthly_kpi["uniqueUsers"])/bk_monthly_target_uu()
  diff_of_daily_pv = daily_kpi["events"] - bk_daily_target_pv()
  diff_of_monthly_pv = monthly_kpi["events"] - bk_monthly_target_pv()
  diff_of_monthly_uu = monthly_kpi["uniqueUsers"] - bk_monthly_target_uu()

  target_date = datetime.datetime.strptime(find_str, '%Y/%m/%d')
  days = calendar.monthrange(target_date.year,target_date.month)[1]
  remaining_days = days - target_date.day
  lapsed_days = days - remaining_days
  estimate_monthly_pv = (monthly_kpi["events"]/lapsed_days)*remaining_days+monthly_kpi["events"]
  estimate_monthly_uu = (monthly_kpi["uniqueUsers"]/lapsed_days)*remaining_days+monthly_kpi["uniqueUsers"]
  estimate_achievement_rate_of_monthly_pv = float(estimate_monthly_pv)/bk_monthly_target_pv()
  estimate_achievement_rate_of_monthly_uu = float(estimate_monthly_uu)/bk_monthly_target_uu()

  # for segment
  all_segment_pv_for_daily = daily_segment_kpi["fly_bys"]["events"] + daily_segment_kpi["occasionals"]["events"] + daily_segment_kpi["regulars"]["events"] + daily_segment_kpi["fan"]["events"]
  rate_of_flybys_daily_pv = float(daily_segment_kpi["fly_bys"]["events"])/all_segment_pv_for_daily
  rate_of_occasionals_daily_pv = float(daily_segment_kpi["occasionals"]["events"])/all_segment_pv_for_daily
  rate_of_regulars_daily_pv = float(daily_segment_kpi["regulars"]["events"])/all_segment_pv_for_daily
  rate_of_fan_daily_pv = float(daily_segment_kpi["fan"]["events"])/all_segment_pv_for_daily

  all_segment_uu_for_daily = daily_segment_kpi["fly_bys"]["uniqueUsers"] + daily_segment_kpi["occasionals"]["uniqueUsers"] + daily_segment_kpi["regulars"]["uniqueUsers"] + daily_segment_kpi["fan"]["uniqueUsers"]
  rate_of_flybys_daily_uu = float(daily_segment_kpi["fly_bys"]["uniqueUsers"])/all_segment_uu_for_daily
  rate_of_occasionals_daily_uu = float(daily_segment_kpi["occasionals"]["uniqueUsers"])/all_segment_uu_for_daily
  rate_of_regulars_daily_uu = float(daily_segment_kpi["regulars"]["uniqueUsers"])/all_segment_uu_for_daily
  rate_of_fan_daily_uu = float(daily_segment_kpi["fan"]["uniqueUsers"])/all_segment_uu_for_daily

  all_segment_pv_for_monthly = monthly_segment_kpi["fly_bys"]["events"] + monthly_segment_kpi["occasionals"]["events"] + monthly_segment_kpi["regulars"]["events"] + monthly_segment_kpi["fan"]["events"]
  rate_of_flybys_monthly_pv = float(monthly_segment_kpi["fly_bys"]["events"])/all_segment_pv_for_monthly
  rate_of_occasionals_monthly_pv = float(monthly_segment_kpi["occasionals"]["events"])/all_segment_pv_for_monthly
  rate_of_regulars_monthly_pv = float(monthly_segment_kpi["regulars"]["events"])/all_segment_pv_for_monthly
  rate_of_fan_monthly_pv = float(monthly_segment_kpi["fan"]["events"])/all_segment_pv_for_monthly

  all_segment_uu_for_monthly = monthly_segment_kpi["fly_bys"]["uniqueUsers"] + monthly_segment_kpi["occasionals"]["uniqueUsers"] + monthly_segment_kpi["regulars"]["uniqueUsers"] + monthly_segment_kpi["fan"]["uniqueUsers"]
  rate_of_flybys_monthly_uu = float(monthly_segment_kpi["fly_bys"]["uniqueUsers"])/all_segment_uu_for_monthly
  rate_of_occasionals_monthly_uu = float(monthly_segment_kpi["occasionals"]["uniqueUsers"])/all_segment_uu_for_monthly
  rate_of_regulars_monthly_uu = float(monthly_segment_kpi["regulars"]["uniqueUsers"])/all_segment_uu_for_monthly
  rate_of_fan_monthly_uu = float(monthly_segment_kpi["fan"]["uniqueUsers"])/all_segment_uu_for_monthly

  formatted = find_str + "\n"
  formatted += "[Daily KPI]\n"
  formatted += "PV:" + format(daily_kpi["events"], ",d") + "(目標:" + format(bk_daily_target_pv(),",d")
  formatted += "、目標比:" + format(achievement_rate_of_daily_pv, ".2%")
  formatted += "、差分:" +  format(diff_of_daily_pv, ",d") + ")\n"
  formatted += "　S1:" + format(daily_segment_kpi["fly_bys"]["events"], ",d") + "[" + format(rate_of_flybys_daily_pv, ".1%") + "]"
  formatted += "、S2:" + format(daily_segment_kpi["occasionals"]["events"], ",d") + "[" + format(rate_of_occasionals_daily_pv, ".1%") + "]"
  formatted += "、S3:" + format(daily_segment_kpi["regulars"]["events"], ",d") + "[" + format(rate_of_regulars_daily_pv, ".1%") + "]"
  formatted += "、S4:" + format(daily_segment_kpi["fan"]["events"], ",d") + "[" + format(rate_of_fan_daily_pv, ".1%") + "]\n"
  formatted += "UU:" + format(daily_kpi["uniqueUsers"],",d") + "\n"
  formatted += "　S1:" + format(daily_segment_kpi["fly_bys"]["uniqueUsers"], ",d") + "[" + format(rate_of_flybys_daily_uu, ".1%") + "]"
  formatted += "、S2:" + format(daily_segment_kpi["occasionals"]["uniqueUsers"], ",d") + "[" + format(rate_of_occasionals_daily_uu, ".1%") + "]"
  formatted += "、S3:" + format(daily_segment_kpi["regulars"]["uniqueUsers"], ",d") + "[" + format(rate_of_regulars_daily_uu, ".1%") + "]"
  formatted += "、S4:" + format(daily_segment_kpi["fan"]["uniqueUsers"], ",d") + "[" + format(rate_of_fan_daily_uu, ".1%") + "]\n"
#  if achievement_rate_of_daily_pv >= 0.9:
#    formatted += BOT_COMMENT[0]
#  elif achievement_rate_of_daily_pv < 0.5:
#    formatted += BOT_COMMENT[1]
  formatted += "[Monthly KPI]\n"
  formatted += "残り日数:" + str(remaining_days) + "\n"
  formatted += "累積PV:" + format(monthly_kpi["events"],",d") + "(目標:" + format(bk_monthly_target_pv(),",d")
  formatted += "、目標比:" + format(achievement_rate_of_monthly_pv, ".1%")
  formatted += "、差分:" +  format(diff_of_monthly_pv, ",d")
  if remaining_days != 0:
    formatted += "、着地予測:" + format(estimate_monthly_pv, ",d") + "[" + format(estimate_achievement_rate_of_monthly_pv, ".1%") + "]"
  formatted += ")\n"
  formatted += "　S1:" + format(monthly_segment_kpi["fly_bys"]["events"], ",d") + "[" + format(rate_of_flybys_monthly_pv, ".1%") + "]"
  formatted += "、S2:" + format(monthly_segment_kpi["occasionals"]["events"], ",d") + "[" + format(rate_of_occasionals_monthly_pv, ".1%") + "]"
  formatted += "、S3:" + format(monthly_segment_kpi["regulars"]["events"], ",d") + "[" + format(rate_of_regulars_monthly_pv, ".1%") + "]"
  formatted += "、S4:" + format(monthly_segment_kpi["fan"]["events"], ",d") + "[" + format(rate_of_fan_monthly_pv, ".1%") + "]\n"
  formatted += "累積UU:" + format(monthly_kpi["uniqueUsers"],",d") + "(目標:" + format(bk_monthly_target_uu(),",d")
  formatted += "、目標比:" + format(achievement_rate_of_monthly_uu, ".1%")
  formatted += "、差分:" +  format(diff_of_monthly_uu, ",d")
  if remaining_days != 0:
    formatted += "、着地予測:" + format(estimate_monthly_uu, ",d") + "[" + format(estimate_achievement_rate_of_monthly_uu, ".1%") + "]"
  formatted += ")\n"
  formatted += "　S1:" + format(monthly_segment_kpi["fly_bys"]["uniqueUsers"], ",d") + "[" + format(rate_of_flybys_monthly_uu, ".1%") + "]"
  formatted += "、S2:" + format(monthly_segment_kpi["occasionals"]["uniqueUsers"], ",d") + "[" + format(rate_of_occasionals_monthly_uu, ".1%") + "]"
  formatted += "、S3:" + format(monthly_segment_kpi["regulars"]["uniqueUsers"], ",d") + "[" + format(rate_of_regulars_monthly_uu, ".1%") + "]"
  formatted += "、S4:" + format(monthly_segment_kpi["fan"]["uniqueUsers"], ",d") + "[" + format(rate_of_fan_monthly_uu, ".1%") + "]\n"
  return formatted

def for_sk_slack(find_str, daily_kpi, monthly_kpi):
  target_date = datetime.datetime.strptime(find_str, '%Y/%m/%d')
  days = calendar.monthrange(target_date.year,target_date.month)[1]
  remaining_days = days - target_date.day
  lapsed_days = days - remaining_days
  estimate_monthly_pv = (monthly_kpi["events"]/lapsed_days)*remaining_days+monthly_kpi["events"]
  estimate_monthly_uu = (monthly_kpi["uniqueUsers"]/lapsed_days)*remaining_days+monthly_kpi["uniqueUsers"]

  formatted = find_str + "\n"
  formatted += "[Daily KPI]\n"
  formatted += "PV:" + format(daily_kpi["events"], ",d") + "\n"
  formatted += "UU:" + format(daily_kpi["uniqueUsers"],",d") + "\n"
  formatted += "[Monthly KPI]\n"
  formatted += "残り日数:" + str(remaining_days) + "\n"
  formatted += "累積PV:" + format(monthly_kpi["events"],",d")
  if remaining_days != 0:
    formatted += "(着地予測:" + format(estimate_monthly_pv, ",d") + ")"
  formatted += "\n累積UU:" + format(monthly_kpi["uniqueUsers"],",d")
  if remaining_days != 0:
    formatted += "(着地予測:" + format(estimate_monthly_uu, ",d") + ")"
  return formatted

def format_sk_basic_kpi(kpi):
  pv = kpi["data"]["events"]
  uu = kpi["data"]["uniqueUsers"]
  achievement_rate_of_daily_uu = float(uu)/sk_daily_target_uu()
  diff_of_daily_uu = uu - sk_daily_target_uu()

  messages = []
  messages.append("＜基本KPI＞\n")
  messages.append("　PV:" + format(pv, ",d") + "\n")
  messages.append("　UU:" + format(uu, ",d"))
  messages.append("(目標:" + format(sk_daily_target_uu(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_daily_uu, ".2%"))
  messages.append("、差分:" + format(diff_of_daily_uu, ",d") + ")\n")
  return "".join(messages)

def format_bk_basic_kpi(kpi):
  pv = kpi["data"]["events"]
  uu = kpi["data"]["uniqueUsers"]
  achievement_rate_of_daily_uu = float(uu)/bk_daily_target_uu()
  diff_of_daily_uu = uu - bk_daily_target_uu()

  messages = []
  messages.append("＜基本KPI＞\n")
  messages.append("　PV:" + format(pv, ",d") + "\n")
  messages.append("　UU:" + format(uu, ",d"))
  messages.append("(目標:" + format(bk_daily_target_uu(), ",d"))
  messages.append("、目標比:" + format(achievement_rate_of_daily_uu, ".2%"))
  messages.append("、差分:" + format(diff_of_daily_uu, ",d") + ")\n")
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
  return "".join(messages)

def format_for_bk_slack(date_str, kpi):
  basic_kpi = kpi["daily"]["basic"]
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
  return "".join(messages)
