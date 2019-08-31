import MeCab
from operator import itemgetter
import math
#file = open("sansa.txt", "w")

def cause(t, location):
    emo_cause_noun = {'yorokobi':{}, 'ikari':{}, 'aware':{}, 'kowa':{}, 'haji':{}, 'suki':{}, 'iya':{}, 'takaburi':{}, 'yasu':{}, 'odoroki':{}}
    emo_cause_noun_count = {'yorokobi':{}, 'ikari':{}, 'aware':{}, 'kowa':{}, 'haji':{}, 'suki':{}, 'iya':{}, 'takaburi':{}, 'yasu':{}, 'odoroki':{}}
    emo_cause_verb = {'yorokobi':{}, 'ikari':{}, 'aware':{}, 'kowa':{}, 'haji':{}, 'suki':{}, 'iya':{}, 'takaburi':{}, 'yasu':{}, 'odoroki':{}}
    emo_cause_verb_count = {'yorokobi':{}, 'ikari':{}, 'aware':{}, 'kowa':{}, 'haji':{}, 'suki':{}, 'iya':{}, 'takaburi':{}, 'yasu':{}, 'odoroki':{}}
    cause_point = {'yorokobi':{}, 'ikari':{}, 'aware':{}, 'kowa':{}, 'haji':{}, 'suki':{}, 'iya':{}, 'takaburi':{}, 'yasu':{}, 'odoroki':{}}
    cause_word = {'yorokobi':[], 'ikari':[], 'aware':[], 'kowa':[], 'haji':[], 'suki':[], 'iya':[], 'takaburi':[], 'yasu':[], 'odoroki':[]}
    m = MeCab.Tagger('')
    # t = ml_ask.ask(location)
    #pickle.dump(t, file)
    for i in t:
        if(i[1] == "100m"):
            score = 50
        elif(i[1] == "500m"):
            score = 10
        elif(i[1] == "1km"):
            score = 5
        else:
            score = 1
        # result = m.parse(format_text(i[0])).split('\n')
        result = m.parse(i[0]).split('\n')
        #単語の個数計算
        for word in result:
            word_info = word.split('\t')
            #print(len(word))
            if(len(word_info) >= 2):
                clazz = word_info[1].split(',')
                if((clazz[6] != '*') and (clazz[6] != location)):
                    if(clazz[0] == "名詞"):
                        if clazz[6] in emo_cause_noun_count[i[4]]:
                            emo_cause_noun_count[i[4]][clazz[6]] += i[5]
                        else:
                            emo_cause_noun_count[i[4]][clazz[6]] = i[5]
                    elif((clazz[0] == "動詞") and (clazz[1] == "自立")):
                        #すでに単語登録されてるか
                        if clazz[6] in emo_cause_verb_count[i[4]]:
                            #登録されてたらカウントアップ
                            emo_cause_verb_count[i[4]][clazz[6]] += i[5]
                        else:
                            #登録されてなかったら新規登録
                            emo_cause_verb_count[i[4]][clazz[6]] = i[5]

    for i in t:
        #print(repr(i[0]), repr(format.format_text(i[0])))
        # result = m.parse(format_text(i[0])).split('\n')
        result = m.parse(i[0]).split('\n')
        #tf-idf値計算
        for word in result:
            word_info = word.split('\t')
            #print(len(word))
            if(len(word_info) >= 2):
                clazz = word_info[1].split(',')
                if((clazz[6] != '*') and (clazz[6] != location)):
                    if(clazz[0] == "名詞"):
                        #感情の中である単語の出現回数/ある感情に出現する単語数
                        tf = emo_cause_noun_count[i[4]][clazz[6]] / sum(emo_cause_noun_count[i[4]].values())
                        #分母
                        mother = 0
                        #文書に単語が含まれる個数（1つは必ず一致）
                        for e in ['yorokobi', 'ikari', 'aware', 'kowa', 'haji', 'suki', 'iya', 'takaburi', 'yasu', 'odoroki']:
                            if clazz[6] in emo_cause_noun_count[e]:
                                mother += 1
                        #全文書数/ある単語が含まれている文書数
                        idf = math.log10(10/mother)+1
                        #すでにtf-idf値が設定されているか
                        #print('A')
                        if clazz[6] not in emo_cause_noun[i[4]]:
                            #されてなければ新規登録
                            emo_cause_noun[i[4]][clazz[6]] = tf*idf
                        #elif emo_cause_noun[i[5]][clazz[6]] < tf*idf:
                        #    emo_cause_noun[i[5]][clazz[6]] = tf*idf
                    elif((clazz[0] == "動詞") and (clazz[1] == "自立")):
                        tf = emo_cause_verb_count[i[4]][clazz[6]] / sum(emo_cause_verb_count[i[4]].values())
                        mother = 0
                        for e in ['yorokobi', 'ikari', 'aware', 'kowa', 'haji', 'suki', 'iya', 'takaburi', 'yasu', 'odoroki']:
                            if clazz[6] in emo_cause_verb_count[e]:
                                mother += 1
                        idf = math.log10(10/mother)+1
                        if clazz[6] not in emo_cause_verb[i[4]]:
                            emo_cause_verb[i[4]][clazz[6]] = tf*idf
                        #elif emo_cause_verb[i[5]][clazz[6]] < tf*idf:
                        #    emo_cause_verb[i[5]][clazz[6]] = tf*idf
    for i in t:
        # result = m.parse(format_text(i[0])).split('\n')
        result = m.parse(i[0]).split('\n')
        point = 0
        point_cnt = 0
        for word in result:
            word_info = word.split('\t')
            #print(len(word))
            if(len(word_info) >= 2):
                clazz = word_info[1].split(',')
                if((clazz[6] != '*') and (clazz[6] != location)):
                    if(clazz[0] == "名詞"):
                        point += emo_cause_noun[i[4]][clazz[6]]
                        point_cnt += 1
                    elif((clazz[0] == "動詞") and (clazz[1] == "自立")):
                        point += emo_cause_verb[i[4]][clazz[6]]
                        point_cnt += 1
        #print(point, point_cnt)
        if(point != 0):
            cause_point[i[4]][i[0]] = int(point*100/point_cnt)
        else:
            cause_point[i[4]][i[0]] = 0.1


    for i in ['yorokobi', 'ikari', 'aware', 'kowa', 'haji', 'suki', 'iya', 'takaburi', 'yasu', 'odoroki']:
        # print(i)
        noun = sorted(emo_cause_noun[i].items(), key=itemgetter(1), reverse=True)[0:3]
        # print(noun)
        # cause_word[i].append(work[0].keys())

        verb=sorted(emo_cause_verb[i].items(), key=itemgetter(1), reverse=True)[0:3]
        # print(verb)
        # cause_word[i].append(work[0].keys())

        sent=sorted(cause_point[i].items(), key=itemgetter(1), reverse=True)[0:3]
        # print(sent)
        # cause_word[i].append(work[0].keys())

        noun_list=[]
        verb_list=[]
        sent_list=[]
        # print(len(noun))
        # print(len(verb))
        # print(len(sent))
        for x in range(len(noun)):
            noun_list.append(noun[x][0])
        for x in range(len(verb)):
            verb_list.append(verb[x][0])
        for x in range(len(sent)):
            sent_list.append(sent[x][0])

        cause_word[i].append(noun_list)
        cause_word[i].append(verb_list)
        cause_word[i].append(sent_list)

    return cause_word

# print(cause("盛岡駅"))
