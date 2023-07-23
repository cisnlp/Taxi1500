# Taxi1500: A Multilingual Dataset for Text Classification in 1500 Languages


## Introduction
This repository contains information about Taxi1500 dataset and code for evaluation and processing.

Taxi500 is a dataset for evaluating the cross-lingual generalization ability of multilingual pre-trained language models. It contains a sentence classification task with 6 topics and covers 1502 typologically diverse languages spanning 112 language families.

For a full description of the dataset, please refer to our [paper](https://arxiv.org/abs/2305.08487).

## Dataset
- Taxi500 is developed based on the [PBC](https://aclanthology.org/L14-1215/) and [1000Langs](https://github.com/ehsanasgari/1000Langs) corpora.
- Taxi1500 proposes a sentence classification task with 6 topics in 1502 languages. The 6 topics are: 

| topic | definition | 
|----------|----------|
| Recommendation  | An imperative statement which suggests to act or believe in certain ways.  | 
| Faith   | Display of belief and love toward God, instructions on how to maintain faith, stories of faith and its consequences, etc. |
| Description | Describes a person, relationship, phenomenon, situation, etc.   | 
| Sin | Describes what is considered sin, stories of sinful people and sinful actions. |
| Grace | God’s love, blessing, and kindness towards humans. | 
| Violence | Describes wars, conflict, threats, and torture; but also destructions of people, cities, and nations. |

## Access to the data
Taxi1500 covers 1502 languages, we release 1430 editions in 670 languages at the time of publishing, the data can be accessed through the [link](). For the rest copyrighted 832 languages the users can contact thomas.mayer@uni-marburg.de and use the code we provide to obtain the evaluation data.


## Data structure

The table below shows the structure of the dataset in each language. We present examples from the English dataset.

| id | label | verse |
|----------|----------|----------|
| 55002024   | Recommendation | For a slave of the Lord does not need to fight , but needs to be gentle toward all , qualified to teach , showing restraint when wronged ,   |
| 51002005 | Faith  | Though I am absent in body , I am with you in spirit , rejoicing to see your good order and the firmness of your faith in Christ . |
| 60003012 | Sin | For the eyes of Jehovah are on the righteous , and his ears listen to their supplication , but the face of Jehovah is against those doing bad things . ”|



## Citation

If you find our model, data or the overview of data useful for your research, please cite:

```
@misc{ma2023taxi1500,
      title={Taxi1500: A Multilingual Dataset for Text Classification in 1500 Languages}, 
      author={Chunlan Ma and Ayyoob ImaniGooghari and Haotian Ye and Ehsaneddin Asgari and Hinrich Schütze},
      year={2023},
      eprint={2305.08487},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```










