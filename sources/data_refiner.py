from sources.commons import *

from sources import file_util, string_util, container_util


###########################################################################################

class DataRefiner :
    def __init__(self) :
        self.inputs = []
        self.labels = []

    def get_datas(self) :
        if len(self.inputs) == len(self.labels) :
            return self.inputs, self.labels, self.get_label_num()

        return None, None, 0

    def get_label_num(self) :
        if len(self.labels) > 0 :
            label_set = set()
            
            for label in self.labels :
                label_set.add(label)
            
            return len(label_set)
    
        return 0

    ############ƒ###############################################################################
    
    def load(self, in_path: str, doc_max_count=-1) :
        in_file_paths = file_util.get_file_paths(in_path, True)
        doc_count = 0
        
        for in_file_path in in_file_paths :
            if (0 < doc_count) and (doc_max_count <= doc_count) :
                break
            
            inputs, labels = self.parsing_file_txt(in_file_path)
            
            if (len(inputs) > 0) and (len(inputs) == len(labels)) :
                self.inputs.extend(inputs)
                self.labels.extend(labels)
            
            doc_count += 1
    
        self.print_datas()

    def parsing_file_txt(self, in_file_path: str, encoding=ENCODING, delim_key=DELIM_KEY) :
        inputs, labels = [], []
        
        in_file = file_util.open_file(in_file_path, encoding, 'r')
        
        while 1 :
            line = in_file.readline()
            if not line :
                break
            
            temp = line.split(delim_key)
            temp = string_util.trim(temp)
            
            if len(temp) < 5 :
                continue
            
            inputs.append(temp[3])
            labels.append(temp[4])

        return inputs, labels

    ###########################################################################################
    
    def print_datas(self) :
        input_size = len(self.inputs)
        label_size = len(self.labels)
        
        # logging(f"DataRefiner.print_datas() input size : {input_size}, label size : {label_size}\n")
        
        label_dict = {}
        for label in self.labels :
            container_util.add_str_int(label_dict, label, 1)
        
        label_dict = container_util.sorted_dict(label_dict)
        # for label in label_dict.keys() :
        #     logging(f"DataRefiner.print_datas() label : {label}, freq : {label_dict[label]}")

###########################################################################################

if __name__ == "__main__" :
    res_dir = "../resources/"
    
    train_dir = res_dir + "/youtube/train/"
    
    data_refiner = DataRefiner()
    data_refiner.load(train_dir)
