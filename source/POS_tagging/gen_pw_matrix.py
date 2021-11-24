import numpy

import numpy as np
import json
import corpus_resource
fp = "corpus_resource/n_gram/2014_corpus_1gram.txt"
fpp = "corpus_resource/POS_source/word_class_static.txt"
fonp = "corpus_resource/POS_source/pw_matrix"
fotxt = "corpus_resource/POS_source/pw_matrix.txt"

fc = "D:\\resource\\STUDY\\NLP\\2014_corpus_processed.txt"


if __name__ == '__main__':
    with open(fp, 'r')as f:
        gram1 = json.load(f)
    with open(fpp, 'r')as ff:
        word_class = json.load(ff)

    corpus = open(fc,"r")

    print(len(word_class))

    word_class_list = list(word_class.keys())


    num_word_class = len(word_class)

    wp_matrix = np.zeros([num_word_class,num_word_class])

    for line in corpus:
        line = line.strip()
        words = line.split()
        #print(line)
        #print(words)
        for (word_index,word) in enumerate(words):
            #print(word)
            if word_index == 0:
                cur_word_class = "start"
            else:
                cur_word_record = words[word_index].split("/")
                #cur_word = cur_word_record[0].replace("[","").replace("]","")
                cur_word_class = cur_word_record[-1].replace("[","").replace("]","")
            #print(cur_word_class)
            try:
                from_class_matrix_index = word_class_list.index(cur_word_class)
            except:
                continue

            if word_index == len(words)-1:
                next_word_class = "end"

            else:

                next_word_record = words[word_index+1].split("/")
                #next_word = next_word_record[0].replace("[","").replace("]","")
                next_word_class = next_word_record[-1].replace("[","").replace("]","")

            print(cur_word_class,next_word_class)
            try:
                to_class_matrix_index = word_class_list.index(next_word_class)
            except:
                continue

            wp_matrix[from_class_matrix_index][to_class_matrix_index]+=1

    print(wp_matrix)
    np.save(fonp, wp_matrix)
    np.savetxt(fotxt, wp_matrix, fmt=numpy.float, delimiter=',')





