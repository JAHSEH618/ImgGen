#!/usr/bin/env python3
"""
网易企业邮箱批量下载脚本 - 配置文件版本
支持使用JSON配置文件来管理账号和下载选项
"""

import imaplib
import email
from email.header import decode_header
import os
import sys
import json
from datetime import datetime


class NeteaseMailDownloader:
    def __init__(self, username, password, save_dir, imap_server="imap.qiye.163.com", imap_port=993):
        """
        初始化邮件下载器

        Args:
            username: 邮箱账号
            password: 邮箱密码或授权码
            save_dir: 保存目录
            imap_server: IMAP服务器地址
            imap_port: IMAP端口
        """
        self.username = username
        self.password = password
        self.save_dir = save_dir
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.mail = None

        # 创建保存目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def connect(self):
        """连接到IMAP服务器"""
        try:
            print(f"正在连接到 {self.imap_server}...")
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            print("连接成功！")
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def login(self):
        """登录邮箱"""
        try:
            print(f"正在登录账号 {self.username}...")
            self.mail.login(self.username, self.password)
            print("登录成功！")
            return True
        except Exception as e:
            print(f"登录失败: {e}")
            print("提示: 请检查账号密码是否正确，或尝试使用授权码")
            return False

    def get_folders(self):
        """获取所有邮箱文件夹"""
        try:
            status, folders = self.mail.list()
            if status == 'OK':
                folder_list = []
                for folder in folders:
                    # 解析文件夹名称
                    folder_str = folder.decode()
                    parts = folder_str.split('"')
                    if len(parts) >= 3:
                        folder_name = parts[-2]
                        folder_list.append(folder_name)
                return folder_list
            return []
        except Exception as e:
            print(f"获取文件夹列表失败: {e}")
            return []

    def decode_str(self, s):
        """解码邮件头部字符串"""
        if s is None:
            return ""

        value, charset = decode_header(s)[0]
        if charset:
            try:
                value = value.decode(charset)
            except:
                try:
                    value = value.decode('utf-8', errors='ignore')
                except:
                    value = str(value)
        elif isinstance(value, bytes):
            try:
                value = value.decode('utf-8', errors='ignore')
            except:
                value = str(value)

        return str(value)

    def clean_filename(self, filename):
        """清理文件名中的非法字符"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def download_emails(self, folder="INBOX", max_count=None, start_date=None):
        """
        下载指定文件夹的邮件

        Args:
            folder: 文件夹名称，默认为INBOX（收件箱）
            max_count: 最大下载数量，None表示全部下载
            start_date: 开始日期，格式为'DD-MMM-YYYY'，如'01-Jan-2024'
        """
        try:
            # 选择文件夹
            print(f"\n正在选择文件夹: {folder}")
            status, messages = self.mail.select(folder, readonly=True)
            if status != 'OK':
                print(f"无法选择文件夹 {folder}")
                return

            # 搜索邮件
            if start_date:
                # 根据日期搜索
                search_criteria = f'(SINCE "{start_date}")'
                status, data = self.mail.search(None, search_criteria)
            else:
                # 搜索所有邮件
                status, data = self.mail.search(None, 'ALL')

            if status != 'OK':
                print("搜索邮件失败")
                return

            # 获取邮件ID列表
            mail_ids = data[0].split()
            total_mails = len(mail_ids)

            if total_mails == 0:
                print("没有找到邮件")
                return

            print(f"找到 {total_mails} 封邮件")

            # 限制下载数量
            if max_count:
                mail_ids = mail_ids[-max_count:]  # 获取最新的N封邮件
                print(f"将下载最新的 {len(mail_ids)} 封邮件")

            # 创建文件夹目录
            folder_dir = os.path.join(self.save_dir, self.clean_filename(folder))
            if not os.path.exists(folder_dir):
                os.makedirs(folder_dir)

            # 下载每封邮件
            success_count = 0
            for i, mail_id in enumerate(mail_ids, 1):
                try:
                    print(f"\n[{i}/{len(mail_ids)}] 正在下载邮件 ID: {mail_id.decode()}...")

                    # 获取邮件
                    status, msg_data = self.mail.fetch(mail_id, '(RFC822)')
                    if status != 'OK':
                        print(f"获取邮件失败")
                        continue

                    # 解析邮件
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # 获取邮件信息
                    subject = self.decode_str(msg['Subject'])
                    from_addr = self.decode_str(msg['From'])
                    to_addr = self.decode_str(msg['To'])
                    date = self.decode_str(msg['Date'])

                    print(f"  主题: {subject}")
                    print(f"  发件人: {from_addr}")
                    print(f"  日期: {date}")

                    # 创建邮件保存目录
                    mail_dir_name = f"{mail_id.decode()}_{self.clean_filename(subject[:50])}"
                    mail_dir = os.path.join(folder_dir, mail_dir_name)
                    if not os.path.exists(mail_dir):
                        os.makedirs(mail_dir)

                    # 保存邮件元数据
                    metadata = {
                        'id': mail_id.decode(),
                        'subject': subject,
                        'from': from_addr,
                        'to': to_addr,
                        'date': date,
                        'folder': folder
                    }

                    with open(os.path.join(mail_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, ensure_ascii=False, indent=2)

                    # 保存原始邮件
                    with open(os.path.join(mail_dir, 'raw_email.eml'), 'wb') as f:
                        f.write(raw_email)

                    # 提取邮件内容和附件
                    self.extract_email_content(msg, mail_dir)

                    success_count += 1
                    print(f"  ✓ 下载成功")

                except Exception as e:
                    print(f"  ✗ 下载失败: {e}")
                    continue

            print(f"\n下载完成！成功: {success_count}/{len(mail_ids)}")
            print(f"保存位置: {folder_dir}")

        except Exception as e:
            print(f"下载邮件时出错: {e}")

    def extract_email_content(self, msg, save_dir):
        """提取邮件内容和附件"""
        body_text = ""
        body_html = ""
        attachment_count = 0

        # 创建附件目录
        attachments_dir = os.path.join(save_dir, 'attachments')

        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition', ''))

            try:
                # 获取邮件正文
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        try:
                            body_text += payload.decode(charset, errors='ignore')
                        except:
                            body_text += payload.decode('utf-8', errors='ignore')

                elif content_type == 'text/html' and 'attachment' not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        try:
                            body_html += payload.decode(charset, errors='ignore')
                        except:
                            body_html += payload.decode('utf-8', errors='ignore')

                # 保存附件
                elif content_disposition and 'attachment' in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = self.decode_str(filename)
                        filename = self.clean_filename(filename)

                        if not os.path.exists(attachments_dir):
                            os.makedirs(attachments_dir)

                        filepath = os.path.join(attachments_dir, filename)

                        # 处理重名文件
                        counter = 1
                        base_name, ext = os.path.splitext(filename)
                        while os.path.exists(filepath):
                            filename = f"{base_name}_{counter}{ext}"
                            filepath = os.path.join(attachments_dir, filename)
                            counter += 1

                        # 保存附件
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))

                        attachment_count += 1
                        print(f"  - 附件: {filename}")

            except Exception as e:
                print(f"  处理邮件部分时出错: {e}")
                continue

        # 保存纯文本内容
        if body_text:
            with open(os.path.join(save_dir, 'content.txt'), 'w', encoding='utf-8') as f:
                f.write(body_text)

        # 保存HTML内容
        if body_html:
            with open(os.path.join(save_dir, 'content.html'), 'w', encoding='utf-8') as f:
                f.write(body_html)

        if attachment_count > 0:
            print(f"  附件数量: {attachment_count}")

    def close(self):
        """关闭连接"""
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
                print("\n已断开连接")
            except:
                pass


def load_config(config_file):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"错误: 配置文件 {config_file} 不存在")
        print("请复制 mail_config.json.example 为 mail_config.json 并填写正确的配置")
        return None
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件格式错误: {e}")
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("网易企业邮箱批量下载工具 (配置文件版本)")
    print("=" * 60)

    # 读取配置文件
    config_file = "mail_config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    config = load_config(config_file)
    if not config:
        return

    # 获取配置
    email_account = config.get('email_account')
    email_password = config.get('email_password')
    save_dir = config.get('save_dir', './mail_downloads')
    imap_server = config.get('imap_server', 'imap.qiye.163.com')
    imap_port = config.get('imap_port', 993)
    download_options = config.get('download_options', {})

    # 验证必要的配置
    if not email_account or email_account == "your_email@company.com":
        print("错误: 请在配置文件中填写正确的邮箱账号")
        return

    if not email_password or email_password == "your_password_or_auth_code":
        print("错误: 请在配置文件中填写正确的邮箱密码或授权码")
        return

    # 创建下载器实例
    downloader = NeteaseMailDownloader(
        email_account,
        email_password,
        save_dir,
        imap_server,
        imap_port
    )

    # 连接和登录
    if not downloader.connect():
        return

    if not downloader.login():
        return

    try:
        # 获取文件夹列表
        print("\n正在获取邮箱文件夹列表...")
        folders = downloader.get_folders()
        if folders:
            print("\n可用的文件夹:")
            for idx, folder in enumerate(folders, 1):
                print(f"  {idx}. {folder}")

        # 从配置中获取下载选项
        folder = download_options.get('folder', 'INBOX')
        max_count = download_options.get('max_count')
        start_date = download_options.get('start_date')

        # 下载邮件
        downloader.download_emails(folder, max_count, start_date)

    finally:
        # 关闭连接
        downloader.close()


if __name__ == "__main__":
    main()