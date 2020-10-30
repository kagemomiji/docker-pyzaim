# pyzaim [![Build Status](https://travis-ci.org/kagemomiji/pyzaim.svg?branch=master)](https://travis-ci.org/kagemomiji/pyzaim)

[Zaim](https://zaim.net/)のデータを取得・操作するPythonパッケージ

## 概要

大きくわけて2つの処理を行うパッケージです。

- [Zaim API](https://dev.zaim.net/)のラッパークラス
  - Zaim APIのアクセストークンの発行
  - Rest APIとして提供されている処理の実行
- [Selenium](https://github.com/SeleniumHQ/selenium/tree/master/py)を用いたデータ取得
  - Zaimにはクレジットカードや銀行口座から自動でデータ取得する機能があるが、APIではそれらのデータにはアクセスできない
  - これらの情報を取得するため、Seleniumのwebdriver(Chrome)を用いてデータを取得

## インストール

```bash
pip install pyzaim
```

## 準備

- Zaimアカウントの作成
- Zaim Developersでのアプリケーションの登録 (コンシューマID、コンシューマシークレットの発行)
- Google Chromeおよびseleniumの導入

## 使い方

### Zaim APIのラッパークラスの使い方

#### アクセストークンの発行

予め環境変数を定義する

USER_IDとUSER_PASSWORDはWEB UIで使用するユーザ名とパスワード
CONSUMER_IDとCONSUMER_SECRETはDEVELOPERS SITEで入手する

```bash
export USER_ID=<user id>
export USER_PASSWORD=<user password>
export CONSUMER_ID=<consumer id>
export CONSUMER_SECRET=<consumer secret>
```

```python
from pyzaim import OauthInitializer

oinit = OauthInitializer()
oinit.authentication()

# 自動で認証が終了し，Oauth Verifier, Acess token, Acess Secretが表示される
# chromedriverはパスが通っている場所に置くこと
```

取得したOauthVerifier, Access token, Access Secretは以下のように環境変数に定義する

```bash
export OAUTH_VERIFIER=<oauth verifier>
export ACCESS_TOKEN=<access token>
export ACCESS_TOKEN_SECRET=<access secret>
```

#### APIを利用してデータを取得・操作

```python
from pyzaim import ZaimAPI

# 環境変数から各パラメータを読み出すので定義不要
api = ZaimAPI()

# 動作確認 (ユーザーID等のデータが取得されて、表示されればOK)
print(api.verify())

# データの取得
data = api.get_data()

# 支払いデータの登録
api.insert_payment_simple('日付(datetime.date型)', '金額(int)', 'ジャンル名',
                          '口座名', 'コメント', '品名', '店舗名') # 後半4つは任意入力

# 使用できるジャンル名は以下で確認できる
print(api.genre_itos)

# 使用できる口座名は以下で確認できる
print(api.account_itos)

# 支払いデータの更新 (更新対象データのIDはapi.get_data()で確認)
api.update_payment_simple('更新対象データのID', '日付(datetime.date型)', '金額(int)',
                          'ジャンル名', '口座名', 'コメント', '品名', '店舗名') # 後半4つは任意入力

# 支払いデータの削除
api.delete_payment('削除対象のデータのID')
```

### seleniumを用いたデータ取得

```python
from pyzaim import ZaimCrawler

# Chrome Driverの起動とZaimへのログイン、ログインには少し時間がかかります
crawler = ZaimCrawler() # headlessをTrueにするとヘッドレスブラウザで実行できる

# データの取得 (データの取得には少し時間がかかります、時間はデータ件数による)
## default では10件読み込み
data = crawler.get_data('取得する年(int)', '取得する月(int)', progress=True) # progressをFalseにするとプログレスバーを非表示にできる

## 最大n件読み込む場合は以下のようにprogressの前にrecord数を定義する
data = crawler.get_data('取得する年(int)', '取得する月(int)',20, progress=True) # max 20件
data = crawler.get_data('取得する年(int)', '取得する月(int)',40, progress=True) # max 40件

# 終了処理
crawler.close()
```

## Acknowledgement

This Software includes customized [reeve0930/pyzaim](https://github.com/reeve0930/pyzaim)  

