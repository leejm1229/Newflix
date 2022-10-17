from sources.commons import *

###########################################################################################

def get_file_name(file_path: str, rm_ext_flag=False) :
    file_name = os.path.basename(file_path)

    if rm_ext_flag :
        idx = file_name.rfind(FILE_EXT)

        if idx != -1 :
            file_name = file_name[:idx]
    
    return file_name

def get_file_paths(in_dir: str, inner_flag: bool) :
    file_paths = []
    count = 0
    if inner_flag :
        for (parent_path, dirs, file_names) in os.walk(in_dir) :
            for file_name in file_names :
                file_path = os.path.join(parent_path, file_name)

                if os.path.isfile(file_path) :
                    file_paths.append(file_path)
                    count=+1
                if count == 2:
                    break
    else :
        file_names = os.listdir(in_dir)
        for file_name in file_names :
            file_path = os.path.join(in_dir, file_name)

            if os.path.isfile(file_path) :
                file_paths.append(file_path)

    return file_paths

def get_cnt_file(in_dir: str, inner_flag: bool) :
    file_cnt = 0

    if inner_flag :
        for (parent_path, dirs, file_names) in os.walk(in_dir) :
                for file_name in file_names :
                    file_path = os.path.join(parent_path, file_name)

                    if os.path.isfile(file_path) :
                        file_cnt += 1
    else :
        file_names = os.listdir(in_dir)
        for file_name in file_names :
            file_path = os.path.join(in_dir, file_name)

            if os.path.isfile(file_path) :
                file_cnt += 1

    return file_cnt

###########################################################################################

def exists(file_path: str) :
    if file_path == None or len(file_path) == 0 :
        return False

    if os.path.exists(file_path) and os.path.isfile(file_path) :
        return True

    return False

def make_parent(file_path: str) :
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def open_file(file_path: str, encoding: str, mode: str) :
    if mode == 'w' :
        make_parent(file_path)

    if len(encoding) == 0 :
        return open(file_path, mode)
    else :
        return open(file_path, mode, encoding=encoding)

###########################################################################################

def write_dict(out_file_path: str, encoding: str, out_dict: dict, delim: str) :
    file = open_file(out_file_path, encoding, 'w')

    items = out_dict.items()
    for item in items :
        file.write(f"{item[0]}{delim}{item[1]}\n")
    
    file.close()