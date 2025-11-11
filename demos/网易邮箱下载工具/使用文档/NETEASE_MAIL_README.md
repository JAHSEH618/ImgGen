# 网易企业邮箱批量下载工具

这是一个用于批量下载网易企业邮箱的Python脚本，支持下载邮件内容和附件到本地指定目录。

## 功能特点

- ✅ 支持通过IMAP协议连接网易企业邮箱
- ✅ **批量下载邮箱所有邮件**（支持下载全部邮件）
- ✅ 自动保存邮件正文（纯文本和HTML格式）
- ✅ 自动下载并保存附件
- ✅ 保存邮件元数据（主题、发件人、收件人、日期等）
- ✅ **断点续传**（自动跳过已下载的邮件，支持中断后继续）
- ✅ **进度显示和ETA时间估算**（实时显示下载进度和剩余时间）
- ✅ **批量下载多个文件夹**（一次性下载收件箱、已发送等多个文件夹）
- ✅ 支持按日期筛选邮件
- ✅ 支持限制下载数量
- ✅ 下载前智能确认（超过100封自动提示）
- ✅ 详细的统计信息（成功、失败、跳过、用时、速度等）

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
    "folders": ["INBOX"],
    "max_count": null,
    "start_date": null,
    "skip_existing": true,
    "auto_confirm": false
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

- `folders`: 要下载的文件夹列表（支持多个文件夹）
  - `["INBOX"]` - 只下载收件箱
  - `["INBOX", "Sent"]` - 下载收件箱和已发送
  - `["INBOX", "Sent", "Drafts"]` - 下载多个文件夹
  - 常见文件夹名称：
    - `"INBOX"` - 收件箱
    - `"Sent"` - 已发送
    - `"Drafts"` - 草稿箱
    - `"Trash"` - 垃圾箱
    - `"Junk"` - 垃圾邮件
  - 或其他自定义文件夹名称

- `max_count`: 最大下载数量
  - 设置为数字（如 `10`）表示下载最新的N封邮件
  - 设置为 `null` 表示**下载全部邮件**（推荐）

- `start_date`: 开始日期筛选
  - 格式: `"DD-MMM-YYYY"`，例如 `"01-Jan-2024"`
  - 设置为 `null` 表示不按日期筛选

- `skip_existing`: 断点续传（推荐开启）
  - 设置为 `true` 表示自动跳过已下载的邮件
  - 设置为 `false` 表示重新下载所有邮件
  - **推荐设置为 `true`，这样中断后可以继续下载**

- `auto_confirm`: 自动确认下载
  - 设置为 `true` 表示不询问直接下载
  - 设置为 `false` 表示当邮件数量超过100封时会询问确认
  - **首次使用建议设置为 `false`**

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

### 配置文件示例

#### 示例1: 同时下载已发送和收件箱的所有邮件（推荐配置）

```json
{
  "email_account": "your_email@company.com",
  "email_password": "your_auth_code",
  "save_dir": "./mail_downloads",
  "imap_server": "imap.qiye.163.com",
  "imap_port": 993,
  "download_options": {
    "folders": ["Sent", "INBOX"],
    "max_count": null,
    "start_date": null,
    "skip_existing": true,
    "auto_confirm": false
  }
}
```

**注意**:
- 下载顺序：先下载已发送邮件，再下载收件箱
- 不同邮件服务器的"已发送"文件夹名称可能不同：
  - 网易企业邮箱通常使用: `"Sent"` 或 `"已发送邮件"`
- 建议先运行一次脚本，查看显示的文件夹列表，然后使用准确的文件夹名称

#### 示例2: 下载多个文件夹的所有邮件

```json
{
  "download_options": {
    "folders": ["Sent", "INBOX", "Drafts"],
    "max_count": null,
    "start_date": null,
    "skip_existing": true,
    "auto_confirm": true
  }
}
```

**说明**: 按照数组顺序依次下载：已发送 → 收件箱 → 草稿箱

#### 示例3: 下载收件箱最新的100封邮件

```json
{
  "download_options": {
    "folders": ["INBOX"],
    "max_count": 100,
    "start_date": null,
    "skip_existing": true,
    "auto_confirm": false
  }
}
```

#### 示例4: 下载2024年以来的所有邮件

```json
{
  "download_options": {
    "folders": ["INBOX"],
    "max_count": null,
    "start_date": "01-Jan-2024",
    "skip_existing": true,
    "auto_confirm": false
  }
}
```

#### 示例5: 完整备份所有文件夹（自动确认，适合无人值守）

```json
{
  "download_options": {
    "folders": ["Sent", "INBOX", "Drafts", "Trash", "Junk"],
    "max_count": null,
    "start_date": null,
    "skip_existing": true,
    "auto_confirm": true
  }
}
```

**说明**: 优先备份已发送邮件，依次下载各个文件夹

### 代码示例（直接调用）

#### 示例1: 下载收件箱的所有邮件

```python
downloader.download_emails("INBOX", max_count=None, skip_existing=True)
```

#### 示例2: 下载收件箱最新的10封邮件

```python
downloader.download_emails("INBOX", max_count=10)
```

#### 示例3: 下载2024年1月1日之后的邮件

```python
downloader.download_emails("INBOX", start_date="01-Jan-2024")
```

#### 示例4: 下载已发送文件夹的所有邮件（断点续传）

```python
downloader.download_emails("Sent", max_count=None, skip_existing=True)
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

### 5. 如何下载邮箱里的所有邮件？

在配置文件中设置：
```json
"download_options": {
  "folders": ["INBOX"],
  "max_count": null,  // 设置为 null 表示下载全部
  "skip_existing": true,  // 开启断点续传
  "auto_confirm": true  // 自动确认，不询问
}
```

### 6. 下载中断了怎么办？

不用担心！脚本支持**断点续传**功能：
- 确保 `skip_existing` 设置为 `true`
- 再次运行脚本，它会自动跳过已下载的邮件
- 从中断的地方继续下载

### 7. 如何下载多个文件夹？

在配置文件中设置 `folders` 为数组：
```json
"folders": ["INBOX", "Sent", "Drafts"]
```

### 8. 下载速度慢怎么办？

- 检查网络连接质量
- IMAP协议本身有速度限制
- 大附件会导致下载变慢
- 平均速度通常在 0.5-2 封/秒

### 9. 如何查看下载进度？

脚本会实时显示：
- 当前进度百分比
- 已下载/总数量
- 预计剩余时间（ETA）
- 下载速度统计

## 注意事项

1. **首次使用**：建议先设置 `max_count: 10` 测试，确认正常后再设置为 `null` 下载全部
2. **断点续传**：建议始终开启 `skip_existing: true`，这样下载中断后可以继续
3. **下载时间**：下载大量邮件需要较长时间，建议使用 `auto_confirm: true` 避免等待确认
4. **安全性**：请妥善保管配置文件，避免泄露邮箱密码，建议使用授权码
5. **定期备份**：建议定期备份下载的邮件数据
6. **只读模式**：脚本使用只读模式访问邮箱，不会删除或修改服务器上的邮件
7. **网络稳定**：下载大量邮件时建议保持网络稳定，如中断可通过断点续传继续
8. **磁盘空间**：确保有足够的磁盘空间存储邮件和附件

## 技术支持

如遇到问题，请检查：
1. Python版本是否为3.6或更高
2. 网易企业邮箱IMAP服务是否正常
3. 配置文件格式是否正确

## 许可证

MIT License