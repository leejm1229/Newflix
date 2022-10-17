from sources.commons import *

import tensorflow as tf
#from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from sources.data_refiner import DataRefiner
from sources.npc_tokenizer import NPCTokenizer
from sources.npc_model import NPCModel

##############################################################################

DEBUG = True
TESTING = True

BERT_NAME = "bert-base-multilingual-cased"
BERT_PATH = "./bert_ckpt/"

res_dir = "../resources/"
train_dir = res_dir + "/youtube/train/"

#tf.random.set_seed(1234)
#np.random.seed(1234)

##############################################################################

# data 가져오기
data_refiner = DataRefiner()
data_refiner.load(train_dir)

data_inputs, data_labels, data_label_num = data_refiner.get_datas()

if DEBUG :
    print(f"\ndata_inputs size : {len(data_inputs)}")
    print(f"data_labels size : {len(data_labels)}")
    print(f"data_label_num : {data_label_num}\n")

##############################################################################

# Tokenizer 설정
npc_tokenizer = NPCTokenizer(BERT_NAME, BERT_PATH)

# Tokenizer 테스트
if TESTING :
    temp = "어차피 우승은 4조!!!"
    temp_ids, _, _ = npc_tokenizer.encode(temp, 20)
    print(f"temp_ids : {temp_ids}\n")

    id2word = npc_tokenizer.get_id2word()
    for temp_id in temp_ids :
        print(f"{temp_id} -> {id2word[temp_id]}")
    print()

# Tokenizer max_len 설정
npc_tokenizer.set_max_token_len(data_inputs)

if TESTING :
    temp = "어차피 우승은 4조!!!"
    temp_ids, _, _ = npc_tokenizer.encode(temp)
    print(f"temp_ids len : {len(temp_ids)}\n")

##############################################################################

# 학습 데이터 생성
used_len = 100
train_inputs = npc_tokenizer.make_model_inputs(data_inputs, used_len, True)
train_labels = np.array(data_labels[:used_len], dtype=np.int32)

#train_inputs = npc_tokenizer.make_model_inputs(data_inputs, debug=True)
#train_labels = np.array(data_labels, dtype=np.int32)

print(f"(len) input_ids_list : {len(train_inputs[0])}")
print(f"(len) attention_mask_list : {len(train_inputs[1])}")
print(f"(len) token_type_ids_list : {len(train_inputs[2])}")
print(f"(len) train_labels : {len(train_labels)}")

##############################################################################

# 모델 생성
optimizer = tf.keras.optimizers.Adam(3e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

npc_model = NPCModel(BERT_NAME, BERT_PATH, data_label_num)
npc_model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

# 모델 학습
NUM_EPOCHS = 100
BATCH_SIZE = 10
VALID_SPLIT = 0.1

#saved_model_path = "./saved_model/best_model_" + get_datetime_now()
#es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1, patience=10)
#mc = ModelCheckpoint(saved_model_path, monitor='accuracy', mode='auto', verbose=1, save_weights_only=True, save_best_only=True)
#history = npc_model.fit(train_inputs, train_labels, epochs=NUM_EPOCHS, batch_size=BATCH_SIZE, validation_split=VALID_SPLIT, callbacks=[es,mc])

##############################################################################

es_performance = 0.995
max_performance = 0

for i in range(NUM_EPOCHS) :
    history = npc_model.fit(train_inputs, train_labels, epochs=1, batch_size=BATCH_SIZE, validation_split=VALID_SPLIT)
    print(history)
    
    if i == 0 :
        npc_model.summary()
    
    # 에폭마다 사용자 평가
    performance = npc_model.performance_measure(train_inputs, train_labels, BATCH_SIZE)
    if max_performance < performance :
        max_performance = performance
        
        saved_model_path = "./saved_model/best_model_" + get_datetime_now() + ".h5"
        npc_model.save_weights(saved_model_path, save_format="h5")
    
    if es_performance <= performance :
        break
