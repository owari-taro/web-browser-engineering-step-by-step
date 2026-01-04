import socket
import ssl
import tkinter
import tkinter.font


WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18  # 水平・垂直ステップ
SCROLL_STEP = 100


class URL:
    # コンストラクタ: URL文字列を受け取り、オブジェクトを初期化します
    def __init__(self, url):
        # スキームと残りのURLを分割します
        self.scheme, url = url.split("://", 1)
        # スキームが 'http' または 'https' であることを確認します
        assert self.scheme in ["http", "https"]
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        if "/" not in url:
            url = url + "/"
        # ホストと残りのURL（パス）を分割します
        self.host, url = url.split("/", 1)
        # ホスト名にポートが含まれているか確認します
        if ":" in self.host:
            # ホスト名とポート番号を分割します
            self.host, port = self.host.split(":", 1)
            # ポート番号を整数に変換します
            self.port = int(port)
        # パスを '/' から始まるように設定します
        self.path = "/" + url

    def request(self):
        # TCP/IPソケットを作成します
        s = socket.socket(
            family=socket.AF_INET,  # IPv4アドレスファミリー
            type=socket.SOCK_STREAM,  # ストリームソケットタイプ (TCP)
            proto=socket.IPPROTO_TCP,  # TCPプロトコル
        )
        # 指定されたホストとポートに接続します
        s.connect((self.host, self.port))

        # HTTPSスキームの場合、SSL/TLSでソケットをラップします
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        # GETリクエスト文字列を作成します
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        # Hostヘッダーを追加します
        request += "Host: {}\r\n".format(self.host)
        # ヘッダーの終わりを示す空行を追加します
        request += "\r\n"
        # リクエストをUTF-8でエンコードして送信します
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")

        # レスポンスの最初の行（ステータスライン）を読み取ります
        statusline = response.readline()
        # ステータスラインをバージョン、ステータスコード、説明に分割します
        version, status, explanation = statusline.split(" ", 2)

        # レスポンスヘッダーを格納するディクショナリを初期化します
        response_headers = {}
        # ヘッダーを読み取るループ
        while True:
            line = response.readline()
            # 空行はヘッダーの終わりを示します
            if line == "\r\n":
                break
            # ヘッダー名と値をコロンで分割します
            header, value = line.split(":", 1)
            # ヘッダー名を小文字に正規化し、値の前後の空白を削除してディクショナリに追加します
            response_headers[header.casefold()] = value.strip()
        # Transfer-Encodingヘッダーがないことを確認します
        assert "transfer-encoding" not in response_headers
        # Content-Encodingヘッダーがないことを確認します
        assert "content-encoding" not in response_headers

        content = response.read()
        # ソケットを閉じます
        s.close()
        # ... (ボディ読み取り、ソケットクローズ)
        # レスポンスのボディを返します
        return content


def lex(body):
    # HTML本文からテキストを抽出する関数
    text = ""
    in_tag = False  # タグ内にいるかどうかのフラグ
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            # タグ外の文字をテキストに追加
            text += c
    return text


# テキストのレイアウトを行い、ディスプレイリスト(display_list)を返す関数
def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    font = tkinter.font.Font()  # デフォルトフォントを使用
    for word in text.split():  # テキストを単語に分割してループ
        w = font.measure(word)  # 単語の幅を測定
        if cursor_x + w > WIDTH - HSTEP:  # 単語が右端を超える場合は改行
            cursor_y += font.metrics("linespace") * 1.25
            cursor_x = HSTEP  # x座標をリセット
        # ディスプレイリストdisplay listに単語とその座標を追加
        display_list.append((cursor_x, cursor_y, word))
        # カーソルを単語の幅とスペース分だけ進める
        cursor_x += w + font.measure(" ")
    return display_list


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        # スクロール位置を初期化
        self.scroll = 0
        # 下矢印キーにscrolldownメソッドをバインド
        self.window.bind("<Down>", self.scrolldown)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()  # 再描画

    # URLからWebページを読み込み、表示する関数
    def load(self, url):
        body = url.request()
        text = lex(body)
        self.display_list = layout(text)
        # ディスプレイリストdisplay listを描画
        self.draw()

    # ディスプレイリスト display listに基づいてキャンバスに描画するメソッド
    def draw(self):
        # 描画前にキャンバスをクリア
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            # 画面下部より下の文字はスキップ
            if y > self.scroll + HEIGHT:
                continue
            # 画面上部より上の文字はスキップ
            if y + VSTEP < self.scroll:
                continue
            # スクロール位置を考慮して文字を描画
            self.canvas.create_text(x, y - self.scroll, text=c)


if __name__ == "__main__":
    import sys

    # コマンドライン引数からURLを取得して読み込みます
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
