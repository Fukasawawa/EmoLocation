from mlask import MLAsk
import numpy as np
import twitter, geo_search

emotion_analyzer = MLAsk()

def ask(location):
    t = twitter.tweet_search(location)
    t_work = geo_search.tweet_search(location)
    try:
        for x in t_work:
            if(np.any(t==x[0])== False):
                t = np.insert(t, 1, x, axis=0)
        # emotion = {'yorokobi':0, 'ikari':0, 'aware':0, 'kowa':0, 'haji':0, 'suki':0, 'iya':0, 'takaburi':0, 'yasu':0, 'odoroki':0, 'location':location}
        # for x in range(len(t)):

        t = t.tolist()
    except:
        return None
    new_list=[]
    x=0
    for tweet in t:
        emo_list = emotion_analyzer.analyze(tweet[0])
        if(emo_list['emotion'] != None):
            # emotion[emo_list['representative'][0]] += 1
            tweet.append(emo_list['representative'][0])
            tweet.append(emo_list['intension']+1)
            new_list.append(tweet)
    # print(new_list[:50])
    return new_list

# ask("盛岡駅")
