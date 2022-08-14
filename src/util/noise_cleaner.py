import re



def delete_template(profile_text):
    "初登場回-第14シリーズ第1話『さよなら電ボ』"
    profile_text = re.sub("初登場回-.*?第[0-9]{,3}話『.*?』","",profile_text)
    profile_text = re.sub("（声.*?）","",profile_text)
    profile_text = re.sub("（演.*?）","",profile_text)
    
    profile_text = profile_text.replace("｡","。")
    list_profile_sentence = profile_text.split("。")
    list_new_profile = []
    list_del_template = ["初登場回","未登場","で初登場","にて初登場","に登場","から登場","誕生日は","日生まれ","演‐","声:","声-","声−","演-","声:","初登場:","声:","登場:","版オリジナルキャラクター","声優:"]
    for profile_sentence in list_profile_sentence:
        if len([0 for delete_template in list_del_template if delete_template in profile_sentence])>0:
            continue
        if "声:" in profile_sentence:
            print(profile_sentence)

        list_new_profile.append(profile_sentence)
    new_profile = "。".join(list_new_profile)
    return new_profile
    
def delete_noise(line):
    line = re.sub("\{\{see|.*?\}\}","",line).strip()
    return line


# def dele(chara):
#     chara = re.sub("（.*?）","",chara)
#     chara = re.sub("〈.*?〉","",chara)
#     chara = re.sub(r"[\(（].*?[\)）]"," ",chara)
#     chara = re.sub("&quot&gt.*?&lt/span&gt","",chara)
#     chara = chara.replace(" ","")
#     return chara

def normalize_name(charaname):
    def omit_yomigana(charaname):
        if len(charaname.split("|"))==1:return charaname
        list_charaname = [charaname for charaname in charaname.split("|") if not re_hiragana.fullmatch(charaname) and len(charaname)>0]
        return list_charaname[0]

    charaname = re.sub("\&lt;ref group=\&quot;.*?\&lt;/ref&gt;","",charaname)
    charaname = re.sub("\{読み仮名|\{\{Anchors\|.*?\}\}","",charaname)
    charaname = re.sub("\{Visible anchor|","",charaname)
    charaname = charaname.replace("; ","").replace(";","")
    charaname = re.sub("（.*?）","",charaname) if len(re.sub("（.*?）","",charaname))>0 else charaname
    charaname = re.sub("〈.*?〉","",charaname) if len(re.sub("〈.*?〉","",charaname))>0 else charaname
    charaname = re.sub(r"[\(（].*?[\)）]"," ",charaname) if len(re.sub(r"[\(（].*?[\)）]","",charaname))>0 else charaname
    charaname = re.sub("&quot&gt.*?&lt/span&gt","",charaname)
    charaname = charaname.replace(" ","")
    
    # charaname = charaname.replace("||","|").replace(";","")
    # charaname = charaname.split("|")[0]

    charaname = charaname.replace("[","").replace("]","")
    charaname = charaname.replace("{","").replace("}","")
    charaname = charaname.replace("===","")
    if len(charaname)==0:return None
    while charaname[0] == "|":
        charaname = charaname[1:]
    # charaname = omit_yomigana(charaname)
    charaname = charaname.strip()
    charaname = charaname.replace("&ltspanid=&quot","")
    return charaname

def normalize_description(description):
    if description[0]==":":
        description = description[1:]
    description = description.replace(": ","").strip()
    description = description.replace("[[","").replace("]]","")
    description = description.replace("'''","")
    description = re.sub("\[http.*?\]","",description)
    description = re.sub("\{\{.*?\}\}","",description)
    description = re.sub("&lt;ref name=&quot;.*?&quot; /&gt","",description)
    description = re.sub("&lt;ref name=&quot;.*?&quot; ?/&gt;", "", description)
    description = re.sub("&lt;ref name=&quot;.*?&quot; ?/&gt", "", description)
    description = re.sub("&lt.*?&gt;?", "", description)
    description = re.sub("\{\{Twitter status.*?\}\}", "", description)
    description = re.sub("\&lt;ref group\=\&quot;.*?\&lt;/ref\&gt;","",description)
    description = re.sub("&lt;.*?&lt;/ref&gt;","",description)
    description = description.replace(";","").replace(" ","")
    description = description.replace("}}","")
    description = description.replace("。。","。")
    
    if "声-" in description and description[-1]!="。":
        description = description+"。"    
        # print(description);raise Exception
    if len(description)>0:
        if description[-1] not in set("!?！？。"):
            description = description+"。"
    description = description.replace("。。","。")
    return description
    