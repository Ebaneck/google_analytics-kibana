"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
from datetime import timedelta

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '/home/debian/google_analytics-kibana/key.json'
VIEW_ID = '147428382'


def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
	'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{'name': 'ga:nthDay'}]
        }]
      }
  ).execute()



# Google Analytics returns nthDay with leading 0's, get rid of them
# here and convert to date stamps
def ConvertDays(r):

    for iRow in range(len(r["reports"][0]["data"]["rows"])):
        day = r["reports"][0]["data"]["rows"][iRow]["dimensions"][0]
        day = int(day)
        day = datetime.strftime(datetime.now() - timedelta(days= 30 - day), '%d %b %Y 06:00:00')
        #print r["reports"][0]["data"]["rows"][iRow]["dimensions"][0] + " = " + day

        r["reports"][0]["data"]["rows"][iRow]["dimensions"][0] = day

    return r


# use json.dumps to dump output, this should be the only
# thing that prints when logstash runs the code
def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  response = ConvertDays(response)
  print json.dumps(response)
  return response


if __name__ == '__main__':
  main()

