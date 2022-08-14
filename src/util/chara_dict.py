# from pyrsistent import s
# from pororo import Pororo
# ner_model = Pororo(task="ner", lang="ja")
import re

class CharaDict():

    def __init__(self,list_name,normalize_subname):
        self.normalize_subname = normalize_subname
        self.list_subname,self.dict_subname = self.get_name_list_iter(list_name)
        self.name_tag_dict,self.tag_name_dict = self.make_name_tag_dict(list_name)
        # for name,tag in self.name_tag_dict.items():
            # print("name",name,"tag",tag)

    def get_name_list_iter(self,list_name):
        list_subname,dict_subname =[],{}
        for name in list_name:
            list_subname_each,dict_subname_each = self.get_name_list(name)
            list_subname+=list_subname_each
            dict_subname = {**dict_subname_each,**dict_subname}
        return list_subname,dict_subname


    def get_name_list(self,name_raw):
        list_name = [name_raw]
        list_bracket = [match.group("name") for match in re.finditer(r"[\(（](?P<name>.*?)[\)）]",name_raw)]
        list_name+=list_bracket
        
        name = re.sub(r"[\(（].*?[\)）]"," ",name_raw)
        
        list_name.append(name)

        separate_key = "<separate_key>"
        
        for name in list_name[:]:
            for kigou in list("・/／ | ")+["&quot&gt","&lt/span&gt"]:
                name = name.replace(kigou,separate_key)
            for name_sub in name.split(separate_key):
                if len(name_sub)>1:
                    list_name.append(name_sub)
            for katagaki in ["班長","大佐","少佐","軍曹","先生"]:
                if katagaki in name and name.replace(katagaki,"")!="":
                    list_name.append(name.replace(katagaki,""))
        list_name = sorted(list_name,key=lambda s:len(s),reverse=True)
        dict_name = {name_sub:name_raw for name_sub in list_name}
        return list_name,dict_name

    def make_name_tag_dict(self,list_name):
        if not self.normalize_subname:
            list_name = set([name for name in  self.dict_subname.keys()])
        name_tag_dict = {name:f"<PERSON{ri}>" for ri,name in enumerate(list_name)}
        tag_name_dict = {tag:name for name,tag in name_tag_dict.items()}
        return name_tag_dict,tag_name_dict

    # def replace_ner(self,text):
    #     def get_name_in_dict(name_cand,dict_subname,name_tag_dict,normalize_subname):
    #         if normalize_subname:
    #             if name_cand in dict_subname:
    #                 return name_tag_dict[dict_subname[name_cand]]#person_tag
    #         else:
    #             if name_cand in name_tag_dict:
    #                 return name_tag_dict[name_cand]
    #         list_name = [name for name in set(dict_subname.values()) if name_cand in name and name_cand+"の" not in name]
    #         if len(list_name)==1:
    #             if normalize_subname:
    #                 return name_tag_dict[list_name[0]]
    #             else:
    #                 return name_tag_dict[name_cand]
    #         else:
    #             return name_cand
    #     list_word = []
    #     for sentence in [s for s in text.split("。") if len(s)>0]:
    #         ner_result = ner_model(sentence)
    #         list_word += [get_name_in_dict(name_cand,self.dict_subname,self.name_tag_dict,self.normalize_subname) if tag=="PERSON" else name_cand for name_cand,tag in ner_result]+["。"]
    #     return "".join(list_word)#,name_tag_dict

    # def replace_name_to_tag(self,profile):
    #     profile = self.replace_ner(profile)
    #     for name in self.list_subname:
    #         if self.normalize_subname:
    #             person_tag = self.name_tag_dict[self.dict_subname[name]]
    #         else:
    #             person_tag = self.name_tag_dict[name]
    #         if name in profile:
    #             # print(name,person_tag,profile)
    #             profile = profile.replace(name,person_tag)
    #     return profile
        

    # def add_names_from_ner(self,list_text):
    #     for text in list_text:
    #         for sentence in [s for s in text.split("。") if len(s)>0]:
    #             ner_result = ner_model(sentence)
    #             for name_cand,tag in ner_result:
    #                 if tag=="PERSON":
    #                     if name_cand not in self.name_tag_dict:  
    #                         list_name = [name for name in set(self.dict_subname.values()) if name_cand in name and name_cand+"の" not in name]
    #                         if len(list_name)==1:
    #                             if self.normalize_subname:
    #                                 self.dict_subname[name_cand] = list_name[0]
    #                             else:
    #                                 # print("NOTIN",name_cand,len(list_name),len(self.name_tag_dict))                                 
    #                                 self.name_tag_dict[name_cand] = f"<PERSON{len(self.name_tag_dict)}>"
    #                                 self.tag_name_dict[self.name_tag_dict[name_cand]] = name_cand
    #                                 # print("NOTIN",name_cand,len(list_name),len(self.name_tag_dict))                                 
                                    
