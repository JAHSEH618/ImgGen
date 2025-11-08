# 网易企业邮箱批量下载工具

这是一个用于批量下载网易企业邮箱的Python脚本，支持下载邮件内容和附件到本地指定目录。

## 功能特点

- 支持通过IMAP协议连接网易企业邮箱
- 批量下载邮件到本地目录
- 自动保存邮件正文（纯文本和HTML格式）
- 自动下载并保存附件
- 保存邮件元数据（主题、发件人、收件人、日期等）
- 支持按日期筛选邮件
- 支持限制下载数量
- 支持下载指定文件夹的邮件

## 安装依赖

脚本使用Python标准库，无需安装额外依赖。

## 使用方法

### 方法1: 直接使用脚本（推荐新手）

1. 打开 `download_netease_mail.py` 文件
2. 修改以下配置信息：

```python
EMAIL_ACCOUNT = "your_email@company.com"  # 你的邮箱账号
EMAIL_PASSWORD = "your_password"  # 你的邮箱密码或授权码
SAVE_DIR = "./mail_downloads"  # 保存目录
```

3. 运行脚本：

```bash
python3 download_netease_mail.py
```

或者通过命令行参数传入：

```bash
python3 download_netease_mail.py your_email@company.com your_password ./mail_downloads
```

### 方法2: 使用配置文件（推荐）

1. 复制配置文件示例：

```bash
cp mail_config.json.example mail_config.json
```

2. 编辑 `mail_config.json` 文件，填写你的邮箱信息：

```json
{
  "email_account": "your_email@company.com",
  "email_password": "your_password_or_auth_code",
  "save_dir": "./mail_downloads",
  "imap_server": "imap.qiye.163.com",
  "imap_port": 993,
  "download_options": {
    "folder": "INBOX",
    "max_count": 10,
    "start_date": null
  }
}
```

3. 运行脚本：

```bash
python3 download_netease_mail_config.py
```

或者指定配置文件：

```bash
python3 download_netease_mail_config.py my_config.json
```

## 配置说明

### 基本配置

- `email_account`: 你的网易企业邮箱账号
- `email_password`: 邮箱密码或授权码（建议使用授权码）
- `save_dir`: 邮件保存的本地目录
- `imap_server`: IMAP服务器地址（默认: imap.qiye.163.com）
- `imap_port`: IMAP端口（默认: 993）

### 下载选项

- `folder`: 要下载的文件夹名称
  - `"INBOX"` - 收件箱
  - `"Sent"` - 已发送
  - `"Drafts"` - 草稿箱
  - `"Trash"` - 垃圾箱
  - 或其他自定义文件夹名称

- `max_count`: 最大下载数量
  - 设置为数字（如 `10`）表示下载最新的N封邮件
  - 设置为 `null` 表示下载全部邮件

- `start_date`: 开始日期筛选
  - 格式: `"DD-MMM-YYYY"`，例如 `"01-Jan-2024"`
  - 设置为 `null` 表示不按日期筛选

## 下载的文件结构

```
mail_downloads/
└── INBOX/                          # 文件夹名称
    ├── 1_邮件主题1/                 # 邮件ID_主题
    │   ├── metadata.json           # 邮件元数据
    │   ├── raw_email.eml           # 原始邮件文件
    │   ├── content.txt             # 纯文本内容
    │   ├── content.html            # HTML内容
    │   └── attachments/            # 附件目录
    │       ├── 附件1.pdf
    │       └── 附件2.docx
    └── 2_邮件主题2/
        └── ...
```

## 获取授权码

为了安全起见，建议使用授权码而不是直接使用邮箱密码：

1. 登录网易企业邮箱网页版
2. 进入"设置" -> "安全" -> "客户端授权密码"
3. 生成新的授权码
4. 在脚本中使用授权码替代密码

## 使用示例

### 示例1: 下载收件箱的所有邮件

```python
downloader.download_emails("INBOX")
```

### 示例2: 下载收件箱最新的10封邮件

```python
downloader.download_emails("INBOX", max_count=10)
```

### 示例3: 下载2024年1月1日之后的邮件

```python
downloader.download_emails("INBOX", start_date="01-Jan-2024")
```

### 示例4: 下载已发送文件夹的最新5封邮件

```python
downloader.download_emails("Sent", max_count=5)
```

## 常见问题

### 1. 登录失败

- 检查邮箱账号和密码是否正确
- 尝试使用授权码而不是密码
- 确认企业邮箱已开启IMAP服务

### 2. 连接失败

- 检查网络连接
- 确认IMAP服务器地址和端口是否正确
- 检查防火墙设置

### 3. 中文乱码

脚本已处理常见的编码问题，如果仍有乱码，请检查邮件原始编码格式。

### 4. 附件下载失败

某些附件可能因为编码或格式问题导致下载失败，脚本会跳过这些附件并继续下载其他内容。

## 注意事项

1. 首次运行建议先设置 `max_count` 为较小的数值（如10），测试成功后再批量下载
2. 下载大量邮件可能需要较长时间，请耐心等待
3. 请妥善保管配置文件，避免泄露邮箱密码
4. 建议定期备份下载的邮件数据
5. 脚本使用只读模式访问邮箱，不会删除或修改服务器上的邮件

## 技术支持

如遇到问题，请检查：
1. Python版本是否为3.6或更高
2. 网易企业邮箱IMAP服务是否正常
3. 配置文件格式是否正确

## 许可证

MIT License