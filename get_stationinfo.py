import re
import urllib
import logging
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error   import HTTPError, URLError

def dms2deg(degree, minute, second):
    """
    Transform DMS-notation into DEG-notation.
    
    Parameters
    ----------
    degree : int
    minute : int
    second : float
    
    Returns
    -------
    deg : float
    """
    deg = degree + minute/60 + second/3600
    return deg

def get_stationinfo(article_url, wiki_url='https://ja.wikipedia.org'):
    """
    Get Station Infomation from Wikipedia.
    
    Parameters
    ----------
    article_url : str
    
    wiki_url : str, optional
    
    Returns
    -------
    station_info : dict
    
    Examples
    --------
    >>> get_stationinfo('/wiki/鹿児島駅')
    {'name' : '鹿児島駅'
    ,'lat'  : 31.601497222
    ,'lng'  : 130.56311388
    ,'passengers' : 1597
    ,'next_article' : ['/wiki/鹿児島中央駅'
                      ,'/wiki/竜ヶ水'
                      ,'/wiki/桜島浅橋通停留場']}                      
    """
    station_name = None
    latitude     = None
    longitude    = None
    passengers   = None
    passengers_list = []
    next_urls    = set()
    logging.debug('##################################')
    logging.debug('Start get_stationinfo '+article_url)    
    logging.debug('##################################')
    target_url = wiki_url + urllib.parse.quote(article_url)
    html = urlopen(target_url)
    bsObj = BeautifulSoup(html.read(),'html.parser')
    infoboxes = bsObj.find_all("table", {"class":"infobox bordered"})
    logging.debug('Number of infoboxes : '+str(len(infoboxes)))
    for infobox in infoboxes:
        rows = infobox.find_all('tr',{'class':'','itemprop':'','style':''})

        """Get Station Name"""
        if station_name is None:
            """First InfoBox."""
            station_name = rows[0].text
            logging.debug('Station Name        : '+station_name)            

        """Get Location Data"""
        if latitude is None:
            for row in rows:
                if ('北緯' in row.text):
                    dms_lat  = row.text.split('北緯')[1].split('秒')[0]
                    degree = float(dms_lat.split('度')[0])
                    minute = float(dms_lat.split('度')[1].split('分')[0])
                    second = float(dms_lat.split('度')[1].split('分')[1])
                    latitude = dms2deg(degree,minute,second)
                    dms_lng = row.text.split('東経')[1].split('秒')[0]
                    degree = float(dms_lng.split('度')[0])
                    minute = float(dms_lng.split('度')[1].split('分')[0])
                    second = float(dms_lng.split('度')[1].split('分')[1])
                    longitude = dms2deg(degree,minute,second)
                    logging.debug('Location(lat)       : '+str(latitude))
                    logging.debug('Location(lng)       : '+str(longitude))                    
        
        """Get Next URL  """
        for row in rows:
            if ('◄' in row.text or '►' in row.text):
                objs=row.find_all('a',href=re.compile('^(/wiki/)((?!:).)*$'))
                urls=[urllib.parse.unquote(o.attrs['href']) for o in objs]
                for url in urls:
                    logging.debug('Add Article         : '+url)
                    next_urls.add(url)

        """Get Passengers"""
        for row in rows:
            if('人員' in row.text):
                passengers_list.append(int(re.sub('\\D','',row.text.split('人/日')[0])))
    passengers = max(passengers_list) if passengers_list != [] else 0
    logging.debug('Passengers          : '+str(passengers))
    logging.debug('##################################')
    logging.debug('End get_stationinfo '+article_url)    
    logging.debug('##################################')
    return {
        'name' : station_name,
        'lat'  : latitude,
        'lng'  : longitude,
        'passengers': passengers,
        'next_urls' : next_urls
    }

    
if __name__ == '__main__':
    import random
    logging.basicConfig(level=logging.DEBUG)
    article_url_list = ['/wiki/東京駅',\
                        '/wiki/淀屋橋駅',\
                        '/wiki/扇町駅 (大阪府)']
    urls = set()
    article_url = article_url_list[2]
    while True:
        urls.add(article_url)
        dic = get_stationinfo(article_url)
        article_url = random.choice(list(dic['next_urls']))
        print(urls)
