# RelationExtractor

C100で執筆した「キャラクターの関係性を考慮したAIの考えるキャラクター設定」のコードです。
記事では以下の3ステップを実行しました。

1. 関係性抽出部分
2. 相関図生成部分
3. プロフィール生成部分

現状コードがあるのは1.と3.の部分です。

1.に対応するコードは、

1_1_download_wiki.sh

1_2_scrape_xml.py



であり、3.に対応するコードは

3_1_download_relation_file.sh

3_2_preprocess_profgen.py

3_3_train_relation_profile_generator.ipynb

です。

python=3.8.3で実行確認済です。

*.pyファイルは、現状はpandasのみ必要です。

pip install pandas==1.4.3



*.pyファイル自体はどこのディレクトリで実行しても問題ないですが、

*.ipynbファイルはGoogle Colab上で実行することを想定しております。

フォルダの置く場所としては、{Googleドライブのフォルダがある場所}/codes/my_github/

です。

上記フォルダに移動して、

git clone https://github.com/ashwatthaman/RelationExtractor.git

などとするかダウンロードしたzipを展開してください。

1. 関係性抽出部分については一応コードは載せてありますが、これだけでは2以降のステップに進めず、人手の教師データ作成が必要になります。
3. から始めると、プロフィール生成モデルの学習が行えます。

#wiki data のダウンロードと前処理


1_1_download_wiki.sh

1_2_scrape_xml.py            

---------------------------ここで人手の前処理が必要--------------------------

3_1_download_relation_file.sh // 人手で作成した関係抽出モデルから得られた関係性データのダウンロード。

3_2_preprocess_profgen.py // 関係性データの前処理。

3_3_train_relation_profile_generator.ipynb // 関係性データを使ったプロフィール文生成。

注: 3_3_train_relation_profile_generator.ipynbはGoogle Colab上で実行してください。
