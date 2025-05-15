# HTTP Server

一个支持 Gzip 压缩的简单 HTTP 服务器，特别优化了 JavaScript 文件的传输。
用于前端项目的本地开发，可以方便的进行静态文件服务，并且自动对 JavaScript 文件进行 Gzip 压缩，测试发布环境。

## 功能特点

- 支持静态文件服务
- 自动对 JavaScript 文件进行 Gzip 压缩
- 自动查找可用端口
- 支持自定义服务目录
- 支持目录列表功能

## 系统要求

- Python 3.6 或更高版本

## 安装

由于本项目只使用 Python 标准库，无需安装额外的依赖。

```bash
git clone https://github.com/cxdmaye/http-server.git
cd http-server
```

## 使用方法

### 基本用法

```bash
python server.py
```

这将使用默认配置启动服务器：
- 端口：8200
- 服务目录：当前目录

### 高级用法

```bash
python server.py -p <端口号> -d <目录路径>
```

参数说明：
- `-p, --port`: 指定服务器端口号（默认：8200）
- `-d, --directory`: 指定服务目录路径（默认：当前目录）

### 示例

```bash
# 在端口 8080 上启动服务器，服务 /path/to/your/files 目录
python server.py -p 8080 -d /path/to/your/files
```

## 特性说明

1. **自动端口选择**：如果指定端口被占用，服务器会自动寻找下一个可用端口
2. **Gzip 压缩**：自动对 .js 文件进行 Gzip 压缩，提高传输效率
3. **目录浏览**：当访问目录时，如果没有 index.html，将显示目录内容
4. **错误处理**：提供友好的错误提示和异常处理

## 注意事项

- 服务器默认绑定到所有网络接口（0.0.0.0）
- 使用 Ctrl+C 可以优雅地停止服务器
- 确保服务目录具有适当的读取权限

## 许可证

MIT License 