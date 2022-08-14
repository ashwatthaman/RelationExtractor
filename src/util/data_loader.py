import codecs,glob,os
import codecs,re
import bz2
from util.regexp import match_chara_re,match_title_re,is_chara

def get_title(file_path):
    title = file_path.split("/")[-1].replace(".txt","").replace("mldata_","")
    return title
    
def does_exists(title,root_path,list_dir_type="all"):        
    list_dir = get_list_dir(list_dir_type)
    for dirname in list_dir:
        txtfile_tmp = f"{root_path}/{dirname}/mldata_{title}.txt"
        if os.path.exists(txtfile_tmp):
            return True
    return False


def load_xml_generator(xmlfile):
    with bz2.open(xmlfile,"rb") as f:
        for line in f:
            line = line.decode().strip()
            title,is_title = match_title_re(line,"")
            if is_title:break
        list_line = []
        for line in f:
            line = line.decode().strip()
            title_tmp,is_title = match_title_re(line,title)
            if is_title:
                if is_chara(list_line):
                    yield list_line,title
                title = title_tmp
                list_line = []
            list_line.append(line)  

def get_list_dir(list_dir_type):
    common_path = "./mldata/relext/"
    assert list_dir_type in ["train","validation","augmentation","augmented","annotated","all","rulebased"]
    if list_dir_type=="train":
        list_dir = ["/mldata/mldata_3tupls/","/mldata/mldata_all_train/","/ml_annotated/"]
    elif list_dir_type=="validation":
        list_dir = ["/mldata_all_validation/"]
    elif list_dir_type=="augmentation":
        list_dir = ["/mldata_to_be_augmented/"]
    elif list_dir_type=="augmented":
        list_dir = ["/ml_generated/"]
    elif list_dir_type=="annotated":
        list_dir = ["/ml_annotated/"]
    elif list_dir_type=="all":
        list_dir = ["/mldata_3tupls/","/mldata_all_train/","/mldata_all_validation/","/ml_generated/","/ml_annotated/"]
    elif list_dir_type=="rulebased":
        list_dir = ["//mldata_3tupls/"]    
    list_dir = [common_path+dirname for dirname in list_dir]
    return list_dir
       

def load_relation_tupl_from_text(txtfile):
    title = txtfile.split("/")[-1].replace(".txt","")
            
    lines = [line.strip() for line in codecs.open(txtfile,encoding="utf-8")][:-1]
    for line in lines:
        line = line.strip()
        len_line = len(line.split("|"))
        if len_line<2:
            print("onlytwo",line)
        if len_line==3:
            output_str,input_str,chara = line.split("|")
        elif len_line==2:
            output_str,input_str = line.split("|")
            chara = "?"
        if output_str in ["one","(-,,-)"]:output_str="None"
        yield input_str,output_str, title, chara

def get_txtlist_from_dir(list_dir_type,root_path):
    list_dir = get_list_dir(list_dir_type)
    for dirname in list_dir:
        print(dirname)
        assert os.path.exists(root_path+dirname)  
    list_txtfile = [txtfile for dirname in list_dir for txtfile in glob.glob(root_path+dirname+"/*.txt")]
    return list_txtfile

def load_profile_dict(mlfile):
    profile_dict = {}
    lines = [line.strip() for line in codecs.open(mlfile,encoding="utf-8")][:-1]
    for line in lines:
        line = line.strip()
        len_line = len(line.split("|"))
        if len_line<3:
            print("lessthanthree",line)
            continue
        if len_line==3:
            output_str,input_str,chara = line.split("|")
        profile_dict[chara] = profile_dict.get(chara,[])+[input_str]

    profile_dict = {chara:"。".join(list_profile)+"。" for chara,list_profile in profile_dict.items()}
    return profile_dict

if __name__=="__main__":
    list_txtfile = get_txtlist_from_dir("train","../../data/")
    print(len(list_txtfile))
    list_txtfile = get_txtlist_from_dir("augmentation","../../data/")
    print(len(list_txtfile))