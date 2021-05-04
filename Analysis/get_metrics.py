#!/usr/bin/python3

from similarity.cosine import Cosine

def get_absolute_matches():
    f, g, ctr = open('model_res').readlines(), open('real_res').readlines(), 0
    for i in range(len(f)):
        if f[i] == g[i]:
            ctr += 1
        else:
            print(f[i]," ", g[i])
    return ctr/len(f)

def get_similarity_score():
    cosine = Cosine(2)
    f, g, ctr = open('model_res').readlines(), open('real_res').readlines(), 0
    for i in range(len(f)):
        f[i], g[i] = f[i].replace("\n", ""), g[i].replace("\n", "")
        ctr += cosine.similarity_profiles(cosine.get_profile(f[i]), cosine.get_profile(g[i]))
    return ctr/len(f)


def get_license_confidence():
    f, ctr = open('avg_conf').readlines(), 0
    for val in f:
        val = val.replace("\n", "")
        ctr += float(val)
    return ctr/len(f)

if __name__ == '__main__':
    print("================================================\n \
          Absolute number of matches: ", get_absolute_matches())
    print("================================================\n \
          Similarity merit of matches: ", get_similarity_score())
    print("================================================\n \
          License Confidence: ", get_license_confidence())
