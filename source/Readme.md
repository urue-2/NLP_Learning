#Readme
#
### WYD_NLP 1.0  ----  A simple system for NLP ( WS , POS ) 

#### How to use 咋用？

    系统入口：source/main.py


#### To read the code 读源码

    系统结构：

    source:

            corpus_resource : 直接使用必须的数据
    
                    n_gram : 已经训练好的 3-gram
                    POS_source : 词性转移矩阵
    
            POS_tagging : HMM+Viterbi 分词
    
            WS_dict_MM : MM 分词 （ FMM BMM BIMM ）
    
            WS_static_n_gram : n-gram + Viterbi 分词
    
            corpus_preprocess.py : 2014 人民日报预处理
    
            main.py : < 系统入口 >
    
contact me : 1515450482@qq.com 欢迎联系 bug