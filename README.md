# Webブラウザエンジニアリング―Chrome開発者たちから学ぶ、作って理解するブラウザとWebの仕組み

<div align="center">
    <img height=400 alt="Webブラウザエンジニアリング" src="./docs/web-browser-engineering.webp" />
    <br>
    『Webブラウザエンジニアリング―Chrome開発者たちから学ぶ、作って理解するブラウザとWebの仕組み』
    <br>
    Pavel Panchekha （パベル パンチェカ）、Chris Harrelson （クリス ハレルソン） 著
    <br>
    小河 亮 （オガワ リョウ） 訳
</div>

## このリポジトリについて

このリポジトリは、『Webブラウザエンジニアリング―Chrome開発者たちから学ぶ、作って理解するブラウザとWebの仕組み』のサンプルコードを収録しています。

各節ごとにコミットしているため、特定の章のコードを確認したい場合は、[コミット履歴](https://github.com/negibokken/web-browser-engineering-step-by-step/commits/main/)から該当するコミットを参照してください。
本文のコード例の他に修正の必要がある部分もあるため、途中で挫折しないためにもコミットを参照しながら進めることをお勧めします。

> [!WARNING]
> なお、本リポジトリのコードも完全に原著と同じではない場合があります。あくまで参考としてご利用ください。

## 環境構築について

このリポジトリでは実行に必要な環境をDockerで構築して動かせるようにしています。環境構築に不安がある場合には、このリポジトリをフォーク、クローンしてから`template`ブランチをベースにして進めてみてください。
なお、訳者のmacOSとLinuxで動作確認を行っていますが、もしかしたら読者の方の環境では動かないかもしれません。その際はエラーを修正しながら進めていただけると幸いです。

12章まではGPUが必要ないので、Dockerコンテナで動かすことでホストへのライブラリのインストールなどを省略できます。
しかし、**13章以降はGPUが必要になるため、そのままではDockerで動かすことができません**。特にmacOSのDocker DesktopはGPUパススルーをサポートしていないため、13章以降はローカル環境に直接ライブラリをインストールして動かすなどの対応が必要になります。

Pythonのライブラリは互換性をチェックしているバージョンをインストールして`pyproject.toml`と`uv.lock`に記載しています。最新版のパッケージの場合は作業が必要になる可能性があるので、自分で環境を構築する際にも、これらのファイルをコピーして使うことでパッケージのバージョンを揃えることをお勧めします。

## 注意事項

> [!WARNING]
> 各節の変更点を各コミットに対応させているために、修正が入ったらこのリポジトリのコミットハッシュは変わる可能性があります。

## 事前準備

- Python 3.9 (Dockerを使う場合は13章まで不要)
    - 原著で使っている skia-python 87.7 との相性のため
- [uv](https://docs.astral.sh/uv/) (Dockerを使う場合は13章まで不要)
- Docker（Dockerを使う場合のみ）
- Make
- XQuarts (macOSユーザー向け)

### macOSユーザー向けの事前準備

XQuartzをインストールして、下記のように設定してX11フォワーディングを有効にします。
- Settings > Security > "Allow connections from network clients"にチェック

## Dockerを使って動かす場合

### ビルド

最初にDockerイメージをビルドする必要があります。以下のコマンドを実行してください。

```shell
make docker_build
```

### 実行する

実行するには、`browser/main.py`にブラウザを実装つつ、以下のコマンドを実行します。`<your_url_here>`を実際のURLに置き換えてください。

```shell
make docker_run URL=<your_url_here>
```


### サーバーを実行する

8章以降からはサーバーを実装します。サーバーは`server/server.py`を作成し、下記のコマンドを実行すれば起動できます（`server/server.py`のコードは本文やこのリポジトリを参考に実装してください）。
テキストどおりに実装れば、`http://localhost:8000`でサーバーにアクセスできるようになります。macOSの場合、Dockerコンテナ内ブラウザがサーバーにアクセスするには`http://host.docker.internal:8000`を使う点に注意してください。
Linuxの場合は`http://localhost:8000`で問題ありません。

```shell
make docker_run_server
```

## Dockerを使わずに動かす場合

uvを使ってプロジェクトをセットアップするには、以下のコマンドを実行してください。

```shell
uv sync
```

プロジェクトを実行するには、以下のコマンドを使用します。`https://example.com`を実際のURLに置き換えてください。ホスト環境で動いているので、サーバーへのアクセスは`http://localhost:8000`で行えます。

```shell
cd browser
uv run main.py https://example.com
```


## 動作イメージ

| Dockerを使って動かしたとき | Dockerを使っていないとき |
|:-:|:-:|
| ![Dockerを使って動かしたときのブラウザのスクリーンショット](./docs/example_with_docker.gif) | ![Dockerを使っていないときのブラウザのスクリーンショット](./docs/example_without_docker.gif) |
