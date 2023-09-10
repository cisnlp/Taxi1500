# Taxi1500: A Multilingual Dataset for Text Classification in 1500 Languages


## Introduction
This repository contains the publicly available portion of the Taxi1500 dataset, scripts for processing the data, and evaluation code.

Taxi1500 is a dataset for evaluating the cross-lingual generalization ability of multilingual pre-trained language models. It introduces a sentence classification task with 6 topics and covers 1502 typologically diverse languages spanning 112 language families.

For a full description of the dataset, please refer to our [paper](https://arxiv.org/abs/2305.08487).

## Dataset
- Taxi1500 is developed based on the [PBC](https://aclanthology.org/L14-1215/) and [1000Langs](https://github.com/ehsanasgari/1000Langs) corpora.
- An overview of the topics is provided as follows with a description for each topic.

| topic | definition | 
|----------|----------|
| Recommendation  | The verse suggests to act or believe in certain ways.  | 
| Faith   | Display of belief and love toward God, instructions on how to maintain faith, stories of faith and its consequences, etc. |
| Description | Describes a person, relationship, phenomenon, situation, etc.   | 
| Sin | Describes what is considered sin, stories of sinful people and sinful actions. |
| Grace | God’s love, blessing, and kindness towards humans. | 
| Violence | Describes wars, conflict, threats, destruction of people, cities, nations etc. |

## Data access and structure
While Taxi1500 covers 1502 languages in total, we release 1871 editions in 823 languages which are either open access or have a license permitting distribution at the time of publication.
Due to copyright restrictions, these are released as a corpus instead of the actual dataset, and can be converted into the dataset format shown below using the included processing code.

Please refer to [Taxi1500-c_v1.0](Taxi1500-c_v1.0/) and [Taxi1500-c_v2.0](Taxi1500-c_v2.0/) for the corpora.
Please contact Michael Cysouw, Philipps University of Marburg, to request access to the Parallel Bible Corpus (for academic use only).

The table below shows the structure of the dataset for all languages. The examples shown are from the English dataset.

| id | label | verse |
|----------|----------|----------|
| 55002024   | Recommendation | For a slave of the Lord does not need to fight , but needs to be gentle toward all , qualified to teach , showing restraint when wronged ,   |
| 51002005 | Faith  | Though I am absent in body , I am with you in spirit , rejoicing to see your good order and the firmness of your faith in Christ . |
| 60003012 | Sin | For the eyes of Jehovah are on the righteous , and his ears listen to their supplication , but the face of Jehovah is against those doing bad things . |



## Citation

If you use our work, please cite:

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










