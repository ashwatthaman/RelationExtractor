import os,pandas,codecs
from util.noise_cleaner import normalize_description,normalize_name
from util.regexp import re_chara3

def write_csv(li,title,list_chara_description,csv_path="csv",overwrite=True):
    csvname = f"{csv_path}/{title}.csv"
    if not os.path.exists(f"{csv_path}"):os.mkdir(f"{csv_path}")
    if os.path.exists(csvname) and not overwrite:return

    chara_desc_dict = {}
    chara = None
    for line in list_chara_description:
        if len(line)==0:continue
        if line[0]==";" or "=== " in line or re_chara3.fullmatch(line):
            chara = normalize_name(line)
            if chara is None:continue
        elif line[0]==":":
            if chara is None:continue
            try:
                chara_desc_dict[chara] = chara_desc_dict.get(chara,"") + normalize_description(line)
            except Exception:
                print(line)
                print(title,list_chara_description);break
    if len(chara_desc_dict)==0:return None
    df_dict = {"chara":list(chara_desc_dict.keys()),"description":list(chara_desc_dict.values())}
    pandas.DataFrame(df_dict).to_csv(csvname)

def write_txt(li,title,list_chara_description,txt_path="txt",overwrite=True):
    # title = normalize_title(title)
    txtname = f"{txt_path}/{title}.txt"
    if not os.path.exists(f"{txt_path}"):os.mkdir(f"{txt_path}")
    if os.path.exists(txtname) and not overwrite:return
    fw = codecs.open(txtname,"w",encoding="utf-8")
    fw.write("\n".join(list_chara_description))
    fw.close()