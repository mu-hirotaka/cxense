# encoding: UTF-8
import datetime
import json
import gspread
import oauth2client.client
import os

def authorize():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'gss_key.json')))
  scope = ['https://spreadsheets.google.com/feeds']
  credentials = oauth2client.client.SignedJwtAssertionCredentials(key['client_email'], key['private_key'].encode(), scope)
  return gspread.authorize(credentials)

def write_down_daily_kpi(media_type, date_str, kpi):
  daily_kpi = kpi["daily"]["basic"]["data"]
  monthly_kpi = kpi["monthly"]["basic"]["data"]
  segment_kpi = kpi["daily"]["segment"]
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

  # カラム番号
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

