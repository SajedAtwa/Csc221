from collections import defaultdict
from datetime import datetime
import pytz
import requests

class MTAFeed:

    def __init__(self):
        '''
        Initialize the class attributes and start retrieving the feed (by
        calling the class method self.refresh())
        '''
        self.Mta_URL = 'https://collector-otp-prod.camsys-apps.com/realtime/gtfsrt/ALL/alerts?type=json&apikey=qeqy84JE7hUKfaI0Lxm2Ttcm6ZA0bYrP'
        self.sub_alerts = []
        self._refreshed_time = None
        self.refresh()

    def refresh(self):
        '''
        This method refresh the data by downloading the feed, and extract the 
        alert based on the current timestamp (which is needed for checking
        active periods).
        '''
        Mta_data = requests.get(self.Mta_URL).json()
        East = pytz.timezone('US/Eastern')
        date = datetime.now().astimezone(East)
        Uno = Mta_data['entity']
        Dos = [entity['alert'] for entity in Uno for i in entity['alert']['informed_entity']
             if 'route_id' in i and i['agency_id']=='MTASBWY' and self.is_active(entity['alert'])]
        self.sub_alerts = list(map(lambda j: (j['transit_realtime.mercury_alert']['alert_type'], 
                                           j['informed_entity'][0]['route_id']), Dos))
        self._refreshed_time = date
        

    def getRefreshTime(self):
        '''
        This returns the datetime object of when we last refresh the feed. The
        datetime object should be timezone aware and in the same time zone of 
        the feed, 'US/Eastern'

        >>> feed.getRefreshTime().isoformat()
        '2023-03-29T09:00:28.789415-04:00'

        '''
        return self._refreshed_time

    def items(self, include_non_active=False):
        '''
        Returns an iterator to all alerts (including 'Non Active Alerts' if
        include_non_active is set to True). This should be a generator. The
        idea is to allow users to iterate through the alerts, e.g.:

        >>> for item in feed.items():
        '''
        dedict = defaultdict(set)
        no_active = set(list('1234567ABCDEFGJLMNQRSWZ')+['SI','SF','SR'])
        for alert_type, route_id in self.sub_alerts:
            dedict[alert_type].add(route_id)
            no_active.discard(route_id)
        if include_non_active:
            dedict['Non Active Alerts'] = no_active
        for s, a in dedict.items():
            yield s, a

    def is_active(self, alert):
        '''
        This method checks if the given alert is active at the current time.
        '''
        East = pytz.timezone('US/Eastern')
        date = datetime.now().astimezone(East)
        for l in alert['active_period']:
            start_time = datetime.fromtimestamp(l['start'], East)
            end_time = datetime.fromtimestamp(l.get('end', date.timestamp()), East)
            if start_time <= date <= end_time:
                return True
        return False

    def __getitem__(self, alert_type):
        '''
        We override this built-in operator to allow users to directly retrieve
        the set of lines associated with the alert_type, e.g.:

        >>> print(feed['Delays'])
        {'N', 'W'}

        '''
        if alert_type == 'Non Active Alerts':
          not_active = set(list('1234567ABCDEFGJLMNQRSWZ')+['SI','SF','SR'])
          for alert_type, route_id in self.sub_alerts:
              not_active.discard(route_id)
          return not_active
        else:
          empdict = defaultdict(set)
          for type_of_alert, route_id in self.sub_alerts:
              if type_of_alert == alert_type:
                  empdict[type_of_alert].add(route_id)
          return empdict[alert_type]

    def getLines(self):
        '''
        Return the set of all possible lines
        '''
        pass


if __name__=='__main__':
    Subway_feed = MTAFeed()
    print('Last refresh: ', Subway_feed.getRefreshTime().isoformat(' ')[:19])
    for status, lines in Subway_feed.items():
        print(status, ':', ' '.join(sorted(lines)))
    no_active = 'Non Active Alerts'
    print(no_active, ':', ' '.join(sorted(Subway_feed[no_active])))