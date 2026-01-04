import socket


class URL:
    # コンストラクタ: URL文字列を受け取り、オブジェクトを初期化します
    def __init__(self, url):
        # スキームと残りのURLを分割します
        self.scheme, url = url.split("://", 1)
        # スキームが 'http' であることを確認します
        assert self.scheme == "http"
        if "/" not in url:
            url = url + "/"
        # ホストと残りのURL（パス）を分割します
        self.host, url = url.split("/", 1)
        # パスを '/' から始まるように設定します
        self.path = "/" + url

    def request(self):
        # TCP/IPソケットを作成します
        s = socket.socket(
            family=socket.AF_INET,  # IPv4アドレスファミリー
            type=socket.SOCK_STREAM,  # ストリームソケットタイプ (TCP)
            proto=socket.IPPROTO_TCP,  # TCPプロトコル
        )
        s.connect((self.host, 80))

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
