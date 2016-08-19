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
  daily_pv = daily_kpi["events"]
  daily_uu = daily_kpi["uniqueUsers"]
  monthly_pv = monthly_kpi["events"]
  monthly_uu = monthly_kpi["uniqueUsers"]

  # 認証
  gc = authorize()
  workbook = gc.open("Daily_KPI")
  worksheet = workbook.worksheet(media_type)

  # カラム番号
  DAILY_PV_COL_NUM = 2
  MONTHLY_PV_COL_NUM = 4
  DAILY_UU_COL_NUM = 5
  MONTHLY_UU_COL_NUM = 7

  cell = worksheet.find(date_str)
  worksheet.update_cell(cell.row, DAILY_PV_COL_NUM, daily_pv)
  worksheet.update_cell(cell.row, MONTHLY_PV_COL_NUM, monthly_pv)
  worksheet.update_cell(cell.row, DAILY_UU_COL_NUM, daily_uu)
  worksheet.update_cell(cell.row, MONTHLY_UU_COL_NUM, monthly_uu)

