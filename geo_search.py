# coding: UTF-8
import json, config
# import rm_emoji
import sys, codecs
import requests
import numpy as np
from requests_oauthlib import OAuth1Session
# from format import format_text

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

MAK=config.MAPS_API_KEY

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
# TwitterAPIのURL
# url = "https://api.twitter.com/1.1/geo/search.json"
sea_url = "https://api.twitter.com/1.1/search/tweets.json"
# MAPS_APIのURL
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?language=ja&address={}&key='+MAK
headers = {'content-type': 'application/json'}

def calc_dis(lon_a,lat_a,lon_b,lat_b):
    ra=6378.140  # equatorial radius (km)
    rb=6356.755  # polar radius (km)
    F=(ra-rb)/ra # flattening of the earth
    rad_lat_a=np.radians(lat_a)
    rad_lon_a=np.radians(lon_a)
    rad_lat_b=np.radians(lat_b)
    rad_lon_b=np.radians(lon_b)
    pa=np.arctan(rb/ra*np.tan(rad_lat_a))
    pb=np.arctan(rb/ra*np.tan(rad_lat_b))
    xx=np.arccos(np.sin(pa)*np.sin(pb)+np.cos(pa)*np.cos(pb)*np.cos(rad_lon_a-rad_lon_b))
    c1=(np.sin(xx)-xx)*(np.sin(pa)+np.sin(pb))**2/np.cos(xx/2)**2
    c2=(np.sin(xx)+xx)*(np.sin(pa)-np.sin(pb))**2/np.sin(xx/2)**2
    dr=F/8*(c1-c2)
    rho=ra*(xx+dr)
    return rho

def tweet_search(word):
    #月検索のための配列
    tuki = ['Jan', 'Feb', 'Mat', 'Apl', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    #tweetフォーマット設定
    work = 'ああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああ'
    tweet_list = np.array([[work, 'ああ', 'う', 'え']])

    maps_url = base_url.format(word)

    # 検証時は一回だけ動かしてあとは直打ちで緯度経度を入れる
    # 検証時
    location = requests.get(maps_url, headers=headers).json()
    # print(location)
    # location['results'][0]['address_components'][4]['short_name']=='JP'
    # print(location['results'][0]['address_components'][for x in range(len(location['results'][0]['address_components']))]['short_name']=='JP')
    # print(filter(location['results'][0]['address_components'][x]['short_name'], range(len(location['results'][0]['address_components'])))))
    # print(filter(lambda x:location['results'][0]['address_components'][x]['short_name'] == 'JP', range(len(location['results'][0]['address_components']))))
    if(u'results' in location and len(location['results']) > 0 and filter(lambda x:location['results'][0]['address_components'][x]['short_name'] == 'JP', range(len(location['results'][0]['address_components']))) != None):
        lat = location['results'][0]['geometry']['location']['lat']
        lng = location['results'][0]['geometry']['location']['lng']
    else:
        print("検索地点の名称が違うか検索地点が日本ではありません")
        return []
        # sys.exit()
    print(lat)
    print(lng)
    # 直打ち
    # lat=39.7014371
    # lng=141.136723
    # lat=35.632896
    # lng=139.880394

    old=''
    for x in range(10):

        #検索語と検索数を設定
        # params = {'lat' : 35.362222, 'long' : 138.731388, 'count' : 5, 'accuracy' : '5000m'}
        # params = {'q' : 'near: ' + word + ' within: 0.5km', 'count' : 3}
        ranges="1km"
        params = {'q' : ' -rt -bot', 'geocode' : str(lat) + ','+ str(lng) + ',' + ranges, 'count' : 100, 'until' : old}
        req = twitter.get(sea_url, params = params)
        #正常につながれば
        if req.status_code != 200:
            print("繋がりませんでした")
            exit()
        # Wed Jun 26 07:06:47 +0000 2019
        # print(req.text)
        search_timeline = json.loads(req.text)
        # ツイート数だけループ
        # print(len(search_timeline['statuses']))

        # もっとも古い
        # print(search_timeline['statuses'][-1]['created_at'])
        # 最新
        # print(search_timeline['statuses'][0]['created_at'])
        if(len(search_timeline['statuses']) > 1):
            work=search_timeline['statuses'][-1]['created_at'].split()
        else:
            print('ツイートはもうないよ')
            break
        # print(work)
        old=work[5] + '-' + str(tuki.index(work[1])+1) + '-' + work[2] + '_' + work[3] + '_UTC'
        # print(old)

        for tweet in search_timeline['statuses']:
            if(tweet['coordinates'] is not None):
                # print(tweet['coordinates']['coordinates'][0])
                # print(tweet['coordinates']['coordinates'][1])
                twi_lng=tweet['coordinates']['coordinates'][0]
                twi_lat=tweet['coordinates']['coordinates'][1]
            elif(tweet['place'] is not None):
                # print("placeの方")
                # print(tweet['place']['bounding_box']['coordinates'][0][0][0])
                # print(tweet['place']['bounding_box']['coordinates'][0][0][1])
                twi_lng=tweet['place']['bounding_box']['coordinates'][0][0][0]
                twi_lat=tweet['place']['bounding_box']['coordinates'][0][0][1]
            else:
                # print("continue")
                continue
            # print(tweet['coordinates']['coordinates'][1])
            #ツイート本文から絵文字を削除しMecabようにフォーマットしreturn
            distance = calc_dis(lng, lat, twi_lng, twi_lat)
            if(distance > 1):
                text_dis='5km'
            elif(distance > 0.5):
                text_dis='1km'
            elif(distance > 0.1):
                text_dis='500m'
            else:
                text_dis='100m'
            # add = [format_text(rm_emoji.remove_emoji(tweet['text'].translate(non_bmp_map))), text_dis]
            add = [tweet['text'].translate(non_bmp_map), text_dis]
            date = tweet['created_at']
            #print(add, date)
            month = tuki.index(date.split(' ')[1])+1
            if((month >= 12) or (month <= 2)):
                season = '冬'
            elif(month >= 9):
                season = '秋'
            elif(month >= 6):
                season = '夏'
            else:
                season = '春'
            add.append(season)

            hour = int(date.split(' ')[3].split(':')[0])
            if((hour >= 18) or (hour <= 3)):
                tzone = '夜'
            elif(hour >= 12):
                tzone = '昼'
            else:
                tzone = '朝'
            add.append(tzone)
            #print(add)
            # print(add)
            # add[0] = add[0].decode('utf-8')
            # add[0] = codecs.getwriter("utf-8")(add[0])
            # print(add)
            if(np.any(tweet_list==add[0])== False):
                tweet_list = np.insert(tweet_list, 1, add, axis=0)
            # tweet_list = np.insert(tweet_list, 1, ['つらみ', '100m', '春', '朝'], axis=0)


    tweet_list = np.delete(tweet_list, 0, 0)

    return tweet_list

#data = tweet_search("盛岡駅")
# print(data)
