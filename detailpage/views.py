from django.shortcuts import render
from homepage.models import YoutubeReal, Youtube
from sources.npc_loader import *
import numpy as np
BERT_NAME = "bert-base-multilingual-cased"
BERT_PATH = "bert_ckpt"


def detail(request, channel, url):   
    label = []
    if channel == 'MBC':
        datas = YoutubeReal.objects.filter(url=url)
    elif channel == 'KBS' or channel =='SBS':
        datas = Youtube.objects.filter(url=url)

    data_inputs = datas[0].sub_text.replace("(기자)","").replace("(앵커)","").replace("(기상캐스터)","").split('\n')
    address = url

    texts = ' '.join(data_inputs)
    text_list = datas[0].sub_text.replace("(기자)","").replace("(앵커)","").replace("(기상캐스터)","")
    text_lst  = text_list.split('\n')

    start_lst = datas[0].start.split('\n')
    duration_lst = datas[0].duration.split('\n')
    start = []
    end = []
    index_list=[]
    find_list = []
 
    inputs = make_train_inputs(data_inputs)
    predicts = npc_model.predict(inputs)
    
    for i in range(len(predicts)) :
        label.append(np.argmax(predicts[i]))

    for i in range(len(label)-1):
        if label[i] == 0 and label[i+1] == 1:
            st = float(start_lst[i+1])
            start_index = i + 1 # 시작 인덱스 
            
        elif label[i] == 1 and label[i+1] == 0:
            en = float(start_lst[i]) + float(duration_lst[i])
            end_index = i
            start.append(st)
            end.append(en)
            index_list.append([i for i in range(start_index,end_index+1)])
            
        elif label[i] == 1 and label[i+1] == 1: 
            if (i+1) == len(label)-1: # 제일 마지막 요약문으로 끝날 때 
                en = float(start_lst[i+1]) + float(duration_lst[i+1])
                end_index = i +1 
                start.append(st)
                end.append(en)
                index_list.append([i for i in range(start_index,end_index+1)])
            elif i == 0: # 가장 처음이 요약문 일때 
                st = float(start_lst[i]) 
                start_index = i 
            else:
                pass
    

    if (len(start) == 3):
        index0 = index_list[0]
        find0 = ' '.join([text_lst[i] for i in index0])
        index1 = index_list[1]
        find1 = ' '.join([text_lst[i] for i in index1])
        index2 = index_list[2]
        find2 = ' '.join([text_lst[i] for i in index2])
        find_list  = [find0, find1,find2]

      
    elif (len(start) == 2):
        start.append(0)
        end.append(0)
        index0 = index_list[0]
        find0 = ' '.join([text_lst[i] for i in index0])
        index1 = index_list[1]
        find1 = ' '.join([text_lst[i] for i in index1])
        find2 = ''  
        find_list  = [find0,find1,find2] 
            
    elif (len(start) == 1):
        start.append(0)
        end.append(0)
        start.append(0)
        end.append(0)
        index0 = index_list[0]
        find0 = ' '.join([text_lst[i] for i in index0])
        find1 = ''
        find2 = ''
        find_list  = [find0,find1,find2]
    

    return render(request, 'detailpage/detailpage.html', {'address':address,'start':start,'end':end,'text':texts,'index':index_list,'find':find_list})


def make_train_inputs(data_inputs, max_token_len=194) :
    input_ids_list = []
    attention_mask_list = []
    token_type_ids_list = []

    for data_input in data_inputs :
        input_ids, attention_mask, token_type_ids = npc_tokenizer.encode(data_input, max_token_len)

        input_ids_list.append(input_ids)
        attention_mask_list.append(attention_mask)
        token_type_ids_list.append(token_type_ids)
    
    input_ids_list = np.array(input_ids_list, dtype=int)
    attention_mask_list = np.array(attention_mask_list, dtype=int)
    token_type_ids_list = np.array(token_type_ids_list, dtype=int)

    train_inputs = (input_ids_list, attention_mask_list, token_type_ids_list)
    return train_inputs