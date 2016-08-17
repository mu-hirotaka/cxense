# encoding: UTF-8
import datetime
import sys
import time
import f1_gss_manipulator
import f1_slack_client
import f1_cxense_client
import f1_formatter

def unixtime(date):
  return int(time.mktime(date.timetuple()))

if __name__ == "__main__":
  if (len(sys.argv) > 3) or (len(sys.argv) < 2):
    print "Invalid arguments"
    sys.exit(1)
  elif len(sys.argv) == 2:
    media = sys.argv[1]
    today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    yesterday = today - datetime.timedelta(days = 1)
    start_date_for_pv = yesterday
    first_date_of_this_month = datetime.date(day=1, month=yesterday.month, year=yesterday.year)
    find_str = yesterday.strftime('%Y/%m/%d')
    # calc start_time, end_time
    start_time_for_pv = unixtime(yesterday)
    end_time_for_pv = start_time_for_pv + 60*60*24-1
    start_time_for_uu = unixtime(first_date_of_this_month)
    end_time_for_uu = unixtime(yesterday) + 60*60*24-1
  else:
    media = sys.argv[1]
    target_date = datetime.datetime.strptime(sys.argv[2], '%Y%m%d')
    start_date_for_pv = target_date
    first_date_of_this_month = datetime.date(day=1, month=target_date.month, year=target_date.year)
    find_str = target_date.strftime('%Y/%m/%d')
    # calc start_time, end_time
    start_time_for_pv = unixtime(start_date_for_pv)
    end_time_for_pv = start_time_for_pv + 60*60*24-1
    start_time_for_uu = unixtime(first_date_of_this_month)
    end_time_for_uu = end_time_for_pv

  # call api 
  if media == 'BK':
    daily_kpi = f1_cxense_client.bk_basic_kpi(start_time_for_pv, end_time_for_pv)
    monthly_kpi = f1_cxense_client.bk_basic_kpi(start_time_for_uu, end_time_for_uu)
    daily_segment_kpi = f1_cxense_client.bk_segment_kpi(start_time_for_pv, end_time_for_pv)
    monthly_segment_kpi = f1_cxense_client.bk_segment_kpi(start_time_for_uu, end_time_for_uu)
    # write to spreadsheet
    f1_gss_manipulator.update_bk_kpi(find_str, daily_kpi["data"], monthly_kpi["data"])
    # post to slack channel
    f1_slack_client.post_to_bk_analytics_channel(f1_formatter.for_bk_slack(find_str, daily_kpi["data"], monthly_kpi["data"], daily_segment_kpi, monthly_segment_kpi))
  elif media == 'SK':
    daily_kpi = f1_cxense_client.sk_basic_kpi(start_time_for_pv, end_time_for_pv)
    monthly_kpi = f1_cxense_client.sk_basic_kpi(start_time_for_uu, end_time_for_uu)
    # post to slack channel
    f1_slack_client.post_to_sk_analytics_channel(f1_formatter.for_sk_slack(find_str, daily_kpi["data"], monthly_kpi["data"]))
