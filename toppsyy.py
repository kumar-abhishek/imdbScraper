import requests
import simplejson as json
from math import ceil
import time
import csv
import HTMLParser

API_HOST = 'http://otter.topsy.com'
API_KEY = ''
        
"""
use topsy API to download tweets from twitter
"""
        
class Result(object):
    def __init__(self, request):
        self._request = request
        self._data = json.loads(request.content)
        self.request = self._data['request']
        self.response = self._data['response']
        
    def sanitize_string(self, string):
        #remove new line character from string
        string = string.replace("\n","")
        #escape the HTML special chars
        parser = HTMLParser.HTMLParser()
        return parser.unescape(string)
                    
    def dump_json_to_file(self):
        list_dicts = (self.response['list'])
        csv_file =  csv.writer(open('data.csv','a'), delimiter='|')
        csv_file.writerow(["content", "target_birth_date", "score", "trackback_author_name", "trackback_author_nick"])
        for mydict in list_dicts:
            csv_file.writerow([self.sanitize_string(mydict['content']),mydict['target_birth_date'],mydict['score'], self.sanitize_string(mydict['trackback_author_name']), self.sanitize_string(mydict['trackback_author_nick'])])
            
            
class Topsy(object):
    def __init__(self, api_key=''):
        self._api_key = api_key or API_KEY
        self._api_host = API_HOST

    def _get(self, resource='', **params):
        params['apikey'] = self._api_key
        url = '%s/%s.json' % (self._api_host, resource)
        r = requests.get(url, params=params)
        return Result(request=r)

    
    def search_helper(self, q, page, perpage, maxtime, mintime):
        #current unix timestamp 
        date = int(time.time())  
        return self._get('search', q=q, allow_lang='en', type='tweet', page=page, perpage=perpage, maxtime=maxtime, mintime=mintime, order=date)
        
    def search(self, q='', Type=''):
        """
        1354337580 corresponds to Sat, 01 Dec 2012 04:53:00 GMT
        1207008000 corresponds to 1st april 2008 , 12am
        current unix time: 1350103730
        some very famous movies like 'the dark knight' can have 10k tweets in ~4 days: through topsy
        you can retrieve at max 10 pages each page with a max of 100 tweets=> max 10k tweets can be 
        downloaded in one API call.
        The diff in mintime and maxtime now is just 3 days. 
        """
        mintime = 1349892314
        maxtime = 1350104730
        #diff = maxtime - mintime
        result = self.search_helper(q, 1, 100, maxtime, mintime)
        #while(1):
        num_results = result.response['total']
        print num_results
        result.dump_json_to_file()
        num_pages_left = int(ceil((num_results-100.0)/100.0))
        print "num_pages_left: " , num_pages_left
        if num_pages_left >= 1:
            for page in range(2,num_pages_left+2):
                print 'querying for page: ', page
                result = self.search_helper(q, page, 100, maxtime, mintime)
                result.dump_json_to_file()
        
        #mintime -= diff
        #maxtime -= diff
        
def main():
    topsy = Topsy()
    topsy.search('forrest gump') 
    
if __name__ == '__main__':
    main()
