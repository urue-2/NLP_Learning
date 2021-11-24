import numpy as np
import json
import time

fp = "D:\\resource\\STUDY\\NLP\\2014_corpus_processed.txt"

def gram_1():


    fdic = "D:\\resource\\STUDY\\NLP\\2014_corpus_1gram.txt"
    #286268
    # 《》   []

    mydic = {}
    mydic["BOS"]={"start":0}
    mydic["EOS"] = {"end": 0}
    f = open(fp,"r")
    fd = open(fdic,"w")
    #f = f.readlines(4)
    for line in f:
        line = line.strip().split()
        mydic["BOS"]["start"] += 1
        mydic["EOS"]["end"] += 1
        secondary_words = []
        single_book = []
        for (index, word) in enumerate(line):
            if ("[" in word):
                secondary_words.append([0, index])
                word = word[1:]
                if "《" in line[index - 1]:
                    secondary_words[-1][0] = 1
            if ("]" in word):
                if (secondary_words != []) and len(secondary_words[-1]) == 2:
                    secondary_words[-1].append(index)
                word = word.split("]")[0]



            word, word_class = word.split("/")[0], word.split("/")[-1]
            if word not in mydic.keys():
                mydic[word] = {}
            mydic[word][word_class] = mydic.get(word, {}).get(word_class, 0) + 1


        if secondary_words != []:
            for index in secondary_words:
                if len(index) == 3:
                    if index[0] == 1:
                        new_word = "《"
                    else:
                        new_word = ""
                    start = index[1]
                    end = index[2]
                    for i in range(start, end):
                        new_word += str(line[i].split("[")[-1]).split("/")[0]
                    last_part = line[end].split("]")
                    new_word += last_part[0].split("/")[0]
                    if new_word[0] == "[":
                        new_word = new_word[1:]
                    new_class = last_part[1][1:]
                    if new_word[0] == "《":
                        new_word += "》"
                    if new_word not in mydic.keys():
                        mydic[new_word] = {}
                    mydic[new_word][new_class] = mydic.get(new_word, {}).get(new_class, 0) + 1

    print(len(mydic))
    fd.write(json.dumps(mydic, ensure_ascii=False, indent=2))


def gram_2():
    fdic = "D:\\resource\\STUDY\\NLP\\2014_corpus_2gram.txt"

    mydic = {}
    f = open(fp, "r")
    fd = open(fdic, "w")
    for line in f:
        line = line.strip()
        words = line.split()
        for (index, word) in enumerate(words):
            word = word.split("/")[0]
            if ("[" in word) or ("]" in word):
                word = word.replace("]","")
                word = word.replace("[", "")
            words[index] = word

        words.insert(0,"BOS")
        words.append("EOS")

        for i in range(len(words)-1):
            t2gram = words[i]+"@"+words[i+1]
            mydic[t2gram] = mydic.get(t2gram,0)+1

    print(len(mydic))
    fd.write(json.dumps(mydic, ensure_ascii=False, indent=2))

def gram_3():
    fdic = "D:\\resource\\STUDY\\NLP\\2014_corpus_3gram.txt"

    mydic = {}
    f = open(fp, "r")
    fd = open(fdic, "w")
    for line in f:
        line = line.strip()
        words = line.split()
        for (index, word) in enumerate(words):
            word = word.split("/")[0]
            if ("[" in word) or ("]" in word):
                word = word.replace("]","")
                word = word.replace("[", "")
            words[index] = word

        words.insert(0,"BOS")
        words.append("EOS")

        for i in range(len(words)-2):
            t3gram = words[i]+"@"+words[i+1]+"@"+words[i+2]
            mydic[t3gram] = mydic.get(t3gram,0)+1

    print(len(mydic))
    fd.write(json.dumps(mydic, ensure_ascii=False, indent=2))


if __name__ == '__main__':


    time1=time.perf_counter()
    time2=time.perf_counter()
    print("taking "+str(time2-time1)+" time")


