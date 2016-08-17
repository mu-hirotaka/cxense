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
