
from util.noise_cleaner import delete_noise
from writer.csvtxt_writer import write_txt,write_csv
from util.regexp import match_chara_re,match_title_re,is_section_re
from util.data_loader import load_xml_generator
#適宜書き換えてください。
import os
# xmlfile = os.environ["HOME"]+"/Downloads/jawiki-latest-pages-articles.xml.bz2"
xmlfile = "./jawiki-latest-pages-articles.xml.bz2"


def get_chara_description(list_line):
    chara_flag = False
    for li,line in enumerate(list_line):
        is_charasection,cpath = match_chara_re(line)
        if is_charasection:
            _,csv_path = match_chara_re(line)        
            chara_flag = True
            list_chara_description = []
            continue
        if chara_flag:
            if is_section_re(line):
                chara_flag = False
            else:
                line = delete_noise(line)
                if len(line)>0:
                    list_chara_description.append(line)
    return list_chara_description

def main():
    txt_path = "../data/txt/"
    csv_path = "../data/csv/"
    if not os.path.exists(txt_path):os.makedirs(txt_path)
    if not os.path.exists(csv_path):os.makedirs(csv_path)
    for li,(list_line,title) in enumerate(load_xml_generator(xmlfile)):
        write_txt(li,title,list_line,txt_path=txt_path)
        list_chara_description = get_chara_description(list_line)
        write_csv(li,title,list_chara_description,csv_path=csv_path)
        
if __name__=="__main__":
    main()