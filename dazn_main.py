# encoding: UTF-8
import datetime
import sys
import time
import dazn_gss_manipulator

def unixtime(date):
  return int(time.mktime(date.timetuple()))

if __name__ == "__main__":
  if (len(sys.argv) > 2) or (len(sys.argv) < 1):
    print "Invalid arguments"
    sys.exit(1)
  elif len(sys.argv) == 1:
    today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    eight_days_ago = today - datetime.timedelta(days = 8)
    start_time = unixtime(eight_days_ago)
    end_time = start_time + 60*60*24*8 - 1
    dazn_gss_manipulator.write_down_weekly_kpi(start_time, end_time)
  else:
    target_date = datetime.datetime.strptime(sys.argv[1], '%Y%m%d')
    eight_days_ago = target_date - datetime.timedelta(days = 8)
    start_time = unixtime(eight_days_ago)
    end_time = start_time + 60*60*24*8 - 1
    dazn_gss_manipulator.write_down_weekly_kpi(start_time, end_time)
