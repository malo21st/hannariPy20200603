## hannariPy20200603
# Dash Hands On #6 / Dashの復讐と実践例

- 2020/06/03(水) 21:00 〜 23:00
- オンライン
- https://hannari-python.connpass.com/event/176708/

## ファイルとフォルダの説明
- Dashで作成したアプリの紹介・解説.pdf：説明資料

- index.py：ターミナルから python index.py で起動。control + c で停止。
- app.py：Dashのappインスタンスを生成
* apps：index.pyを実行すると、app0.py〜app4.pyをタブで選べます。
  - app0.py：福岡県の交通事故のダッシュボード
  - app1.py：最短経路のＳＰＡ（Single Page Application）
  - app2.py：【実験】グラフのFigureのコールバック
  - app3.py：【実験】Cytoscapeのelementsプロパティ
  - app4.py：【実験】DataTableとCytoscapeの連携
  - h29.csv：app0.pyで使用する交通事故データ
  - my_style.py：app.1.pyで使用する書式データ
  - table_to_cyto.py：app1.pyで使用するデータ変換の関数
* single_page：単体で起動するapp0.py〜app4.pyを収めたフォルダ
