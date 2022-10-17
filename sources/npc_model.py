from sources.commons import *

import tensorflow as tf
from transformers import TFBertModel

##############################################################################

class NPCModel(tf.keras.Model) :
    def __init__(self, bert_name: str, bert_path: str, num_class: int, dropout_prob=0.1) :
        super(NPCModel, self).__init__()
        
        self.bert = TFBertModel.from_pretrained(bert_name, cache_dir=bert_path)
        self.hidden_layer1 = tf.keras.layers.Dense(256, activation='relu', name='hidden_layer1')
        self.hidden_layer2 = tf.keras.layers.Dense(128, activation='relu', name='hidden_layer2')
        
        output_kernel_initializer = tf.keras.initializers.TruncatedNormal(self.bert.config.initializer_range)
        self.output_layer = tf.keras.layers.Dense(num_class, kernel_initializer=output_kernel_initializer, name="output_layer")

    def call(self, input_ids, attention_mask=None, token_type_ids=None, training=False) :
        out = self.bert(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        out = out[1]
        out = self.hidden_layer1(out)
        out = self.hidden_layer2(out)
        out = self.output_layer(out)
        
        return out

    # def performance_measure(self, train_inputs, train_labels, batch_size=1) :
    #     input_len = len(train_labels)
    #     count_predict_false = 0
    #     count_predict_true = 0
    #     count_label_false = 0
    #     count_label_true = 0
        
    #     predicts = self.predict(train_inputs, batch_size=batch_size)
    #     count_matched_false = 0
    #     count_matched_true = 0
        
    #     for i in range(input_len) :
    #         predict = np.argmax(predicts[i])
    #         label = train_labels[i]
            
    #         if predict == 0 : count_predict_false += 1
    #         if predict == 1 : count_predict_true += 1
    #         if label == 0 : count_label_false += 1
    #         if label == 1 : count_label_true += 1
            
    #         if predict == label :
    #             if predict == 0 :
    #                 count_matched_false += 1
    #             else :
    #                 count_matched_true += 1
        
    #     print(f"\ncount_predict (T/F) : {count_predict_true}/{count_predict_false}")
    #     print(f"count_label (T/F) : {count_label_true}/{count_label_false}")
    #     print(f"count_matched (T/F) : {count_matched_true}/{count_matched_false}\n")
        
    #     print(f"count_predict : {count_predict_false+count_predict_true}")
    #     print(f"count_label : {count_label_false+count_label_true}")
    #     print(f"count_matched : {count_matched_false+count_matched_true}\n")
        
    #     performance_true = count_matched_true / count_label_true
    #     print(f"performance (T) : ({count_matched_true}/{count_label_true}) : {performance_true}")
    #     performance_false = count_matched_false / count_label_false
    #     print(f"performance (F) : ({count_matched_false}/{count_label_false}) : {performance_false}\n")
        
    #     count_matched = count_matched_true+count_matched_false
    #     performance = count_matched / input_len
    #     print(f"{count_matched} --> performance : {performance}\n\n")
        
    #     return performance