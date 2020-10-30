# pyzaim [![Build Status](https://travis-ci.org/kagemomiji/docker-pyzaim.svg?branch=main)](https://travis-ci.org/kagemomiji/docker-pyzaim)

This is docker image for operating personal data in [Zaim](https://zaim.net/)

## Acknowledgement

This Software includes customized [reeve0930/pyzaim](https://github.com/reeve0930/pyzaim)  

## 準備

- Zaimアカウントの作成
- Zaim Developersでのアプリケーションの登録 (コンシューマID、コンシューマシークレットの発行)
- docker環境を構築

## インストール

```bash
docker build -t docker-zaim .
```

## Usage

### Get Access Token/Access Token Secret/ OAUTH VERIFIER

```bash
docker run --rm \
  -e USER_ID=<user email address> \ 
  -e USER_PASSWORD=<user password> \
  -e CONSUMER_ID=<consumer_id> \
  -e CONSUMER_SECRET=<consumer_secret> \
  docker-zaim --oauth
```

after some seconds , it will print ACCESS_TOKEN/ACCESS_TOKEN_SECRET/OAUTH_VERIFIER


### Get Data with API Access

```bash
docker run --rm \
  -e CONSUMER_ID=<consumer_id> \
  -e CONSUMER_SECRET=<consumer_secret> \
  -e OAUTH_VERIFIER=<oauth verifier> \
  -e ACCESS_TOKEN=<access token> \
  -e ACCESS_TOKEN_SECRET=<access token secret>
  docker-zaim --api
```

### Get Data with Crawler Access

```bash
docker run --rm \
  -e USER_ID=<user email address> \ 
  -e USER_PASSWORD=<user password> \
  docker-zaim --crawler
```
