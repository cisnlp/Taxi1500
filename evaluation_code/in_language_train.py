import torch
import pandas as pd
import transformers
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification, AdamW, XLMRobertaConfig, DistilBertModel, BertForSequenceClassification, BertTokenizer, BertModel, AutoTokenizer, AutoModelForMaskedLM
from torch.utils.data import TensorDataset, random_split
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import get_linear_schedule_with_warmup
import numpy as np
import random
from sklearn.metrics import f1_score
from collections import Counter
import time
import datetime
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.utils.multiclass import unique_labels
from collections import defaultdict
import os

seed_val = 42

random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)
torch.cuda.manual_seed_all(seed_val)

epochs = 15
batch_size = 32
accum_iter = 4
learn_rate=2e-5
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


best_model=best_model


def read_data(file):
    print('Preparing dataset...')
    df = pd.read_csv(file, delimiter='\t', header=None,on_bad_lines='skip', engine='python')
    df.columns = ['id', 'label', 'verse']
    print('Number of sentences: {:,}\n'.format(df.shape[0]))
    #print(Counter(list(df['label'])))
   # print(len(Counter(list(df['label']))))
    df['label'].replace({'Recommendation': int(0), 'Faith': int(1), 'Violence': int(2), 'Grace': int(3), 'Sin': int(4), 'Description': int(5)},inplace=True)

    sentences = df.verse.values
    labels = df.label.values
    #print(list(df['label']))
    #print(len(sentences), len(labels))
    return sentences, labels

def encode(sentences, labels):
    print('Loading model tokenizer...')
    input_ids = []
    attention_masks = []
    tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-large')
    for sent in sentences:
        sent = str(sent)
        encoded_dict = tokenizer.encode_plus(
            sent,  # Sentence to encode.
            add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
            truncation=True,
            max_length=100,  # Pad & truncate all sentences.
            pad_to_max_length=True,
            return_attention_mask=True,  # Construct attn. masks.
            return_tensors='pt',  # Return pytorch tensors.
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])
    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)

    labels = torch.tensor(labels)

        #print('Original: ', sentences[0])
        #print('Token IDs:', input_ids[0])

    return input_ids, attention_masks, labels

def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

def F1_score(preds, labels):
    pre = np.argmax(preds, axis=1)
    f1 = f1_score(labels, pre, average='macro')
    return f1

def train(train_dataloader, validation_dataloader):
    global best_loss
    training_stats = []
    #best_loss = float('inf')
    best_acc = 0
    nb_eval_steps = 0

    for epoch_i in range(0, epochs):
        print("")
        print('======== Epoch {:} / {:} ========'.format(epoch_i + 1, epochs))
        print('Training...')

        total_train_loss = 0
        total_train_f1 = 0

        model.cuda()
        model.train()
        for step, batch in enumerate(train_dataloader):
            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            b_labels = batch[2].to(device)
            
            
            (loss, logits) = model(b_input_ids,
                                   attention_mask=b_input_mask,
                                   labels=b_labels,
                                   return_dict=False)
            loss = loss / accum_iter
            logits = logits.detach().cpu().numpy()
            b_label_ids = b_labels.to('cpu').numpy()
            
            total_train_loss += loss.item()
            total_train_f1 += F1_score(logits, b_label_ids)
            prediction = np.argmax(logits, axis=1)
            #print('train predict:', prediction)
            #print('true_label', b_label_ids)
            
            loss.backward()
            if ((step + 1) % accum_iter == 0) or (step + 1 == len(train_dataloader)):
                optimizer.step()
                scheduler.step()
                model.zero_grad()

        avg_train_loss = total_train_loss / len(train_dataloader)
        avg_train_f1 = total_train_f1 / len(train_dataloader)
        print('train_f1: ', avg_train_f1)

        # print("")
        # print("  Average training loss: {0:.2f}".format(avg_train_loss))
        # print("  Average training F1: {0:.2f}".format(avg_train_f1))
        # #print("  Training epcoh took: {:}".format(training_time))
        #
        # print("")
        # print("Running Validation...")

        model.eval()

        total_eval_accuracy = 0
        total_eval_f1_score = 0
        total_eval_loss = 0
        for batch in validation_dataloader:
            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            b_labels = batch[2].to(device)
            with torch.no_grad():
                (loss, logits) = model(b_input_ids,
                                       attention_mask=b_input_mask,
                                       labels=b_labels,
                                       return_dict=False)
            total_eval_loss += loss.item()
            logits = logits.detach().cpu().numpy()
            label_ids = b_labels.to('cpu').numpy()

            total_eval_f1_score += F1_score(logits, label_ids)
            total_eval_accuracy += flat_accuracy(logits, label_ids)

            #print('val pre:', np.argmax(logits, axis=1))
            #print('val true:',label_ids)
        avg_val_accuracy = total_eval_accuracy / len(validation_dataloader)
        avg_val_f1 = total_eval_f1_score / len(validation_dataloader)
        avg_val_loss = total_eval_loss / len(validation_dataloader)
        print('avg_val_accuracy:', avg_val_accuracy, 'avg_val_f1: ', avg_val_f1, 'avg_val_loss', avg_val_loss)
        if avg_val_loss < best_loss:
            # print('avg_val_loss:', avg_val_loss)
            # print('best_loss:', best_loss)
            best_loss = avg_val_loss
            # print('validation loss improved, saving model to best_model.pt')
            torch.save(model, best_model)
            print('loss descreased:', epoch_i)
        else:
            pass
        print('val_f1: ', avg_val_f1)
        # print("  Accuracy: {0:.2f}".format(avg_val_accuracy))
        # print("  F1: {0:.2f}".format(avg_val_f1))


        #validation_time = format_time(time.time() - t0)

        # print("  Validation Loss: {0:.2f}".format(avg_val_loss))
       # print("  Validation took: {:}".format(validation_time))
        training_stats.append(
            {
                'epoch': epoch_i + 1,
                'Train Loss': avg_train_loss,
                'Val Loss': avg_val_loss,
                'Val Accu.': avg_val_accuracy,
                'val F1 ': avg_val_f1,
            }
        )

        print("")
        print("Training complete!")
    pd.set_option('display.precision', 2)
    df_stats = pd.DataFrame(data=training_stats)
    df_stats = df_stats.set_index('epoch')
    print(df_stats)


def test(test_dataloader):
    print('Start Test...')
    model = torch.load(best_model)
    model.cuda()
    model.eval()
    predictions, true_labels = [], []
    #prediction_list, actual_label=np.array(), np.array()

    total_test_accuracy = 0
    total_test_f1_score = 0
    #total_test_loss = 0
    nb_eval_steps = 0
    # Predict
    for batch in test_dataloader:
        # Add batch to GPU
        batch = tuple(t.to(device) for t in batch)

        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch

        # Telling the model not to compute or store gradients, saving memory and
        # speeding up prediction
        with torch.no_grad():
            # Forward pass, calculate logit predictions
            outputs = model(b_input_ids,
                            attention_mask=b_input_mask)

        logits = outputs[0]

        # Move logits and labels to CPU
        # Move logits and labels to CPU
        logits = logits.detach().cpu().numpy()
        label_ids = b_labels.to('cpu').numpy()

        total_test_f1_score += F1_score(logits, label_ids)
        total_test_accuracy += flat_accuracy(logits, label_ids)
        # Store predictions and true labels

        predictions.append(np.argmax(logits, axis=1).flatten())

        true_labels.append(label_ids)
        # actual_label.concate(label_ids)
        # prediction_list.concate(logits)
        #print(predictions)
        #print('predict: ', np.argmax(predictions, axis=0))
        #print('true label:', true_labels)
    avg_test_accuracy = total_test_accuracy / len(true_labels)
    avg_test_f1 = total_test_f1_score / len(true_labels)
    pre = np.array(predictions)

    #print(true_labels)
    #print(pre)
    print("  Accuracy: {0:.2f}".format(avg_test_accuracy))
    print("  F1: {0:.2f}".format(avg_test_f1))
    print('    DONE.')
    return avg_test_f1


lan_files = os.listdir("/mounts/data/proj/ayyoob/Chunlan/lrs_train_dev_test2")


languages=[]
with open('../data_collect/lan_line.tsv', 'r') as myfile:
    lines=myfile.readlines()
    for line in lines:
        l = line.split(',')
        languages.append(l[0])

df10=pd.DataFrame(columns=['lan', 'f1', 'batch_size', 'learn_rate'])

lan_param_dic=defaultdict(tuple)
with open('xlmr_l_32results.csv', 'w') as f:
    for lan in languages:
        print(lan)
        best_loss = float('inf')
        best_vali_f1=float('-inf')
        best_learn_rate=float()
        recored_batch_size=int()
        train_file='/mounts/data/proj/ayyoob/Chunlan/lrs_train_dev_test2/860_'+lan+'_train.tsv'
        dev_file='/mounts/data/proj/ayyoob/Chunlan/lrs_train_dev_test2/'+lan+'_dev.tsv'
        test_file = '/mounts/data/proj/ayyoob/Chunlan/lrs_train_dev_test2/'+lan+'_test.tsv'
        # try:
        model = XLMRobertaForSequenceClassification.from_pretrained(
            "xlm-roberta-large", # Use the 12-layer BERT model, with an uncased vocab.
        num_labels = 6, 
        output_attentions = False, # Whether the model returns attentions weights.
        output_hidden_states = False, # Whether the model returns all hidden-states.
        )
        model.cuda()
        optimizer = AdamW(model.parameters(),
        lr = learn_rate, # args.learning_rate - default is 5e-5, our notebook had 2e-5
        eps = 1e-8 # args.adam_epsilon  - default is 1e-8.
        )
        train_verse, train_label = read_data(train_file)
        train_input_ids, train_attention_masks, train_labels = encode(train_verse, train_label)
        train_dataset = TensorDataset(train_input_ids, train_attention_masks, train_labels)

        dev_verse, dev_label = read_data(dev_file)
        dev_input_ids, dev_attention_masks, dev_labels = encode(dev_verse, dev_label)
        val_dataset = TensorDataset(dev_input_ids, dev_attention_masks, dev_labels)


        train_dataloader = DataLoader(
                    train_dataset,  # The training samples.
                    sampler = RandomSampler(train_dataset), # Select batches randomly
                    batch_size = batch_size,# Trains with this batch size.
            )

        validation_dataloader = DataLoader(
                    val_dataset, # The validation samples.
                    sampler = SequentialSampler(val_dataset), # Pull out batches sequentially.
                    batch_size = batch_size # Evaluate with this batch size.
                )

        total_steps = len(train_dataloader) * epochs
        scheduler = get_linear_schedule_with_warmup(optimizer,
                                            num_warmup_steps = 0, # Default value in run_glue.py
                                            num_training_steps = total_steps) 
        
        train_dataloader, validation_dataloader, model, optimizer, scheduler = accelerator.prepare(
                        train_dataloader, validation_dataloader, model, optimizer, scheduler)
        vali_loss, recored_batch_size, recored_learn_rate = train(train_dataloader, validation_dataloader)

        test_verse, test_label = read_data(test_file)
        test_input_ids, test_attention_masks, test_labels = encode(test_verse, test_label)
        test_dataset = TensorDataset(test_input_ids, test_attention_masks, test_labels)

        test_verse, test_label = read_data(test_file)
        test_input_ids, test_attention_masks, test_labels = encode(test_verse, test_label)
        test_dataset = TensorDataset(test_input_ids, test_attention_masks, test_labels)
        
        test_dataloader=DataLoader(
            test_dataset,
            sampler = SequentialSampler(test_dataset),
            batch_size = batch_size,
        )
        test_f1 = test(test_dataloader)

        lan_param_dic[lan]=(test_f1, recored_batch_size, str(recored_learn_rate))
        print(lan_param_dic)
        print(lan, test_f1)
        df10 = df10.append({'lan': lan, 'f1': lan_param_dic[lan][0], 'batch_size': lan_param_dic[lan][1], 'learn_rate': lan_param_dic[lan][2]}, ignore_index=True)
        print(df10)
        line=(',').join([lan, str(test_f1), str(recored_batch_size), str(recored_learn_rate)])
        f.write(line+'\n')
        df10.to_csv('./no_para32_xlmr_large_in_language_860_f1.csv', index=False)
    # except:
    #     pass

    




















