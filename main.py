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
    date_str = yesterday.strftime('%Y/%m/%d')
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
    date_str = target_date.strftime('%Y/%m/%d')
    # calc start_time, end_time
    start_time_for_pv = unixtime(start_date_for_pv)
    end_time_for_pv = start_time_for_pv + 60*60*24-1
    start_time_for_uu = unixtime(first_date_of_this_month)
    end_time_for_uu = end_time_for_pv

  # call api 
  if media == 'BK':
    # request api
    daily_kpi = f1_cxense_client.basic_kpi(media, start_time_for_pv, end_time_for_pv)
    monthly_kpi = f1_cxense_client.basic_kpi(media, start_time_for_uu, end_time_for_uu)
    segment_kpi = f1_cxense_client.segment_kpi(media, start_time_for_pv, end_time_for_pv)

    all_referrer_kpi = f1_cxense_client.basic_kpi_for_each_referrer(media, start_time_for_pv, end_time_for_pv)
    search_referrer_kpi = f1_cxense_client.basic_kpi_from_search(media, start_time_for_pv, end_time_for_pv)
    social_referrer_kpi = f1_cxense_client.basic_kpi_from_social(media, start_time_for_pv, end_time_for_pv)
    other_referrer_kpi = f1_cxense_client.basic_kpi_from_other(media, start_time_for_pv, end_time_for_pv)

    smartnews_kpi = f1_cxense_client.basic_kpi_from_smartnews(media, start_time_for_pv, end_time_for_pv)
    smartnews_ranking = f1_cxense_client.url_uu_ranking_from_smartnews(media, start_time_for_pv, end_time_for_pv)
    yahoo_kpi = f1_cxense_client.basic_kpi_from_yahoo(media, start_time_for_pv, end_time_for_pv)
    yahoo_ranking = f1_cxense_client.url_uu_ranking_from_yahoo(media, start_time_for_pv, end_time_for_pv)
    twitter_kpi = f1_cxense_client.basic_kpi_from_twitter(media, start_time_for_pv, end_time_for_pv)
    twitter_ranking = f1_cxense_client.url_uu_ranking_from_twitter(media, start_time_for_pv, end_time_for_pv)
    facebook_kpi = f1_cxense_client.basic_kpi_from_facebook(media, start_time_for_pv, end_time_for_pv)
    facebook_ranking = f1_cxense_client.url_uu_ranking_from_facebook(media, start_time_for_pv, end_time_for_pv)

    kpi = {
        "daily": {
          "basic": daily_kpi,
          "segment": segment_kpi,
          "referrer": {
            "all": all_referrer_kpi,
            "search": search_referrer_kpi,
            "social": social_referrer_kpi,
            "other": other_referrer_kpi
          },
          "smartnews": {
            "basic": smartnews_kpi,
            "ranking": smartnews_ranking
          },
          "yahoo": {
            "basic": yahoo_kpi,
            "ranking": yahoo_ranking
          },
          "twitter": {
            "basic": twitter_kpi,
            "ranking": twitter_ranking
          },
          "facebook": {
            "basic": facebook_kpi,
            "ranking": facebook_ranking
          }
        },
        "monthly": {
          "basic": monthly_kpi
        },
    }

    # write to spreadsheet
    f1_gss_manipulator.write_down_daily_kpi(media, date_str, kpi)

    # post to slack channel
    f1_slack_client.post_to_channel(media, f1_formatter.format_for_slack(media, date_str, kpi))

  elif media == 'SK':
    # request api
    daily_kpi = f1_cxense_client.basic_kpi(media, start_time_for_pv, end_time_for_pv)
    monthly_kpi = f1_cxense_client.basic_kpi(media, start_time_for_uu, end_time_for_uu)
    segment_kpi = f1_cxense_client.segment_kpi(media, start_time_for_pv, end_time_for_pv)

    all_referrer_kpi = f1_cxense_client.basic_kpi_for_each_referrer(media, start_time_for_pv, end_time_for_pv)
    search_referrer_kpi = f1_cxense_client.basic_kpi_from_search(media, start_time_for_pv, end_time_for_pv)
    social_referrer_kpi = f1_cxense_client.basic_kpi_from_social(media, start_time_for_pv, end_time_for_pv)
    other_referrer_kpi = f1_cxense_client.basic_kpi_from_other(media, start_time_for_pv, end_time_for_pv)

    smartnews_kpi = f1_cxense_client.basic_kpi_from_smartnews(media, start_time_for_pv, end_time_for_pv)
    smartnews_ranking = f1_cxense_client.url_uu_ranking_from_smartnews(media, start_time_for_pv, end_time_for_pv)
    yahoo_kpi = f1_cxense_client.basic_kpi_from_yahoo(media, start_time_for_pv, end_time_for_pv)
    yahoo_ranking = f1_cxense_client.url_uu_ranking_from_yahoo(media, start_time_for_pv, end_time_for_pv)
    twitter_kpi = f1_cxense_client.basic_kpi_from_twitter(media, start_time_for_pv, end_time_for_pv)
    twitter_ranking = f1_cxense_client.url_uu_ranking_from_twitter(media, start_time_for_pv, end_time_for_pv)
    facebook_kpi = f1_cxense_client.basic_kpi_from_facebook(media, start_time_for_pv, end_time_for_pv)
    facebook_ranking = f1_cxense_client.url_uu_ranking_from_facebook(media, start_time_for_pv, end_time_for_pv)

    kpi = {
        "daily": {
          "basic": daily_kpi,
          "segment": segment_kpi,
          "referrer": {
            "all": all_referrer_kpi,
            "search": search_referrer_kpi,
            "social": social_referrer_kpi,
            "other": other_referrer_kpi
          },
          "smartnews": {
            "basic": smartnews_kpi,
            "ranking": smartnews_ranking
          },
          "yahoo": {
            "basic": yahoo_kpi,
            "ranking": yahoo_ranking
          },
          "twitter": {
            "basic": twitter_kpi,
            "ranking": twitter_ranking
          },
          "facebook": {
            "basic": facebook_kpi,
            "ranking": facebook_ranking
          }
        },
        "monthly": {
          "basic": monthly_kpi
        },
    }

    # write to spreadsheet
    f1_gss_manipulator.write_down_daily_kpi(media, date_str, kpi)

    # post to slack channel
    f1_slack_client.post_to_channel(media, f1_formatter.format_for_slack(media, date_str, kpi))

  elif media == 'BBK':
    # request api
    daily_kpi = f1_cxense_client.basic_kpi(media, start_time_for_pv, end_time_for_pv)
    monthly_kpi = f1_cxense_client.basic_kpi(media, start_time_for_uu, end_time_for_uu)
    segment_kpi = f1_cxense_client.segment_kpi(media, start_time_for_pv, end_time_for_pv)

    all_referrer_kpi = f1_cxense_client.basic_kpi_for_each_referrer(media, start_time_for_pv, end_time_for_pv)
    search_referrer_kpi = f1_cxense_client.basic_kpi_from_search(media, start_time_for_pv, end_time_for_pv)
    social_referrer_kpi = f1_cxense_client.basic_kpi_from_social(media, start_time_for_pv, end_time_for_pv)
    other_referrer_kpi = f1_cxense_client.basic_kpi_from_other(media, start_time_for_pv, end_time_for_pv)

    smartnews_kpi = f1_cxense_client.basic_kpi_from_smartnews(media, start_time_for_pv, end_time_for_pv)
    smartnews_ranking = f1_cxense_client.url_uu_ranking_from_smartnews(media, start_time_for_pv, end_time_for_pv)
    yahoo_kpi = f1_cxense_client.basic_kpi_from_yahoo(media, start_time_for_pv, end_time_for_pv)
    yahoo_ranking = f1_cxense_client.url_uu_ranking_from_yahoo(media, start_time_for_pv, end_time_for_pv)
    twitter_kpi = f1_cxense_client.basic_kpi_from_twitter(media, start_time_for_pv, end_time_for_pv)
    twitter_ranking = f1_cxense_client.url_uu_ranking_from_twitter(media, start_time_for_pv, end_time_for_pv)
    facebook_kpi = f1_cxense_client.basic_kpi_from_facebook(media, start_time_for_pv, end_time_for_pv)
    facebook_ranking = f1_cxense_client.url_uu_ranking_from_facebook(media, start_time_for_pv, end_time_for_pv)

    kpi = {
        "daily": {
          "basic": daily_kpi,
          "segment": segment_kpi,
          "referrer": {
            "all": all_referrer_kpi,
            "search": search_referrer_kpi,
            "social": social_referrer_kpi,
            "other": other_referrer_kpi
          },
          "smartnews": {
            "basic": smartnews_kpi,
            "ranking": smartnews_ranking
          },
          "yahoo": {
            "basic": yahoo_kpi,
            "ranking": yahoo_ranking
          },
          "twitter": {
            "basic": twitter_kpi,
            "ranking": twitter_ranking
          },
          "facebook": {
            "basic": facebook_kpi,
            "ranking": facebook_ranking
          }
        },
        "monthly": {
          "basic": monthly_kpi
        },
    }

    # write to spreadsheet
    f1_gss_manipulator.write_down_daily_kpi(media, date_str, kpi)

    # post to slack channel
    f1_slack_client.post_to_channel(media, f1_formatter.format_for_slack(media, date_str, kpi))
