import http.server
import socketserver
import gzip
import os
import argparse
import posixpath
import socket
from urllib.parse import unquote


class GzipHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, root_dir=None, **kwargs):
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def end_headers(self):
        # 检查文件类型是否为 JS
        if self.path.endswith(".js"):
            self.send_header("Content-Encoding", "gzip")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def send_file(self, path):
        with open(path, "rb") as file:
            content = file.read()
            # 如果是 JS 文件，进行 Gzip 压缩
            if path.endswith(".js"):
                content = gzip.compress(content)
            self.send_response(200)
            self.send_header("Content-type", self.guess_type(path))
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    def translate_path(self, path):
        """重写路径转换方法，使用指定的目录作为根目录"""
        path = path.split("?", 1)[0]
        path = path.split("#", 1)[0]
        path = posixpath.normpath(unquote(path))
        words = path.split("/")
        words = filter(None, words)
        path = str(self.root_dir)
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # 忽略绝对路径和相对路径
                continue
            path = os.path.join(path, word)
        return path

    def do_GET(self):
        try:
            path = self.translate_path(self.path)
            if path is not None and os.path.isfile(path):
                self.send_file(path)
            elif path is not None and os.path.isdir(path):
                # 如果是目录，尝试查找 index.html
                index_path = os.path.join(path, "index.html")
                if os.path.isfile(index_path):
                    self.send_file(index_path)
                else:
                    # 如果没有 index.html，列出目录内容
                    self.list_directory(path)
            else:
                self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, str(e))


def find_available_port(start_port, max_attempts=100):
    """寻找从start_port开始的第一个可用端口"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None


def run_server(port, directory):
    # 确保目录存在
    if not os.path.exists(directory):
        print(f"错误：目录 '{directory}' 不存在")
        return

    # 获取绝对路径
    directory = os.path.abspath(directory)

    # 创建服务器，允许端口重用
    socketserver.TCPServer.allow_reuse_address = True
    handler = lambda *args, **kwargs: GzipHTTPRequestHandler(
        *args, root_dir=directory, **kwargs
    )

    # 寻找可用端口
    available_port = find_available_port(port)
    if available_port is None:
        print(f"错误：无法找到可用端口，已尝试 {port} 到 {port + 99}")
        return
    
    if available_port != port:
        print(f"注意：端口 {port} 已被占用，使用端口 {available_port} 代替")

    try:
        with socketserver.TCPServer(("", available_port), handler) as httpd:
            print(f"在端口 {available_port} 启动服务")
            print(f"服务目录: {directory}")
            print(f"服务地址: http://localhost:{available_port}")
            print("按 Ctrl+C 停止服务器")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"错误：{str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="启动一个支持 Gzip 压缩的 HTTP 服务器")
    parser.add_argument(
        "-p", "--port", type=int, default=8200, help="服务器端口号 (默认: 8200)"
    )
    parser.add_argument(
        "-d", "--directory", type=str, default=".", help="服务目录路径 (默认: 当前目录)"
    )

    args = parser.parse_args()
    run_server(args.port, args.directory)
