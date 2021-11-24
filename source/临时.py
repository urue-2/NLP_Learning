fp = "D:\\resource\\STUDY\\NLP\\2014_corpus_processed.txt"
fo = "D:\\resource\\STUDY\\NLP\\test_set.txt"
import  json
import time

test_num = 5000

def test():
    global test_num
    source_file = open(fp,"r")
    test_file = open(fo,"w")

    for line in source_file:
        if test_num == 0:
            break
        line = line.strip()
        word_records = line.split()
        new_sen = ""
        new_class = []
        new_words = []
        for one_record in word_records:
            one_record = one_record.split("/")
            print(one_record)
            try:
                cur_word = one_record[0].replace("[","").replace("]","")
            except:
                continue

            try:
                cur_class = one_record[1].replace("[","").replace("]","")
            except:
                continue

            new_sen+=cur_word
            new_words.append(cur_word)
            new_class.append(cur_class)

        new_sen+="\n"
        new_class = str(new_class)+"\n"
        new_words = str(new_words)+"\n"

        test_file.write(new_sen)
        test_file.write(new_words)
        test_file.write(new_class)
        test_num -= 1

    print("写完了")






if __name__ == '__main__':


    time1=time.perf_counter()
    time2=time.perf_counter()
    print("taking "+str(time2-time1)+" time")