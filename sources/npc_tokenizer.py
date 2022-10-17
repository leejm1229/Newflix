# from commons import *
from sources.commons import *
from transformers import BertTokenizer

##############################################################################
BERT_NAME = "bert-base-multilingual-cased"
BERT_PATH = "bert_ckpt"
class NPCTokenizer :
    def __init__(self, bert_name: str, bert_path: str) :
        self.bert_name, self.bert_path = bert_name, bert_path
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_name, cache_dir=self.bert_path)
        
        self.word2id = self.tokenizer.get_vocab()
        self.id2word = {id:word for id, word in enumerate(self.word2id)}
        
        self.max_token_len = 0
    
    ##############################################################################
    
    def get_word2id(self) :
        return self.word2id

    def get_id2word(self) :
        return self.id2word

    ##############################################################################
    
    def set_max_token_len(self, inputs: list) :
        for input in inputs :
            token_len = len(self.tokenizer.encode(input))
            
            if self.max_token_len < token_len :
                self.max_token_len = token_len

    
    def get_max_token_len(self) :
        return self.max_token_len

    ##############################################################################
    
    def encode(self, input: str, max_token_len=-1) :
        if max_token_len == -1 :
            max_token_len = self.max_token_len
        
        encoded = self.tokenizer.encode_plus(text=input, max_length=max_token_len,
                                             add_special_tokens=True, truncation=True,
                                             padding='max_length', return_attention_mask=True)
        
        input_ids = encoded['input_ids']
        attention_mask = encoded['attention_mask']
        token_type_ids = encoded['token_type_ids']
    
        return input_ids, attention_mask, token_type_ids

    def make_model_inputs(self, data_inputs, used_len=-1, debug=False) :
        input_ids_list = []
        attention_mask_list = []
        token_type_ids_list = []
        
        for i in range(len(data_inputs)) :
            input_ids, attention_mask, token_type_ids = self.encode(data_inputs[i])
            
            
            input_ids_list.append(input_ids)
            attention_mask_list.append(attention_mask)
            token_type_ids_list.append(token_type_ids)
        
        if used_len > 0 :
            input_ids_list = input_ids_list[:used_len]
            attention_mask_list = attention_mask_list[:used_len]
            token_type_ids_list = token_type_ids_list[:used_len]
        
        input_ids_list = np.array(input_ids_list, dtype=int)
        attention_mask_list = np.array(attention_mask_list, dtype=int)
        token_type_ids_list = np.array(token_type_ids_list, dtype=int)
        
        model_inputs = (input_ids_list, attention_mask_list, token_type_ids_list)
        return model_inputs

tokenizer = NPCTokenizer(BERT_NAME, BERT_PATH)