# -*- coding:utf-8 -*-
fp = "D:\\resource\\STUDY\\NLP\\2014_corpus.txt"
fpp = "D:\\resource\\STUDY\\NLP\\2014_corpus_processed.txt"

fi = open(fp,"r",encoding="utf-8")
#fi=fi.readlines(5)
fo = open(fpp,"w")
for line in fi:
    line = line.strip()
    words = line.split()
    for (i,word) in enumerate(words):

        pw = word.split("/")
        tword = pw[0]
        if "e" in tword or "E" in tword or "a" in tword or "A" in tword or "i" in tword or "I" in tword:
            print(word,tword)
            pw[0]="EEE"
            new_word = "/".join(pw)
            words[i] = new_word

    line = " ".join(words)
    line+="\n"


    fo.write(line)

fi.close()
fo.close()

str = "澳大利亚/nsf 悉尼/ns 市/n [新/a 南/b 威尔士/ns 大学/nis]/ntu 大气/n 科学家/nnt StevenSherwood/x 表示/v ，/w 目前/t 的/ude1 模型/n 和/cc 各种/rz 观测/v 资料/n 表明/v ，/w 一旦/d 二氧化碳/n 的/ude1 含量/n 是/vshi 工业化/vn 前/f 含量/n [280/m ppm/x]/mq （/w 百万分之一/m ）/w 的/ude1 两倍/mq ，/w 地球/ns 将/d 变暖/nz [1/m ./w 5/m 摄氏度/q]/mq 到/v [4/m ./w 5/m 摄氏度/q]/mq ，/w 并且/c 气候/n 系统/n 也/d 将/d 作出/v 调整/vn 。/w Sherwood/x 强调/v ，/w 这/rzv 一/m 研究/vn 是/vshi 很/d 宽泛/a 的/ude1 ，/w 自从/p [第一/m 台/q]/mq 计算机/n 于/p 上世纪/nz 70年代/t 开始/v 模拟/vn 气候/n 以来/f ，/w 这种/r 情况/n 就/d 从未/d 改变/v 过/uguo 。/w 他/rr 指出/v ，/w 广泛/a 的/ude1 分析/vn 表明/v ，/w 一个/mq 模型/n 的/ude1 [气候/n 敏感性/gi]/nz 在/p 很大/d 程度/n 上/f 取决于/v 该/rz 模型/n 如果/c 评估/vn 低空/s 云层/n 的/ude1 形成/vn 。/w 如果/c 一个/mq 模拟/vn 生成/v 了/ule 大量/m 的/ude1 低端/nz 云层/n ，/w 则/d 有/vyou 更多/ad 的/ude1 阳光/n 被/pbei 反射/v 回/v 太空/s ，/w 大体上/d 看/v ，/w 地球/ns 会/v 比/p 没有/v 云层/n 时/ng 更/d 冷/a 。/w \n"

print(str.isalpha())