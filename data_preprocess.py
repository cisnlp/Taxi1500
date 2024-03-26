import os
from collections import Counter
from collections import defaultdict
import pandas as pd
import collections
import numpy as np
import random
import csv

path=''
labeled_data=''

#transfer english labeled data to other languages
eng_dict = {}
with open(labeled_data, 'r') as file:
    lines = file.readlines()
    for line in lines:
        l =line.split('\t')
        eng_dict[l[0]] = l[1]

def lrs_lan_dict(file):
    lrs_dict = {}
    with open(file, 'r') as myfile:
        lines = myfile.readlines()
        for line in lines[11:]:
            l = line.split('\t')
            try:
                lrs_dict[l[0]] = l[1]
            except IndexError:
                pass
    return lrs_dict

lan_file = {}
with open('lan_file_size.tsv', 'r') as file:
    lines = file.readlines()
    for line in lines:
        l=line.strip().split('\t')     
        if l[0] != 'pre':  
            lan_file[l[0]] = l[1]

for files in os.listdir("./"):
    if os.path.exists("./transfered"):
        os.system("rm -rf "+"./transfered")
os.mkdir('./transfered')
for lan in lan_file.keys():
    lrs_file_path = './transfered/'+lan+'.tsv' 
    lrs_dict = lrs_lan_dict(lan_file[lan])
    print(lan)
    with open(lrs_file_path, 'w') as file:
        for k in eng_dict.keys():
            try:
                line = ('\t').join([str(k), eng_dict[k], lrs_dict[k]])
                file.write(line)
            except KeyError:
                pass

lan_files = os.listdir('./transfered/')
print(lan_files)

#filter out languages that under 900 lines
len_list=[]
for file in lan_files:
    lan=file[:3]
    with open('./transfered/'+file, 'r') as myfile, open('./lan_line.tsv', 'a') as file1:
        lines = myfile.readlines()
        if len(lines)> 900:
            line = (',').join([lan, str(len(lines))])
            len_list.append(len(lines))
            file1.write(line+'\n')


#transfer train, dev and test file for other languages from english

def train_dev_test(eng_file, file_path):
    labeled_eng_dict = dict() #{id, label) english
    with open(eng_file) as file:
        lines = file.readlines()
        for line in lines:
            id, label, verse = line.split('\t')
            labeled_eng_dict[id] = label

    lan_files = os.listdir("./transfered/")

    test_lan=[]
    with open('lan_line.tsv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.split(',')
            test_lan.append(l[0])

    for file in lan_files:
        lan=file[:3]
        if lan in test_lan:
            with open('./transfered/'+file, 'r') as myfile, open(file_path+'/'+lan+'.tsv', 'w') as file1:
                lrs_dict = dict() #{id: verse) low resource language
                lines = myfile.readlines()
                for line in lines:
                    print(line)
                    l = line.split('\t')
                    if l[0] in labeled_eng_dict.keys():
                        file1.write(line)

    print('success')

eng_train_file='../eng_data/eng_train.tsv'
eng_dev_file='../eng_data/eng_dev.tsv'
eng_test_file='../eng_data/eng_test.tsv'


os.mkdir('./train_dev_test')
os.mkdir('./train_dev_test/train')
os.mkdir('./train_dev_test/dev')
os.mkdir('./train_dev_test/test')
train_dev_test(eng_train_file, './train_dev_test/train')
train_dev_test(eng_dev_file, './train_dev_test/dev')
train_dev_test(eng_test_file, './train_dev_test/test')