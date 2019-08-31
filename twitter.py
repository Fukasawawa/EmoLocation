# coding: UTF-8
import json, config
# import rm_emoji
import sys
import numpy as np
from requests_oauthlib import OAuth1Session
# from format import format_text

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
url = "https://api.twitter.com/1.1/search/tweets.json"

def tweet_search(word):
    #月検索のための配列
    tuki = ['Jan', 'Feb', 'Mat', 'Apl', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    #tweetフォーマット設定
    work = 'ああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああ'
    tweet_list = np.array([[work, 'ああ', 'う', 'え']])

    old=''
    for x in range(10):

        #検索語と検索数を設定
        params = {'q' : '"' + word + '"' + ' -rt -bot', 'count' : 100, 'until' : old}
        req = twitter.get(url, params = params)
        #正常につながれば
        if req.status_code != 200:
            print("ERROR: %d" % req.status_code)
            exit()

        search_timeline = json.loads(req.text)

        if(len(search_timeline['statuses']) > 1):
            work=search_timeline['statuses'][-1]['created_at'].split()
        else:
            print('ツイートはもうないよ')
            break
        # print(work)
        old=work[5] + '-' + str(tuki.index(work[1])+1) + '-' + work[2] + '_' + work[3] + '_UTC'
        # print(old)

        #ツイート数だけループ
        for tweet in search_timeline['statuses']:
            #ツイート本文から絵文字を削除しMecabようにフォーマットしreturn
            # add = [format_text(rm_emoji.remove_emoji(tweet['text'].translate(non_bmp_map))), '1km']
            add = [tweet['text'].translate(non_bmp_map), '1km']
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

            if(np.any(tweet_list==add[0])== False):
                tweet_list = np.insert(tweet_list, 1, add, axis=0)
            # tweet_list = np.insert(tweet_list, 1, ['つらみ', '100m', '春', '朝'], axis=0)

        tweet_list = np.delete(tweet_list, 0, 0)

        return tweet_list


#data = tweet_search("盛岡駅")
#print(data)
