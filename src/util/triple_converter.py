from util.data_loader import load_relation_tupl_from_text#,convert_str_to_tupl
from util.chara_dict import CharaDict
from util.noise_cleaner import normalize_name
import re


def concat_same_chara_relation(list_relation_tupl):

    chara_rel_dict = {}
    for chara1,relation,chara2 in list_relation_tupl:
        chara1_norm,chara2_norm = normalize_name(chara1),normalize_name(chara2)        
        relation_tupl_str = f"({chara1_norm},{relation},{chara2_norm})"

        if chara1 not in chara_rel_dict:
            chara_rel_dict[chara1] = {}
        chara_rel_dict[chara1][chara2] = chara_rel_dict[chara1].get(chara2,[])+[relation_tupl_str]
        
        if chara2 not in chara_rel_dict:
            chara_rel_dict[chara2] = {}
        chara_rel_dict[chara2][chara1] = chara_rel_dict[chara2].get(chara1,[])+[relation_tupl_str]
    return chara_rel_dict


def fix_same_chara_relation(chara1,chara2,input_str):
    if chara1==chara2:
        chara2 = "-"
    return chara1,chara2


def convert_str_to_tupl(triple_str):
    if triple_str=="None":return []
    triple_str = triple_str.replace("\"","")
    bracket_re = r"[^\(,]*?\([^,]*?\)[^\),]*?"
    bracket_re = r"[^\(,]*?\([^,]*?\)[^\),]*?"
    bracket_re = r"[^\(,]*?(?P<bracket>\([^\(\),]*?\))[^\),]*?"


    for ret in re.findall(bracket_re,triple_str):
        ret_fixed = ret.replace("(","（").replace(")","）")
        triple_str = triple_str.replace(ret,ret_fixed)

    triple_str = triple_str.replace(",","\",\"").replace("(","(\"").replace(")","\")").replace(")\",\"(","),(")
    try:
        triple = eval(triple_str) if "),(" in triple_str else [eval(triple_str)]
        return triple  
    except SyntaxError:
        return []
    except TypeError:
        return []

def load_triple_normalized_name(txtfile,convert_to_person_tag=True):
    dict_chara = {}#set()
    set_names = set()
    for li,(input_str,output_str, title, chara) in enumerate(load_relation_tupl_from_text(txtfile)):
        dict_chara[chara] = dict_chara.get(chara,len(dict_chara))
        for tupl in convert_str_to_tupl(output_str):
            if len(tupl)!=3:
                # print(li,tupl)
                continue
            chara1,chara2 = tupl[0],tupl[2]
            set_names.add(chara1);set_names.add(chara2)
    try:
        title
    except UnboundLocalError:
        return None,None,None,None
    chara_dict = CharaDict(list(dict_chara.keys()),normalize_subname=True)
    
    for name_in_sent in set_names:
        if name_in_sent in chara_dict.dict_subname:continue
        list_name_sub = chara_dict.get_name_list(name_in_sent)[0]
        list_name_norm = [name_sub for name_sub in list_name_sub if name_sub in chara_dict.dict_subname]
        if len(list_name_norm)==1:
            name_norm = list_name_norm[0]
            chara_dict.dict_subname[name_in_sent] = name_norm
        else:
            pass
    list_norm_tupl = []

    cnt_same_chara_relation, cnt_diff_chara_relation= 0,0
    for li,(input_str,output_str, title, chara) in enumerate(load_relation_tupl_from_text(txtfile)):
        dict_chara[chara] = dict_chara.get(chara,len(dict_chara))
        for tupl in convert_str_to_tupl(output_str):
            
            if len(tupl)!=3:
                continue
            
            chara1,chara2 = tupl[0],tupl[2]
            chara1,chara2 = fix_same_chara_relation(chara1,chara2,input_str+output_str+ title+ chara)
            try:
                chara1 =  chara_dict.dict_subname[chara1] if chara1!="-" else chara 
                chara2 =  chara_dict.dict_subname[chara2] if chara2!="-" else chara
            except Exception:continue
            # print([chara1,chara2,chara])
            
            if chara1 not in chara_dict.name_tag_dict or chara2 not in chara_dict.name_tag_dict:
                # print(chara1,chara2)
                continue
            chara_tag1,chara_tag2 = chara_dict.name_tag_dict[chara1],chara_dict.name_tag_dict[chara2]
            num1 = int(chara_tag1.replace("<PERSON","").replace(">",""))
            num2 = int(chara_tag2.replace("<PERSON","").replace(">",""))
            
            if convert_to_person_tag:
                chara1,chara2 = chara_tag1,chara_tag2
            norm_tupl = [chara1,tupl[1],chara2,num1,num2,max([num1,num2])]
            if num1==num2:
                # print(input_str,output_str,chara,chara1,chara2)
                cnt_same_chara_relation+=1
            else:
                list_norm_tupl.append(norm_tupl)
                cnt_diff_chara_relation+=1
            # print(norm_tupl)
    return list_norm_tupl,title,cnt_same_chara_relation, cnt_diff_chara_relation

def normalize_relation_to_mermaidjsrule(list_norm_tupl):
    del_letters = ["“","「","」"]
    replace_bracket = lambda rel:rel.replace("「","").replace("」","").replace("“","")
    list_norm_tupl = [(chara1,replace_bracket(rel),chara2,cnum1,cnum2,mnum) for chara1,rel,chara2,cnum1,cnum2,mnum in list_norm_tupl]
    return list_norm_tupl

def reduce_relation_of_same_characters(list_norm_tupl,thre=4):
    charas_rel_dict = {}
    new_list_norm_tupl = []
    for chara1,rel,chara2,chara_num1,chara_num2,max_num in list_norm_tupl:
        charas_key = "-".join(sorted([chara1,chara2]))
        charas_rel_dict[charas_key] = charas_rel_dict.get(charas_key,0)+1
        if charas_rel_dict[charas_key]>thre:continue
        new_list_norm_tupl.append([chara1,rel,chara2,chara_num1,chara_num2,max_num])

    return new_list_norm_tupl