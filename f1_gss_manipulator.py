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

def update_bk_kpi(find_str, daily_kpi, monthly_kpi):
  pv = daily_kpi["events"]
  uu = daily_kpi["uniqueUsers"]
  pv_sum = monthly_kpi["events"]
  uu_sum = monthly_kpi["uniqueUsers"]

  # 認証
  gc = authorize()
  workbook = gc.open("BK_KPI")
  worksheet = workbook.worksheet("KPI")
  # カラム番号
  PV_COL_NUM = 2
  PV_SUM_COL_NUM = 5
  UU_COL_NUM = 6
  UU_SUM_COL_NUM = 7
  try:
    cell = worksheet.find(find_str)
    worksheet.update_cell(cell.row, PV_COL_NUM, pv)
    worksheet.update_cell(cell.row, PV_SUM_COL_NUM, pv_sum)
    worksheet.update_cell(cell.row, UU_COL_NUM, uu)
    worksheet.update_cell(cell.row, UU_SUM_COL_NUM, uu_sum)
  except Exception as e:
    print '--- Error ---'
    print 'type:' + str(type(e))
    print 'message:' + e.message
    print '-------------'

def update_sk_kpi(find_str, daily_kpi, monthly_kpi):
  pass
