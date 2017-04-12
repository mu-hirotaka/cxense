# encoding: UTF-8
import datetime
import json
import gspread
import oauth2client.client
import os
import f1_cxense_client

# sheet column number 
STATUS_COL_NUM = 1
DATE_COL_NUM = 2
URL_COL_NUM = 3
TITLE_COL_NUM = 4
PV_COL_NUM = 5
UU_COL_NUM = 6

def authorize():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'gss_key.json')))
  scope = ['https://spreadsheets.google.com/feeds']
  credentials = oauth2client.client.SignedJwtAssertionCredentials(key['client_email'], key['private_key'].encode(), scope)
  return gspread.authorize(credentials)

def write_down_weekly_kpi(start_time, end_time):

  # 認証
  gc = authorize()
  workbook = gc.open("BBK_NEWS_KPI")
  worksheet = workbook.worksheet('news')

  cell_list = worksheet.findall('ing')
  for cell in cell_list:
    # status 以外のセルは無視
    if cell.col != STATUS_COL_NUM:
      continue

    url_cell = worksheet.cell(cell.row, URL_COL_NUM)
    # api access
    response = f1_cxense_client.pv_and_uu_by_url('BBK', start_time, end_time, url_cell.value)

    worksheet.update_cell(cell.row, PV_COL_NUM, response["data"]["events"])
    worksheet.update_cell(cell.row, UU_COL_NUM, response["data"]["uniqueUsers"])
    worksheet.update_cell(cell.row, TITLE_COL_NUM, response["title"])
    worksheet.update_cell(cell.row, cell.col, 'done')

