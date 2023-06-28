# Taxi1500: Taxi1500: A Multilingual Dataset for Text Classification in 1500 Languages


## Introduction
This repository contains information about Taxi1500, data and code.

The Taxi500 is a dataset for the evaluation of the cross-lingual generalization ability of pre-trained multilingual models. It covers 1502 typologically diverse languages (spanning 112 language families) and includes one sentence classification task with 6 topics.

For a full description of the dataset, see the [paper](https://arxiv.org/abs/2305.08487).

## Task and languages.
- Taxi500 is developed based on the [PBC](https://aclanthology.org/L14-1215/) and [1000Langs](https://github.com/ehsanasgari/1000Langs).
- Taxi1500 is a multilingual evaluation dataset contains one classification task with 6 topics in 1502 languages. The 6 topics are: 

| topic | definition | 
|----------|----------|
| Recommendation  | An imperative statement which suggests to act or believe in certain ways.  | 
| Faith   | Display of belief and love toward God, instructions on how to maintain faith, stories of faith and its consequences, etc. |
| Description | Describes a person, relationship, phenomenon, situation, etc.   | 
| Sin | Describes what is considered sin, stories of sinful people and sinful actions. |
| Grace | God’s love, blessing, and kindness towards humans. | 
| Violence | Describes wars, conflict, threats, and torture; but also destructions of people, cities, and nations. |

## Access to the data
Taxi1500 covers 1502 languages, we release 670 languages in 1430 editions at the time of publishing, the data can be accessed through the [form](https://docs.google.com/forms/d/1lXrUQl_acQRE4VnZ7uEUpgNHnpG50wSXzQnCO_SM02A/edit?pli=1). For the rest copyrighted 832 languages the users can contact thomas.mayer@uni-marburg.de and use codes we provide to obtain the evaluation data.


## Data structure

Below shows the structure of data in each languages, we present the English data as example.

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










