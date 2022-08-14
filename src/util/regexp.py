import re

re_hiragana = re.compile(r'^[あ-ん]+$')
re_chara3 = re.compile("\* .*?：\[\[.*?\]\]")

# title_re = "<title>"
# title_re = "<title>:^*?</title>"
title_re = "<title>(?P<title>[^:]*?)</title>"

charasection_re = "== 登場人物 =="
charasection_re2 = "== 登場キャラクター =="
charasection_re3 = "== キャラクター =="
re_dict = {charasection_re:"csv",charasection_re2:"csv_tojochara",charasection_re3:"csv_chara"}
is_section_re = lambda line:True if "== " in line and "=== " not in line else False

def is_chara(list_line):
    for line in list_line:
        is_charasection,csv_path = match_chara_re(line)
        if is_charasection:return True
    return False

def match_chara_re(line):
    is_charasection = True
    if charasection_re in line:
        csv_path = re_dict[charasection_re]
    elif charasection_re2 in line:
        csv_path = re_dict[charasection_re2]
    elif charasection_re3 in line:
        csv_path = re_dict[charasection_re3]
    # elif "マハーバーラタ" in line:
        # csv_path = "csv_mahabharata"
    else:
        is_charasection = False
        csv_path = None
    return is_charasection,csv_path


def match_title_re(line,title):
    match = re.search(title_re,line)
    if match is None:
         return title,False
    # print(match)
    # print(match.group("title"))
    title = match.group("title")
    title = title.strip().replace(" ", "")
    title = title.replace("/", "／")
    return title,True


if __name__=="__main__":
    # line ="<title>PHPプログラミング言語</title>"
    # print(match_title_re(line,""))
    line ="<title>Category:PHPプログラミング言語</title>"
    print(match_title_re(line,""))