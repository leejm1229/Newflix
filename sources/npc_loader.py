from sources.commons import *
import tensorflow as tf
from sources.data_refiner import DataRefiner
from sources.npc_tokenizer import NPCTokenizer
from sources.npc_model import NPCModel

##############################################################################

DEBUG = True
TESTING = False

BERT_NAME = "bert-base-multilingual-cased"
BERT_PATH = "./bert_ckpt/"

res_dir = "./resources/"
train_dir = res_dir + "/youtube/train/"

##############################################################################

npc_tokenizer = NPCTokenizer(BERT_NAME, BERT_PATH)

def load_model():
    # data 가져오기
    data_refiner = DataRefiner()
    data_refiner.load(train_dir)

    data_inputs, data_labels, data_label_num = data_refiner.get_datas()
    ##############################################################################

    # Tokenizer max_len 설정
    npc_tokenizer.set_max_token_len(data_inputs)

    ##############################################################################

    # 학습 데이터 생성
    used_len = 5
    train_inputs = npc_tokenizer.make_model_inputs(data_inputs, used_len, True)
    train_labels = np.array(data_labels[:used_len], dtype=np.int32)

    ##############################################################################

    # 모델 생성
    optimizer = tf.keras.optimizers.Adam(3e-5)
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

    npc_model = NPCModel(BERT_NAME, BERT_PATH, data_label_num)
    npc_model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

    npc_model.fit(train_inputs, train_labels, epochs=1, batch_size=2, validation_split=0.1)

    saved_model_path = "./saved_model/best_model.h5"
    npc_model.load_weights(saved_model_path)
    
    return npc_model

npc_model = load_model()

