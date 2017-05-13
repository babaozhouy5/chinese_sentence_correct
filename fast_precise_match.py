#!/usr/bin/python
# -*- coding: utf-8 -*-

strStart = 0    # init state
goOn = 1        # go on state
strError = -1   # error state
F = 2           # final state
EPSILLON = ''   # null

'''
A possible dfa/dict format: ()
'''
result = set()

def delta(state, word):
    if state == strStart:
        return goOn
    elif state == goOn:
        return goOn
    elif state == strError:
        return F

def CnPreciseMatch(dfa, state, str, sentence, idx):
    global result
    next_state = delta(state, sentence[idx])
    if idx < len(sentence)-1 and next_state != strError:
        if next_state == F:
            result |= set(str + sentence[idx])
            print result
        CnPreciseMatch(dfa, next_state, str + sentence[idx], sentence, idx + 1)


def CnFussyMatch(dict, state, str, sentence, idx, diff, t_w, cdfa):
    if idx == len(sentence) -1:
        return
    if diff + MetaD(sentence[idx], EPSILLON) <= t_w:
        CnFussyMatch(dict, state, str, sentence, idx+1, diff + MetaD(sentence[idx], epsilon), t_w, cdfa)
    for x in [delta(state, x_) != stError for x_ in xs]:
        if diff + MetaD(x, EPSILLON) <= t_w:
            if state


if __name__ == '__main__':
    sentence = list(u'中国人民站起来了!')
    dfa = (0, 0, 0, 0)
    CnPreciseMatch(dfa, strStart, '', sentence, 0)
    print result
