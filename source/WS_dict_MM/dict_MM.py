# 基于词典分词

import  math
import  time
import json

big_dict={}
upper_dict={}
dict_maxlen = 0

def loaddict():
    global  upper_dict
    dictpath = "D:\\resource\\STUDY\\NLP\\2014_corpus_1gram.txt"
    with open(dictpath, 'r') as f:
        upper_dict = json.load(f)


def build_dict():
    ss = time.perf_counter()
    global dict_maxlen
    dict_source_path = "D:\\下载\\人民日报语料.txt"
    dict_file = open(dict_source_path,'r')
    for line in dict_file:
        words = line[:-1].split(" ")
        for word in words:
            big_dict[word] = big_dict.get(word,0) + 1
    for word in big_dict.keys():
        if len(word) > dict_maxlen:
            dict_maxlen = len(word)
            print(word)

    ee = time.perf_counter()
    print("build dict take ",str(ee-ss))

def FMM(sentence):
    sentence_len = len(sentence)
    start_index = 0
    end_index = min(dict_maxlen-1,sentence_len-1)
    re = []
    while not (start_index > sentence_len-1) :
        cur_word = sentence[start_index:end_index+1]
        while (cur_word not in upper_dict.keys())  :
            if start_index == end_index:
                break
            else:
                end_index -= 1
                cur_word = sentence[start_index:end_index + 1]

        cur_word = sentence[start_index:end_index+1]
        re.append(cur_word)
        #print(re)
        start_index = end_index+1
        end_index = min( start_index +dict_maxlen -1 , sentence_len-1)
    return re


def BMM(sentence):
    sentence_len = len(sentence)
    end_index = sentence_len-1
    start_index =max( end_index - dict_maxlen + 1, 0)
    re = []
    while not (end_index < 0):
        cur_word = sentence[start_index:end_index + 1]
        while not (cur_word  in big_dict.keys()):
            if start_index == end_index:
                break
            else:
                start_index += 1
                cur_word = sentence[start_index:end_index + 1]

        re.append(cur_word)
        end_index = start_index - 1
        start_index = max (end_index - dict_maxlen +1 , 0)

    re.reverse()
    return re


def BI_MM(sentence):
    fm = FMM(sentence)
    bm = BMM(sentence)
    # 两者相同，优先返回BMM
    if len(fm) < len(bm):
        return fm
    else:
        return bm











#------------------------------
#API part





# 0FMM 1BMM 2BI_MM
def MM(sentence,method="BI_MM"):
    """

    :param sentence:
    :param method:
    :return: WS result using MM , default : BIMM
    """
    s_time = time.perf_counter()
    build_dict()
    if method == "FMM":
        re = FMM(sentence)
    elif method=="BMM":
        re = BMM(sentence)
    else :
        re = BI_MM(sentence)
    e_time = time.perf_counter()

    print("MM WP result", re)
    print("time",e_time-s_time)
    print("\n")
    return re




if __name__ == '__main__':
    loaddict()
    print(len(upper_dict))

    #re = MM(sentence="")
    sen = "人民网1月1日讯据《纽约时报》报道，美国华尔街股市在2013年的最后一天继续上涨，和全球股市一样，都以最高纪录或接近最高纪录结束本年的交易。"
    s = time.perf_counter()
    print("FMM",FMM(sen))
    e = time.perf_counter()
    print("FMM take ",str(e-s))