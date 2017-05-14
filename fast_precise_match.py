#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *

stStart = ''    # init state
stNext  = 1     # next state
stError = -1    # error state
stFinal = 2     # final state
EPSILLON = ''   # null
INFI    = 9999  # present infinity

t_w     = 50    # model hyper-parameter: threshold

def delta(state, word, zh_dict):
    for d in zh_dict:
        if d.endswith(word):
            return stFinal
    return stNext


def MetaD(w1, w2):
    metad = 0
    if w1 == w2:
        metad = 0
    elif w1 == EPSILLON or w2 == EPSILLON:
        metad = 50
    else:
        w1_py = getPinYin(w1)
        w2_py = getPinYin(w2)
        dist = levenshtein(w1_py, w2_py)
        if dist == 0:   # same pronunciation but different shape
            metad = 30
        elif dist == 1:
            metad = 40
        else:
            metad = INFI
    return metad


def cfs(x):
    Meta_Strings = []
    for w in zh_dict:
        if x != w and MetaD(x, w) < INFI:
            Meta_Strings.append(w)
    return Meta_Strings


def CnPreciseMatch(zh_dict, state, str, sentence, idx, result):
    next_state = delta(state, sentence[idx])
    if idx < len(sentence)-1 and next_state != stError:
        if next_state == stFinal:
            result.add(str + sentence[idx])
        CnPreciseMatch(zh_dict, next_state, str + sentence[idx], sentence, idx + 1, result)


def CnFussyMatch(dict, state, str, sentence, idx, diff, t_w, cdfa, result):
    if idx == len(sentence) - 1:
        return
    # try to delte a Chinese character
    if diff + MetaD(sentence[idx], EPSILLON) <= t_w:
        CnFussyMatch(dict, state, str, sentence, idx+1, diff + MetaD(sentence[idx], EPSILLON), t_w, cdfa, result)

    # try to insert a Chinsese character
    for x, next_state in [(x_, delta(state, x_)) for x_ in xs if delta(state, x_) != stError]:
        if diff + MetaD(x, EPSILLON) <= t_w:
            if next_state == stFinal:
                result.add((str + x, idx, diff + MetaD(x, EPSILLON)))
            CnFussyMatch(dict, next_state, str + x, sentence, idx, diff + MetaD(x, EPSILLON), t_w, cdfa, result)

    # get all possible meta-strings into set
    temp_set = set()
    CnPreciseMatch(cdfa, stStart, '', sentence, idx, temp_set)

    # try to replace X with its similar string Y
    for x in temp_set:
        for y in cfs(x):
            next_state = delta(state, y)
            if diff + MetaD(x, EPSILLON) <= t_w and next_state != stError:
                if next_state == stFinal:
                    result.add((str + y, idx+len(x), diff + MetaD(x, y)))
                CnFussyMatch(dict, next_state, str + y, sentence, idx+len(x), diff + MetaD(x, y), t_w, cdfa, result)


if __name__ == '__main__':
    sentence = list(u'中国人民站起来了!')
    # result = set()
    # CnPreciseMatch(zh_dict, stStart, '', sentence, 0, result)
    # for r in list(result):
    #     print r
