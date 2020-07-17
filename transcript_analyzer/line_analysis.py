#!/usr/bin/env python3

def runit():
    import sys

    with open('phage.txt') as file:
        lines = file.readlines()
    people = []
    line_counts = []
    word_count = []
    for i in lines:
        i = i.replace(' [OC]','')
        if ':' in i and i[1].isupper():
            if i[:i.index(':')] not in people:
                people.append(i[:i.index(':')])
                line_counts.append(1)
                words = i[i.index(':')+1:].split()
                word_count.append(len(words))
            else:
                line_counts[people.index(i[:i.index(':')])] += 1
                words = i[i.index(':')+1:].split()
                word_count[people.index(i[:i.index(':')])] += len(words)
    for i in people:
        print(i +' '* (20 - len(i))+str(line_counts[people.index(i)])+' '*(20 - len(str(line_counts[people.index(i)])))+str(word_count[people.index(i)]))
    return people
