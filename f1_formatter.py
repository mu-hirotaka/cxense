# encoding: UTF-8
import calendar
import datetime
import json
import os

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

def for_bk_slack(find_str, daily_kpi, monthly_kpi):
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

  formatted = "------------------------ " + find_str + " ------------------------\n"
  formatted += "[Daily KPI]\n"
  formatted += "PV:" + format(daily_kpi["events"], ",d") + "(目標:" + format(bk_daily_target_pv(),",d")
  formatted += "、目標比:" + format(achievement_rate_of_daily_pv, ".1%")
  formatted += "、差分:" +  format(diff_of_daily_pv, ",d") + ")\n"
  formatted += "UU:" + format(daily_kpi["uniqueUsers"],",d") + "\n"
  if achievement_rate_of_daily_pv > 0.9:
    formatted += "目標までもう一踏ん張り。今日こそ達成を目指そう。\n"
  formatted += "[Monthly KPI]\n"
  formatted += "残り日数:" + str(remaining_days) + "\n"
  formatted += "累積PV:" + format(monthly_kpi["events"],",d") + "(目標:" + format(bk_monthly_target_pv(),",d")
  formatted += "、目標比:" + format(achievement_rate_of_monthly_pv, ".1%")
  formatted += "、差分:" +  format(diff_of_monthly_pv, ",d")
  if remaining_days != 0:
    formatted += "、着地予測:" + format(estimate_monthly_pv, ",d") + "[" + format(estimate_achievement_rate_of_monthly_pv, ".1%") + "]"
  formatted += ")\n"
  formatted += "累積UU:" + format(monthly_kpi["uniqueUsers"],",d") + "(目標:" + format(bk_monthly_target_uu(),",d")
  formatted += "、目標比:" + format(achievement_rate_of_monthly_uu, ".1%")
  formatted += "、差分:" +  format(diff_of_monthly_uu, ",d")
  if remaining_days != 0:
    formatted += "、着地予測:" + format(estimate_monthly_uu, ",d") + "[" + format(estimate_achievement_rate_of_monthly_uu, ".1%") + "]"
  formatted += ")"
  return formatted

def for_sk_slack(find_str, daily_kpi, monthly_kpi):
  target_date = datetime.datetime.strptime(find_str, '%Y/%m/%d')
  days = calendar.monthrange(target_date.year,target_date.month)[1]
  remaining_days = days - target_date.day
  lapsed_days = days - remaining_days
  estimate_monthly_pv = (monthly_kpi["events"]/lapsed_days)*remaining_days+monthly_kpi["events"]
  estimate_monthly_uu = (monthly_kpi["uniqueUsers"]/lapsed_days)*remaining_days+monthly_kpi["uniqueUsers"]

  formatted = "------------------------ " + find_str + " ------------------------\n"
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
