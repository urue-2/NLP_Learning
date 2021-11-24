import numpy as np

if __name__ == '__main__':


    fonp = "corpus_resource/POS_source/pw_matrix.npy"
    fotxt = "corpus_resource/POS_source/pw_matrix.txt"

    a = np.load(fonp)
    print(a.sum())

