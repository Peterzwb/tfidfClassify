# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 10:23:53 2018

@author: Administrator
"""

import jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs
#import logging


class getData:
    def __init__(self):
        self.path = r"G:\项目1—人工智能客服\lda\data\data.txt"
        self.stopword = r"G:\项目1—人工智能客服\lda\data\stop_word.txt"
        self.newword = r"G:\项目1—人工智能客服\lda\data\dict.txt"
          
    def read_text(self , word_type):
        if word_type == 1:
            path = self.path
            text = codecs.open(path , "r")
        else:
            path = self.newword
            text = codecs.open(path , "r" , encoding="utf8")
#        path = r"G:\项目1—人工智能客服\lda\data\data.txt"
        line = text.readline()
        textData = []
        while line:
            textData.append(line)
            line = text.readline()
        return textData
                
    def jiebaNWored(self):
        newwords = self.read_text(word_type=2)
        for i in range(0 , len(newwords)):
            newwords[i] = newwords[i].strip("\r\n")
            jieba.suggest_freq((newwords[i]), True)
#        return newwords
    
    def read_stopword(self):
        path = self.stopword
#        path = r"G:\项目1—人工智能客服\lda\data\stop_word.txt"
        stopwords = codecs.open(path,'r').readlines()
        stopwords = [ w.strip() for w in stopwords ]
#        newstopword = ["-" , "[" , "]" , "、" , "@" , "“" , "”" , ")" , "(" , ","]
#        for i in newstopword:
#            stopwords.append(i)
        return stopwords
    
    def pretreatment(self , data_type):
#        self.jiebaNWored()
        data_use = self.read_text(word_type=1)
#        data_use = textData
        stopwords = self.read_stopword()
#        data_use = try_1
        seg_save = []
        for i in data_use:
            i = i.lower()#全部小写
            seg_list = jieba.cut_for_search(i , HMM=True)
            seg = " ".join(seg_list)
            seg = seg.split(" ")
            words = [w for w in seg if w not in stopwords]
            words = " ".join(words)
            seg_save.append(words)#变成分词列表
        seg = "".join(seg_save)
        if data_type == 1:
            seg = seg.replace("\n" , "")
            seg = seg.split(" ")              
#        for i in seg:
#            if i in stopwords:
#                seg.remove(i)
#        words = [ w for w in seg if w not in stopwords ]
        return seg
        
    def testWord(self,sentence):
        stopwords = self.read_stopword()
#        print(sentence)
        sen = sentence.lower()
        sen_seg = jieba.cut_for_search(sen , HMM=False)
        sen_seg = " ".join(sen_seg)
        sen_seg = sen_seg.split(" ")
        words = [w for w in sen_seg if w not in stopwords]

        return words

         
if __name__ == '__main__':     
    getdata = getData()
#    try_1 = getdata.pretreatment(2)  
    data = getdata.read_text(word_type=1)
    getdata.jiebaNWored()
            
    sen = getdata.testWord(sentence = "CRM宽带资源的地址在哪里")
#    sentence = getdata.testWord(sentence=sen)
#    
#    words = getdata.read_text(word_type=2)