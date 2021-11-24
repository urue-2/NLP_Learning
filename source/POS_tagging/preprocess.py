import numpy
import json



fp = "D:\\resource\\STUDY\\NLP\\2014_corpus_1gram.txt"
fpp = "D:\\resource\\STUDY\\NLP\\word_class_static.txt"

if __name__ == '__main__':
    with open(fp, 'r')as f:
        gram1 = json.load(f)

    fo = open(fpp,"w")

    wp = {}
    for (word,word_dict) in gram1.items():
        if word.isalpha():
            for (twp,twp_num) in word_dict.items():
                wp[twp] = wp.get(twp,0)+twp_num

    fo.write(json.dumps(wp, ensure_ascii=False, indent=2))
    print(len(wp))
    print(wp)





    f.close()
    fo.close()