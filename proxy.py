import subprocess

# バッチコマンドを実行し、出力を取得
command = "netsh winhttp show proxy"
result = subprocess.run(command, capture_output=True, text=True, shell=True)

# 出力を変数に格納
output = result.stdout

# プロキシIPアドレスを抽出（簡易的な例）
proxy_ip = None
for line in output.splitlines():
    if "プロキシ サーバー" in line:
        proxy_ip = line.split(":")[-1].strip()
        break

# 結果を表示
print("プロキシ設定:")
print(output)
print(f"抽出されたプロキシIPアドレス: {proxy_ip}")
