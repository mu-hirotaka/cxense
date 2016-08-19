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

  daily_pv = daily_kpi["events"]
  daily_uu = daily_kpi["uniqueUsers"]
  monthly_pv = monthly_kpi["events"]
  monthly_uu = monthly_kpi["uniqueUsers"]

  fly_bys_pv = segment_kpi["fly_bys"]["events"]
  fly_bys_uu = segment_kpi["fly_bys"]["uniqueUsers"]
  occasionals_pv = segment_kpi["occasionals"]["events"]
  occasionals_uu = segment_kpi["occasionals"]["uniqueUsers"]
  regulars_pv = segment_kpi["regulars"]["events"]
  regulars_uu = segment_kpi["regulars"]["uniqueUsers"]
  fan_pv = segment_kpi["fan"]["events"]
  fan_uu = segment_kpi["fan"]["uniqueUsers"]

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

