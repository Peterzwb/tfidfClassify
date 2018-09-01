'''
Created on 2018年8月8日

@author: Admin
'''

from LightMysql import LightMysql
import logging
import numpy
from zhcnSegment import Seg
from collections import defaultdict
from regular import checkData
from sentenceSimilarity import SentenceSimilarity

def trainData():
    # 配置信息，其中host, port, user, passwd, db为必需
    dbconfig = {'host':'127.0.0.1',
                'port': 3306,
                'user':'root',
                'passwd':'root',
                'db':'ah_q_text_classify',
                'charset':'utf8'}
    result = None
    try:
        QUERY_ALL_ALARMOBJET = " SELECT"
        QUERY_ALL_ALARMOBJET += " question ,label_2"
        QUERY_ALL_ALARMOBJET += " FROM q_original_lable ";
        QUERY_ALL_ALARMOBJET += " WHERE 1=1 and status=1 "
        db = LightMysql(dbconfig)  # 创建LightMysql对象，若连接超时，会自动重连
        sql_select = QUERY_ALL_ALARMOBJET
#         print(sql_select)
        result, colmun = db.query(sql_select, 'all')  # 返回有多少行
    except Exception as e:
        logging.error(e)
    finally:
        if(db != None):
            db.close()  # 操作结束，关闭对象
    return result    

def readDictData(original_ss, dict):
    values = []
    with open('ah_data_2.txt', encoding='utf-8') as f:
        line = f.readline()
        while line:
            data = line.split(':')
            dict[data[1]] = data[0]
            values.append(data[1])
            
            line = f.readline()
            
    original_ss.set_sentences(values)




# 用于周末的比对
data = trainData()
train_data = numpy.array(data)[:, 0]
lable = numpy.array(data)[:, 1]

from sklearn.model_selection import train_test_split, KFold, cross_val_score
X_train, X_test, Y_train, Y_test = train_test_split(train_data, lable, test_size=0.1, random_state=0, shuffle=True)
def dictTest():
    dict = {}
    seg = Seg()
    original_ss = SentenceSimilarity(seg)
    readDictData(original_ss, dict)
    original_ss.TfidfModel()
#     original_ss.LdaModel()
#     original_ss.LsiModel()
    total_data_len = len(X_test)
    success_len = 0
    f1 = open('ah_data_lsi.txt', 'w', encoding='utf-8')
    for i in range(len(X_test)):
        print("-------------------------------------")
        text = checkData(X_test[i]);
        text = "".join(seg.cut_for_search(text))
        print("测试内容: " + text)
        
        try :
            sentences = original_ss.similarityArray(text)
            sentences = sorted(sentences, key=lambda e:e.get_score(), reverse=True)
            count = 0
            for sentence  in  sentences:
                if sentence.get_score() > 0.9:
                    print(sentence.get_score())
                    
                if sentence.get_score() == 1.0:
                    count = count + 1
                    
            sentence = original_ss.similarity(text)
            if count < 2 and dict.get(sentence.get_origin_sentence()) == Y_test[i]:
                success_len = success_len + 1
            else:
                y = Y_test[i]
                f1.writelines("-------------------------------------\n")
                f1.writelines("测试内容: " + text + "\n")
                for sentence  in  sentences:
                    f1.writelines("匹配标签: 【" + dict.get(sentence.get_origin_sentence()) + "】 真实标签:【" + y + "】 评分: " + str(sentence.get_score()) + "\n")
        except Exception as e:
            print(e)
    print(success_len / total_data_len)

dictTest()



# from sklearn.model_selection import train_test_split, KFold, cross_val_score
# X_train, X_test, Y_train, Y_test = train_test_split(train_data, lable, test_size=0.1, random_state=0, shuffle=True)        
# 
# print("train len : %d" % len(X_train))
# print("test len : %d" % len(X_test))
# 
# # 根据类别拼接成一个句子
# dict = {}
# seg = Seg()
# for i in range(len(X_train)):
#     key = Y_train[i]
#     value = X_train[i]
#     text = checkData(value);
#     text = seg.cut_for_search(text)
#     print("".join(text))
# # print(success_len / total_data_len)














