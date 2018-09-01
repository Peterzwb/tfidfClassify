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

y_arrs = [31, 10, 21, 16, 36, 11, 19, 17, 30, 7, 2, 6, 27, 26, 25, 38, 4, 15, 37, 5, 9, 39, 29, 3, 40, 13, 32, 14, 18, 1, 24]
y_label_arrs = ['订单卡单', '受理报错', '改签不限量套餐', '工号权限/密码', '财辅报账支撑', '固定资产支撑', '拆机/销户系统校验不通过', '工程类项目支撑', '订单删单/撤单', '人像采集报错', 'IPTV退单、删单', '串码释放', '电子流与易支撑重复派单', '流量费用争议', '未实名', '采购支撑', 'OCS冷冻期解冻', '客户编码合并', '过户不成功', '一卡双号退订', '发票打印', '集团4G系统校验不通过', '缴费未到账(第三方平台问题)', 'ITV标清改高清/退单', '非实名/疑似虚假登记停机', '套餐后台修改', '订单待峻工', '套餐补录', '年付宽带到期停机', 'IPTV卡单(卓影平台问题）', '未及时到账']

def trainData(type):
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
        QUERY_ALL_ALARMOBJET += " question,label_2 "
        QUERY_ALL_ALARMOBJET += " FROM q_original_lable ";
        QUERY_ALL_ALARMOBJET += " WHERE 1=1 and status=1 "
        QUERY_ALL_ALARMOBJET += " and y= " + str(type)
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

def getTrainDataDict(top , type):
    data = trainData(type)
    data = numpy.array(data)[:, 0]
    seg = Seg()
    frequency = defaultdict(int)
    for i in range(len(data)):
        texts = checkData(data[i])
        texts = seg.cut_for_search(texts)
        for text in texts:
            if text == ' ':
                continue
            frequency[text] += 1
    #     out_texts.append([text for text in texts  if frequency[text] > 0])
    out_texts = []
    for w in sorted(frequency, key=frequency.get, reverse=True):
        out_texts.append({w:frequency[w]})
    return out_texts[0:top]

def getTrainAllDataDict(isCheck, type):
    data = trainData(type)
    train_data = numpy.array(data)[:, 0]
    lable = numpy.array(data)[:, 1]
    
    from sklearn.model_selection import train_test_split, KFold, cross_val_score
    X_train, X_test, Y_train, Y_test = train_test_split(train_data, lable, test_size=0.1, random_state=0, shuffle=True)
    
    out_texts = []
    seg = Seg()
    for i in range(len(X_train)):
        texts = X_train[i]
        if isCheck :
            texts = checkData(texts)
        texts = seg.cut_for_search(texts)
        texts = "".join(texts)  
        texts = texts.strip()
        texts = texts.replace("\n", "")
        texts = texts.replace("\r", "")
        texts = texts.replace(":", "") 
        out_texts.append(texts)
    return out_texts


def initDictData():
    f1 = open('ah_data_2.txt', 'w', encoding='utf-8')
    dict_arrs = []
    for i in range(len(y_arrs)):
        dicts = getTrainDataDict(True, y_arrs[i])
        dict_arr = []
        for dict in dicts:
            for (k, v) in dict.items():
                dict_arr.append(k)
        dict_arrs.append(' '.join(dict_arr))
        f1.writelines(str(y_label_arrs[i]) + ":" + ' '.join(dict_arr) + "\n")
# initDictData()        
        
def initAllData():
    f1 = open('ah_data_2.txt', 'w', encoding='utf-8')
    for i in range(len(y_arrs)):
        dicts = getTrainAllDataDict(True, y_arrs[i])
        f1.writelines(str(y_label_arrs[i]) + ":" + ' '.join(dicts) + "\n")

initAllData()



def readDictData(original_ss):
    keys = []
    values = []
    with open('ah_data_2.txt', encoding='utf-8') as f:
        line = f.readline()
        while line:
            print(line)
            data = line.split(':')
            keys.append(data[0])
            values.append(data[1])
            line = f.readline()
            
    original_ss.set_sentences(values)















