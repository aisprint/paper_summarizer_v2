### 論文サマライザー

## 概要
このプロジェクトは、OpenAIとAnthropic、Google DeepMindのLLMを使用してPDF論文を要約するStreamlitアプリケーションです。

## デモ
アプリは以下のStreamlitサーバーで利用できます：
[Paper Summarizer V2](https://papersummarizerv2-ertgst946lkt3qpqf5cxup.streamlit.app/)

## アプリの使い方

1. 使用するモデルのAPIキーを取得し、左のサイドバーのAPIキー欄に入力してください。APIキーの取得方法については、それぞれのリンクを参照してください。
2. 要約したい論文（PDFファイル）を「Browse Files」をクリックしてアップロードするか、指定されたエリアにドラッグアンドドロップしてください。論文の内容が自動的に抽出され、テキスト形式で表示されます。
3. モデル、Temperature、最大トークン数を設定してください。アプリ内部には論文を要約するためのプロンプトが事前に入力されているので、特に変更する必要はありません。特定のリクエストがある場合のみ、プロンプトボックスに追加プロンプトを入力してください。
4. 「Submit」をクリックすると、要約が始まります。
5. 表示された結果の右上にあるコピーボタンをクリックすると、要約をコピーできます。応答が途中で途切れている場合は、最大トークン数を増やして再度Submitしてください。
6. ページの下部にあるドロップダウンリストから履歴を表示できますが、アプリウィンドウを閉じるとすべての履歴がクリアされることに注意してください。

## 論文サマライザープロンプト
論文サマライザーのプロンプトは[https://github.com/nhaouari/papersnap](https://github.com/nhaouari/papersnap)のプロンプトを参照しています。

## ローカルマシンへのインストール
このリポジトリをクローンし、必要なパッケージをインストールします：

```bash
git clone https://github.com/aisprint/paper_summarizer.git

cd paper_summarizer

pip install -r requirements.txt
```

## 使用法
Streamlitアプリケーションを実行します：

```bash
streamlit run main.py
```

