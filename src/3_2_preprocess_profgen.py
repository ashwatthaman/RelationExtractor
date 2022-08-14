import pandas,codecs
import os,random,glob

from util.noise_cleaner import delete_template,normalize_name
from util.triple_converter import concat_same_chara_relation,load_triple_normalized_name
from util.data_loader import get_list_dir,load_profile_dict

data_path = "../mldata/profgen"
if not os.path.exists:os.mkdir(data_path)

def get_relation_profile():
    list_dir = get_list_dir("augmented")
    list_dir+= get_list_dir("annotated")
    list_mlfile = [mlfile for dirname in list_dir for mlfile in glob.glob(f"../"+dirname+"/mldata*.txt")]
    savename = "data.pickle"
    list_input,list_relation,list_output = [],[],[]
    for mlfile in list_mlfile:
        list_norm_tupl,_,cnt_same_chara_relation, cnt_diff_chara_relation = load_triple_normalized_name(mlfile,convert_to_person_tag=False)
        if list_norm_tupl is None:continue
        list_relation_tupl = [tupl[:3] for tupl in list_norm_tupl]
        profile_dict = load_profile_dict(mlfile)


        chara_rel_dict = concat_same_chara_relation(list_relation_tupl)
        for chara1,rel_dict in chara_rel_dict.items():
            prof1 = profile_dict[chara1]
            chara1_norm = normalize_name(chara1)

            for chara2,list_relation_str in rel_dict.items():
                prof2 = profile_dict[chara2]
                list_input.append(prof1)
                list_relation.append(chara1_norm+",".join(list_relation_str))
                list_output.append(prof2)
        
    df_dict = {"input":list_input,"relation":list_relation,"output":list_output}
    # print(len(list_input))
    pandas.DataFrame(df_dict).to_pickle(f"{data_path}/{savename}")    

def make_train_data_rel(letter_thre=10):
    def write_file(trdvte,list_src,list_tgt):
        list_ind = [ri for ri in range(len(list_src))]
        random.shuffle(list_ind)
        list_src = [list_src[ind] for ind in list_ind]
        list_tgt = [list_tgt[ind] for ind in list_ind]
        dirname = f"mldata_rel"
        if not os.path.exists(dirname):os.mkdir(dirname)
        fw_src = codecs.open(f"{data_path}/{trdvte}.src-tgt.src", "w", encoding="utf-8")
        fw_tgt = codecs.open(f"{data_path}/{trdvte}.src-tgt.tgt", "w", encoding="utf-8")

        fw_src.write("\n".join(list_src));
        fw_src.close()
        fw_tgt.write("\n".join(list_tgt));
        fw_tgt.close()
    df = pandas.read_pickle(f"{data_path}/data.pickle")
    df = df.dropna(subset=["input","relation","output"])
    df = df.sample(frac=1)
    list_input_tokenized = []
    list_output_tokenized = []

    for prof1,relation,prof2 in zip(df["input"],df["relation"],df["output"]):

        prof1 = delete_template(prof1)
        if len(prof1.strip()) < letter_thre: continue
        prof2 = delete_template(prof2)
        if len(prof2.strip()) < letter_thre: continue
        
        list_input_tokenized.append(relation+prof1)

        list_output_tokenized.append(prof2)

    list_src_tr,list_src_dv,list_src_te = list_input_tokenized[:-2000],list_input_tokenized[-2000:-1000],list_input_tokenized[-1000:]
    list_tgt_tr,list_tgt_dv,list_tgt_te = list_output_tokenized[:-2000],list_output_tokenized[-2000:-1000],list_output_tokenized[-1000:]

    write_file("train",list_src_tr,list_tgt_tr)
    write_file("valid",list_src_dv,list_tgt_dv)
    write_file("test",list_src_te,list_tgt_te)


if __name__=="__main__":
    get_relation_profile()
    make_train_data_rel()