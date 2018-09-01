# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 16:55:24 2018

@author: Administrator
"""

import jieba
from gensim import corpora,models,similarities
import getData 

#获得原数据（已分词，去停词，加语料
getdata = getData.getData()
data_origin = getdata.read_text(word_type=1)
getdata.jiebaNWored()
       
data_seg = getdata.pretreatment(data_type=2)
data_seg = data_seg.split("\n")
for i in range(0,len(data_seg)):
    data_seg[i] = data_seg[i].split(" ")
    data_seg[i].remove("")
   
#获取预处理后的问题   
test_test = "CRM宽带资源的地址在哪里"
sentence = getdata.testWord(sentence=test_test)


dictionary = corpora.Dictionary(data_seg)#这就是一个词袋，就是以序号为键以单词为值的字典
dictionary.keys()
dictionary.token2id

corpus = [dictionary.doc2bow(doc) for doc in data_seg]#编号、频次
test_corpus = dictionary.doc2bow(sentence)#测试句子的词表示

tfidf = models.TfidfModel(corpus)
tfidf[test_corpus]#词tiidf值

index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
sim = index[tfidf[test_corpus]]
sim
sorted(enumerate(sim), key=lambda item: -item[1])