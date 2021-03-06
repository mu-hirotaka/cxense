# encoding: UTF-8
import datetime
import json
import gspread
import oauth2client.client
import os

# sheet column number 
DAILY_PV_COL_NUM = 2
MONTHLY_PV_COL_NUM = 4
DAILY_UU_COL_NUM = 5
MONTHLY_UU_COL_NUM = 7
FLY_BYS_PV_COL_NUM = 8
OCCASIONALS_PV_COL_NUM = 9
REGULARS_PV_COL_NUM = 10
FAN_PV_COL_NUM = 11
FLY_BYS_UU_COL_NUM = 12
OCCASIONALS_UU_COL_NUM = 13
REGULARS_UU_COL_NUM = 14
FAN_UU_COL_NUM = 15
FROM_OTHER_PV_COL_NUM = 16
FROM_SOCIAL_PV_COL_NUM = 17
DIRECT_PV_COL_NUM = 18
FROM_SEARCH_PV_COL_NUM = 19
INTERNAL_PV_COL_NUM = 20
FROM_OTHER_UU_COL_NUM = 21
FROM_SOCIAL_UU_COL_NUM = 22
DIRECT_UU_COL_NUM = 23
FROM_SEARCH_UU_COL_NUM = 24
INTERNAL_UU_COL_NUM = 25
SMARTNEWS_PV_COL_NUM = 26
YAHOO_PV_COL_NUM = 27
TWITTER_PV_COL_NUM = 28
FACEBOOK_PV_COL_NUM = 29
SMARTNEWS_UU_COL_NUM = 30
YAHOO_UU_COL_NUM = 31
TWITTER_UU_COL_NUM = 32
FACEBOOK_UU_COL_NUM = 33
FLY_BYS_AVG_DURATION_COL_NUM = 34
OCCASIONALS_AVG_DURATION_COL_NUM = 35
REGULARS_AVG_DURATION_COL_NUM = 36
FAN_AVG_DURATION_COL_NUM = 37


def authorize():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'gss_key.json')))
  scope = ['https://spreadsheets.google.com/feeds']
  credentials = oauth2client.client.SignedJwtAssertionCredentials(key['client_email'], key['private_key'].encode(), scope)
  return gspread.authorize(credentials)

def write_down_daily_kpi(media_type, date_str, kpi):
  daily_kpi = kpi["daily"]["basic"]["data"]
  monthly_kpi = kpi["monthly"]["basic"]["data"]
  segment_kpi = kpi["daily"]["segment"]
  all_referrer_kpi = kpi["daily"]["referrer"]["all"]
  smartnews_kpi = kpi["daily"]["smartnews"]["basic"]["data"]
  yahoo_kpi = kpi["daily"]["yahoo"]["basic"]["data"]
  twitter_kpi = kpi["daily"]["twitter"]["basic"]["data"]
  facebook_kpi = kpi["daily"]["facebook"]["basic"]["data"]

  daily_pv = daily_kpi["events"]
  daily_uu = daily_kpi["uniqueUsers"]
  monthly_pv = monthly_kpi["events"]
  monthly_uu = monthly_kpi["uniqueUsers"]

  fly_bys_pv = segment_kpi["fly_bys"]["events"]
  fly_bys_uu = segment_kpi["fly_bys"]["uniqueUsers"]
  fly_bys_avg_duration = round(float(segment_kpi["fly_bys"]["activeTime"]) * fly_bys_pv / fly_bys_uu)
  occasionals_pv = segment_kpi["occasionals"]["events"]
  occasionals_uu = segment_kpi["occasionals"]["uniqueUsers"]
  occasionals_avg_duration = round(float(segment_kpi["occasionals"]["activeTime"]) * occasionals_pv / occasionals_uu)
  regulars_pv = segment_kpi["regulars"]["events"]
  regulars_uu = segment_kpi["regulars"]["uniqueUsers"]
  regulars_avg_duration = round(float(segment_kpi["regulars"]["activeTime"]) * regulars_pv / regulars_uu)
  fan_pv = segment_kpi["fan"]["events"]
  fan_uu = segment_kpi["fan"]["uniqueUsers"]
  fan_avg_duration = round(float(segment_kpi["fan"]["activeTime"]) * fan_pv / fan_uu)

  smartnews_pv = smartnews_kpi["events"]
  smartnews_uu = smartnews_kpi["uniqueUsers"]
  yahoo_pv = yahoo_kpi["events"]
  yahoo_uu = yahoo_kpi["uniqueUsers"]
  twitter_pv = twitter_kpi["events"]
  twitter_uu = twitter_kpi["uniqueUsers"]
  facebook_pv = facebook_kpi["events"]
  facebook_uu = facebook_kpi["uniqueUsers"]

  # 認証
  gc = authorize()
  workbook = gc.open("Daily_KPI")
  worksheet = workbook.worksheet(media_type)

  cell = worksheet.find(date_str)
  worksheet.update_cell(cell.row, DAILY_PV_COL_NUM, daily_pv)
  worksheet.update_cell(cell.row, MONTHLY_PV_COL_NUM, monthly_pv)
  worksheet.update_cell(cell.row, DAILY_UU_COL_NUM, daily_uu)
  worksheet.update_cell(cell.row, MONTHLY_UU_COL_NUM, monthly_uu)
  worksheet.update_cell(cell.row, FLY_BYS_PV_COL_NUM, fly_bys_pv)
  worksheet.update_cell(cell.row, OCCASIONALS_PV_COL_NUM, occasionals_pv)
  worksheet.update_cell(cell.row, REGULARS_PV_COL_NUM, regulars_pv)
  worksheet.update_cell(cell.row, FAN_PV_COL_NUM, fan_pv)

  worksheet.update_cell(cell.row, FLY_BYS_UU_COL_NUM, fly_bys_uu)
  worksheet.update_cell(cell.row, OCCASIONALS_UU_COL_NUM, occasionals_uu)
  worksheet.update_cell(cell.row, REGULARS_UU_COL_NUM, regulars_uu)
  worksheet.update_cell(cell.row, FAN_UU_COL_NUM, fan_uu)

  for host in all_referrer_kpi:
    host_name = host["item"]
    if host_name == "other":
      worksheet.update_cell(cell.row, FROM_OTHER_PV_COL_NUM, host["data"]["events"])
      worksheet.update_cell(cell.row, FROM_OTHER_UU_COL_NUM, host["data"]["uniqueUsers"])
    elif host_name == "social":
      worksheet.update_cell(cell.row, FROM_SOCIAL_PV_COL_NUM, host["data"]["events"])
      worksheet.update_cell(cell.row, FROM_SOCIAL_UU_COL_NUM, host["data"]["uniqueUsers"])
    elif host_name == "direct":
      worksheet.update_cell(cell.row, DIRECT_PV_COL_NUM, host["data"]["events"])
      worksheet.update_cell(cell.row, DIRECT_UU_COL_NUM, host["data"]["uniqueUsers"])
    elif host_name == "search":
      worksheet.update_cell(cell.row, FROM_SEARCH_PV_COL_NUM, host["data"]["events"])
      worksheet.update_cell(cell.row, FROM_SEARCH_UU_COL_NUM, host["data"]["uniqueUsers"])
    elif host_name == "internal":
      worksheet.update_cell(cell.row, INTERNAL_PV_COL_NUM, host["data"]["events"])
      worksheet.update_cell(cell.row, INTERNAL_UU_COL_NUM, host["data"]["uniqueUsers"])

  worksheet.update_cell(cell.row, SMARTNEWS_PV_COL_NUM, smartnews_pv)
  worksheet.update_cell(cell.row, SMARTNEWS_UU_COL_NUM, smartnews_uu)
  worksheet.update_cell(cell.row, YAHOO_PV_COL_NUM, yahoo_pv)
  worksheet.update_cell(cell.row, YAHOO_UU_COL_NUM, yahoo_uu)
  worksheet.update_cell(cell.row, TWITTER_PV_COL_NUM, twitter_pv)
  worksheet.update_cell(cell.row, TWITTER_UU_COL_NUM, twitter_uu)
  worksheet.update_cell(cell.row, FACEBOOK_PV_COL_NUM, facebook_pv)
  worksheet.update_cell(cell.row, FACEBOOK_UU_COL_NUM, facebook_uu)

  worksheet.update_cell(cell.row, FLY_BYS_AVG_DURATION_COL_NUM, fly_bys_avg_duration)
  worksheet.update_cell(cell.row, OCCASIONALS_AVG_DURATION_COL_NUM, occasionals_avg_duration)
  worksheet.update_cell(cell.row, REGULARS_AVG_DURATION_COL_NUM, regulars_avg_duration)
  worksheet.update_cell(cell.row, FAN_AVG_DURATION_COL_NUM, fan_avg_duration)

