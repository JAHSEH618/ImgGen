#!/usr/bin/env python3
"""
网易企业邮箱下载工具 - 简易版
专为非技术人员设计，通过交互式问答完成配置和下载
"""

import imaplib
import email
from email.header import decode_header
import os
import sys
import json
import time
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
            print("✓ 连接成功！")
            return True
        except Exception as e:
            print(f"✗ 连接失败: {e}")
            return False

    def login(self):
        """登录邮箱"""
        try:
            print(f"正在登录账号 {self.username}...")
            self.mail.login(self.username, self.password)
            print("✓ 登录成功！")
            return True
        except Exception as e:
            print(f"✗ 登录失败: {e}")
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

    def get_downloaded_mail_ids(self, folder_dir):
        """获取已下载的邮件ID列表"""
        downloaded_ids = set()
        if os.path.exists(folder_dir):
            for item in os.listdir(folder_dir):
                if os.path.isdir(os.path.join(folder_dir, item)):
                    # 从目录名提取邮件ID（格式：ID_主题）
                    mail_id = item.split('_')[0]
                    downloaded_ids.add(mail_id)
        return downloaded_ids

    def download_emails(self, folder="INBOX", max_count=None, start_date=None, skip_existing=True, auto_confirm=False):
        """
        下载指定文件夹的邮件

        Args:
            folder: 文件夹名称，默认为INBOX（收件箱）
            max_count: 最大下载数量，None表示全部下载
            start_date: 开始日期，格式为'DD-MMM-YYYY'，如'01-Jan-2024'
            skip_existing: 是否跳过已下载的邮件（断点续传）
            auto_confirm: 是否自动确认下载（不询问用户）
        """
        try:
            # 选择文件夹
            print(f"\n{'='*60}")
            print(f"正在处理文件夹: {folder}")
            print(f"{'='*60}")

            status, messages = self.mail.select(folder, readonly=True)
            if status != 'OK':
                print(f"✗ 无法选择文件夹 {folder}")
                return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}

            # 搜索邮件
            if start_date:
                # 根据日期搜索
                search_criteria = f'(SINCE "{start_date}")'
                status, data = self.mail.search(None, search_criteria)
            else:
                # 搜索所有邮件
                status, data = self.mail.search(None, 'ALL')

            if status != 'OK':
                print("✗ 搜索邮件失败")
                return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}

            # 获取邮件ID列表
            mail_ids = data[0].split()
            total_mails = len(mail_ids)

            if total_mails == 0:
                print("没有找到邮件")
                return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}

            print(f"✓ 找到 {total_mails} 封邮件")

            # 创建文件夹目录
            folder_dir = os.path.join(self.save_dir, self.clean_filename(folder))
            if not os.path.exists(folder_dir):
                os.makedirs(folder_dir)

            # 检查已下载的邮件（断点续传）
            downloaded_ids = self.get_downloaded_mail_ids(folder_dir) if skip_existing else set()
            if downloaded_ids:
                print(f"✓ 已下载 {len(downloaded_ids)} 封邮件（将跳过）")

            # 过滤已下载的邮件
            mail_ids_to_download = [mid for mid in mail_ids if mid.decode() not in downloaded_ids]

            if not mail_ids_to_download:
                print("✓ 所有邮件都已下载完成！")
                return {'success': 0, 'failed': 0, 'skipped': len(downloaded_ids), 'total': total_mails}

            # 限制下载数量
            original_count = len(mail_ids_to_download)
            if max_count and max_count < len(mail_ids_to_download):
                mail_ids_to_download = mail_ids_to_download[-max_count:]  # 获取最新的N封邮件
                print(f"⚠ 限制下载数量: {len(mail_ids_to_download)} 封（总共 {original_count} 封待下载）")

            # 下载前确认
            if not auto_confirm and len(mail_ids_to_download) > 100:
                print(f"\n⚠ 警告: 准备下载 {len(mail_ids_to_download)} 封邮件，这可能需要较长时间。")
                confirm = input("是否继续？(y/N): ").strip().lower()
                if confirm != 'y':
                    print("已取消下载")
                    return {'success': 0, 'failed': 0, 'skipped': 0, 'total': total_mails}

            # 开始下载
            print(f"\n开始下载 {len(mail_ids_to_download)} 封邮件...")
            print("-" * 60)

            success_count = 0
            failed_count = 0
            start_time = time.time()

            for i, mail_id in enumerate(mail_ids_to_download, 1):
                try:
                    # 计算进度和ETA
                    progress = (i / len(mail_ids_to_download)) * 100
                    elapsed = time.time() - start_time
                    if i > 1:
                        avg_time = elapsed / (i - 1)
                        eta_seconds = avg_time * (len(mail_ids_to_download) - i)
                        eta_str = f"ETA: {int(eta_seconds//60)}分{int(eta_seconds%60)}秒"
                    else:
                        eta_str = "ETA: 计算中..."

                    print(f"\n[{i}/{len(mail_ids_to_download)}] ({progress:.1f}%) {eta_str}")
                    print(f"邮件ID: {mail_id.decode()}")

                    # 获取邮件
                    status, msg_data = self.mail.fetch(mail_id, '(RFC822)')
                    if status != 'OK':
                        print(f"  ✗ 获取邮件失败")
                        failed_count += 1
                        continue

                    # 解析邮件
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # 获取邮件信息
                    subject = self.decode_str(msg['Subject'])
                    from_addr = self.decode_str(msg['From'])
                    to_addr = self.decode_str(msg['To'])
                    date = self.decode_str(msg['Date'])

                    print(f"  主题: {subject[:60]}{'...' if len(subject) > 60 else ''}")
                    print(f"  发件人: {from_addr[:50]}{'...' if len(from_addr) > 50 else ''}")
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
                        'folder': folder,
                        'download_time': datetime.now().isoformat()
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
                    failed_count += 1
                    continue

            # 统计信息
            elapsed_total = time.time() - start_time
            print(f"\n{'='*60}")
            print(f"下载完成！")
            print(f"  成功: {success_count} 封")
            print(f"  失败: {failed_count} 封")
            print(f"  跳过: {len(downloaded_ids)} 封（已下载）")
            print(f"  总计: {total_mails} 封")
            print(f"  用时: {int(elapsed_total//60)}分{int(elapsed_total%60)}秒")
            print(f"  平均速度: {success_count/elapsed_total:.2f} 封/秒" if elapsed_total > 0 else "")
            print(f"  保存位置: {folder_dir}")
            print(f"{'='*60}")

            return {
                'success': success_count,
                'failed': failed_count,
                'skipped': len(downloaded_ids),
                'total': total_mails
            }

        except Exception as e:
            print(f"✗ 下载邮件时出错: {e}")
            return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}

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


def print_header():
    """打印程序头部"""
    print("\n" + "=" * 70)
    print(" " * 20 + "网易企业邮箱下载工具")
    print(" " * 25 + "简易版 v1.0")
    print("=" * 70)


def get_user_input(prompt, default=None, password=False):
    """获取用户输入"""
    if default:
        prompt_text = f"{prompt} [默认: {default}]: "
    else:
        prompt_text = f"{prompt}: "

    if password:
        import getpass
        value = getpass.getpass(prompt_text)
    else:
        value = input(prompt_text).strip()

    return value if value else default


def yes_no_question(prompt, default=True):
    """是/否问题"""
    default_text = "Y/n" if default else "y/N"
    answer = input(f"{prompt} [{default_text}]: ").strip().lower()

    if not answer:
        return default

    return answer in ['y', 'yes', '是']


def save_config(config, filename="mail_config_auto.json"):
    """保存配置到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


def load_saved_config(filename="mail_config_auto.json"):
    """加载已保存的配置"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return None


def interactive_setup():
    """交互式配置向导"""
    print_header()

    print("\n欢迎使用网易企业邮箱下载工具！")
    print("本工具将帮助您轻松下载邮箱中的所有邮件到电脑。")
    print("\n接下来，我会问您几个简单的问题，请按照提示操作即可。\n")

    # 检查是否有已保存的配置
    saved_config = load_saved_config()
    if saved_config:
        print("检测到之前保存的配置：")
        print(f"  邮箱账号: {saved_config.get('email_account')}")
        print(f"  保存目录: {saved_config.get('save_dir')}")
        if yes_no_question("\n是否使用之前的配置？", True):
            return saved_config
        print()

    # 配置字典
    config = {}

    # 第1步：邮箱账号
    print("【步骤 1/5】输入邮箱信息")
    print("-" * 70)
    config['email_account'] = get_user_input("请输入您的邮箱账号（如: zhangsan@company.com）")

    while not config['email_account'] or '@' not in config['email_account']:
        print("✗ 邮箱格式不正确，请重新输入")
        config['email_account'] = get_user_input("请输入您的邮箱账号（如: zhangsan@company.com）")

    # 第2步：密码
    print("\n【步骤 2/5】输入密码")
    print("-" * 70)
    print("提示：建议使用「授权码」而不是直接使用邮箱密码")
    print("如何获取授权码：")
    print("  1. 登录网易企业邮箱网页版")
    print("  2. 进入「设置」->「安全」->「客户端授权密码」")
    print("  3. 生成新的授权码\n")

    config['email_password'] = get_user_input("请输入邮箱密码或授权码", password=True)

    while not config['email_password']:
        print("✗ 密码不能为空，请重新输入")
        config['email_password'] = get_user_input("请输入邮箱密码或授权码", password=True)

    # 第3步：保存位置
    print("\n【步骤 3/5】选择保存位置")
    print("-" * 70)
    default_dir = os.path.join(os.path.expanduser("~"), "邮件下载")
    config['save_dir'] = get_user_input(
        "邮件将保存到哪个文件夹？",
        default=default_dir
    )

    # 第4步：选择要下载的文件夹
    print("\n【步骤 4/5】选择要下载的邮件")
    print("-" * 70)
    print("您想下载哪些邮件？")
    print("  1. 只下载收件箱")
    print("  2. 只下载已发送")
    print("  3. 同时下载已发送和收件箱（推荐，先下载已发送）")
    print("  4. 自定义（连接后手动选择）")

    choice = get_user_input("请选择 [1-4]", default="3")

    if choice == "1":
        folders = ["INBOX"]
    elif choice == "2":
        folders = ["Sent"]
    elif choice == "3":
        folders = ["Sent", "INBOX"]  # 先下载已发送，再下载收件箱
    else:
        folders = None  # 稍后手动选择

    # 第5步：高级选项
    print("\n【步骤 5/5】高级选项")
    print("-" * 70)

    # 是否全部下载
    download_all = yes_no_question("是否下载所有邮件？（如果选择否，可以限制下载数量）", True)

    max_count = None
    if not download_all:
        try:
            max_count = int(get_user_input("下载最新的多少封邮件", default="100"))
        except:
            max_count = 100

    # 是否断点续传
    skip_existing = yes_no_question("是否启用断点续传？（推荐开启，下载中断后可以继续）", True)

    # 构建配置
    config['imap_server'] = "imap.qiye.163.com"
    config['imap_port'] = 993
    config['download_options'] = {
        'folders': folders,
        'max_count': max_count,
        'start_date': None,
        'skip_existing': skip_existing,
        'auto_confirm': True
    }

    # 显示配置摘要
    print("\n" + "=" * 70)
    print("配置摘要")
    print("=" * 70)
    print(f"邮箱账号: {config['email_account']}")
    print(f"保存位置: {config['save_dir']}")
    print(f"下载文件夹: {', '.join(folders) if folders else '稍后选择'}")
    print(f"下载数量: {'全部' if max_count is None else f'最新 {max_count} 封'}")
    print(f"断点续传: {'是' if skip_existing else '否'}")
    print("=" * 70)

    # 保存配置
    if yes_no_question("\n是否保存此配置？（下次可直接使用）", True):
        if save_config(config):
            print("✓ 配置已保存到 mail_config_auto.json")

    return config


def main():
    """主函数"""
    try:
        # 交互式配置
        config = interactive_setup()

        if not config:
            print("配置失败，程序退出")
            return

        # 确认开始下载
        print("\n" + "=" * 70)
        if not yes_no_question("准备就绪，是否开始下载？", True):
            print("已取消下载")
            return

        # 创建下载器
        downloader = NeteaseMailDownloader(
            config['email_account'],
            config['email_password'],
            config['save_dir'],
            config.get('imap_server', 'imap.qiye.163.com'),
            config.get('imap_port', 993)
        )

        # 连接和登录
        print("\n" + "=" * 70)
        print("正在连接邮箱...")
        print("=" * 70)

        if not downloader.connect():
            print("\n连接失败，请检查网络连接")
            return

        if not downloader.login():
            print("\n登录失败，请检查账号密码是否正确")
            print("提示：如果使用密码无法登录，请尝试使用授权码")
            return

        # 获取文件夹列表
        print("\n正在获取邮箱文件夹列表...")
        available_folders = downloader.get_folders()

        if available_folders:
            print("\n您的邮箱中有以下文件夹：")
            for idx, folder in enumerate(available_folders, 1):
                print(f"  {idx}. {folder}")

        # 确定要下载的文件夹
        download_options = config.get('download_options', {})
        folders = download_options.get('folders')

        if not folders:
            # 手动选择文件夹
            print("\n请选择要下载的文件夹（输入序号，多个用逗号分隔，如: 1,2,3）：")
            choice = input("您的选择: ").strip()

            try:
                indices = [int(x.strip()) for x in choice.split(',')]
                folders = [available_folders[i-1] for i in indices if 0 < i <= len(available_folders)]
            except:
                print("选择无效，将下载收件箱")
                folders = ["INBOX"]

        # 验证文件夹是否存在
        valid_folders = [f for f in folders if f in available_folders]
        if not valid_folders:
            print(f"\n警告：文件夹 {folders} 不存在，将尝试下载 INBOX")
            valid_folders = ["INBOX"]

        # 开始下载
        print("\n" + "=" * 70)
        print("开始下载邮件...")
        print("=" * 70)
        print(f"将下载以下文件夹: {', '.join(valid_folders)}")
        print("提示：下载过程中请保持网络连接稳定")
        print("=" * 70)

        total_stats = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0
        }

        overall_start_time = time.time()

        for idx, folder in enumerate(valid_folders, 1):
            print(f"\n{'#' * 70}")
            print(f"正在下载文件夹 [{idx}/{len(valid_folders)}]: {folder}")
            print(f"{'#' * 70}")

            stats = downloader.download_emails(
                folder=folder,
                max_count=download_options.get('max_count'),
                start_date=download_options.get('start_date'),
                skip_existing=download_options.get('skip_existing', True),
                auto_confirm=download_options.get('auto_confirm', True)
            )

            total_stats['success'] += stats['success']
            total_stats['failed'] += stats['failed']
            total_stats['skipped'] += stats['skipped']
            total_stats['total'] += stats['total']

        # 总体统计
        overall_elapsed = time.time() - overall_start_time

        print(f"\n{'=' * 70}")
        print(" " * 28 + "下载完成！")
        print(f"{'=' * 70}")
        print(f"处理文件夹数: {len(valid_folders)}")
        print(f"成功下载: {total_stats['success']} 封")
        print(f"下载失败: {total_stats['failed']} 封")
        print(f"跳过已下载: {total_stats['skipped']} 封")
        print(f"邮件总数: {total_stats['total']} 封")
        print(f"总用时: {int(overall_elapsed//60)}分{int(overall_elapsed%60)}秒")
        if total_stats['success'] > 0 and overall_elapsed > 0:
            print(f"平均速度: {total_stats['success']/overall_elapsed:.2f} 封/秒")
        print(f"\n邮件保存位置: {config['save_dir']}")
        print(f"{'=' * 70}\n")

        # 是否打开文件夹
        if yes_no_question("是否打开邮件保存文件夹？", True):
            import platform
            system = platform.system()
            if system == "Darwin":  # macOS
                os.system(f'open "{config["save_dir"]}"')
            elif system == "Windows":
                os.system(f'explorer "{config["save_dir"]}"')
            else:  # Linux
                os.system(f'xdg-open "{config["save_dir"]}"')

        print("\n感谢使用！")

    except KeyboardInterrupt:
        print("\n\n用户取消操作")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'downloader' in locals():
            downloader.close()

        input("\n按回车键退出...")


if __name__ == "__main__":
    main()
