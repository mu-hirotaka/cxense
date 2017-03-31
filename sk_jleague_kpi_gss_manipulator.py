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
TAG_COL_NUM = 7

TAGS = [u'Jリーグ・試合情報',u'Jリーグ・コラム',u'Jリーグ・ニュース',u'Jリーグ・PR']

def authorize():
  key = json.load(open(os.path.join(os.path.expanduser('~'), '.cxense', 'gss_key.json')))
  scope = ['https://spreadsheets.google.com/feeds']
  credentials = oauth2client.client.SignedJwtAssertionCredentials(key['client_email'], key['private_key'].encode(), scope)
  return gspread.authorize(credentials)

def write_down_weekly_kpi(start_time, end_time):

  # 認証
  gc = authorize()
  workbook = gc.open("SK_JLEAGUE_TAG_KPI")
  worksheet = workbook.worksheet('list')

  cell_list = worksheet.findall('ing')
  for cell in cell_list:
    # status 以外のセルは無視
    if cell.col != STATUS_COL_NUM:
      continue

    url_cell = worksheet.cell(cell.row, URL_COL_NUM)
    # api access
    kpi_res = f1_cxense_client.pv_and_uu_by_url('SK', start_time, end_time, url_cell.value)
    meta_res = f1_cxense_client.content_by_url('SK', url_cell.value)

    tag = get_tag(meta_res["fields"])

    worksheet.update_cell(cell.row, PV_COL_NUM, kpi_res["data"]["events"])
    worksheet.update_cell(cell.row, UU_COL_NUM, kpi_res["data"]["uniqueUsers"])
    worksheet.update_cell(cell.row, TITLE_COL_NUM, kpi_res["title"])
    worksheet.update_cell(cell.row, TAG_COL_NUM, tag)
    worksheet.update_cell(cell.row, cell.col, 'done')

def get_tag(fields):
    for field in fields:
      if field["field"] == "frm-cxtag":
        if isinstance(field["value"], basestring):
          return field["value"]
        elif isinstance(field["value"], list):
          for tag in TAGS:
            if tag in field["value"]:
              return tag
          return field["value"][0]
    return "no tag"
