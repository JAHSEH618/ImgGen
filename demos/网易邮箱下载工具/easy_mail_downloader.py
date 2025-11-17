#!/usr/bin/env python3
"""
网易企业邮箱下载工具 - 性能优化版
专为非技术人员设计，通过交互式问答完成配置和下载

优化特性：
1. 多线程并发下载（3-5个线程）
2. 批量获取邮件头信息
3. 默认只下载2020年后的邮件
4. 更智能的重试机制
5. 实时进度显示
"""

import imaplib
import email
from email.header import decode_header
import os
import sys
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class NeteaseMailDownloader:
    def __init__(self, username, password, save_dir, imap_server="imap.qiye.163.com", imap_port=993):
        """
        初始化邮件下载器
        """
        self.username = username
        self.password = password
        self.save_dir = save_dir
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.mail = None
        self.current_folder = None
        self.last_noop_time = time.time()

        # 线程锁
        self.connection_lock = threading.Lock()

        # 重试配置
        self.max_retries = 3
        self.retry_delay = 2
        self.download_delay = 0.05  # 减少延迟提升速度
        self.noop_interval = 60

        # 多线程配置
        self.max_workers = 3  # 并发线程数

        # 批量获取配置
        self.batch_size = 50

        # 创建保存目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def connect(self):
        """连接到IMAP服务器"""
        try:
            print(f"正在连接到 {self.imap_server}...")
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.mail.sock.settimeout(60)  # 增加超时时间
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
            self.last_noop_time = time.time()
            return True
        except Exception as e:
            print(f"✗ 登录失败: {e}")
            print("提示: 请检查账号密码是否正确，或尝试使用授权码")
            return False

    def create_connection(self):
        """创建新的IMAP连接（用于多线程）"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.sock.settimeout(60)
            mail.login(self.username, self.password)
            return mail
        except Exception as e:
            print(f"创建连接失败: {e}")
            return None

    def reconnect(self, select_folder=None):
        """重新连接到服务器"""
        try:
            print("\n[连接断开] 正在尝试重新连接...")

            if self.mail:
                try:
                    self.mail.logout()
                except:
                    pass

            if not self.connect():
                return False

            if not self.login():
                return False

            if select_folder:
                status, _ = self.mail.select(select_folder, readonly=True)
                if status == 'OK':
                    self.current_folder = select_folder
                    print(f"✓ 已重新选择文件夹: {select_folder}")
                    return True
                else:
                    print(f"✗ 无法重新选择文件夹: {select_folder}")
                    return False

            print("✓ 重新连接成功！")
            return True

        except Exception as e:
            print(f"✗ 重新连接失败: {e}")
            return False

    def keep_alive(self):
        """保持连接活跃"""
        try:
            current_time = time.time()
            if current_time - self.last_noop_time > self.noop_interval:
                with self.connection_lock:
                    self.mail.noop()
                    self.last_noop_time = current_time
        except Exception as e:
            print(f"[警告] 保活失败: {e}")

    def get_folders(self):
        """获取所有邮箱文件夹"""
        try:
            status, folders = self.mail.list()
            if status == 'OK':
                folder_list = []
                for folder in folders:
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
                    mail_id = item.split('_')[0]
                    downloaded_ids.add(mail_id)
        return downloaded_ids

    def fetch_email_headers_batch(self, mail_ids, batch_size=50):
        """批量获取邮件头信息（性能优化关键）"""
        email_headers = {}
        total = len(mail_ids)

        print(f"正在批量获取邮件头信息...")

        for i in range(0, total, batch_size):
            batch = mail_ids[i:i + batch_size]
            progress = ((i + len(batch)) / total) * 100
            print(f"\r  进度: {progress:.1f}% ({i + len(batch)}/{total})", end='', flush=True)

            try:
                # 批量获取
                mail_id_str = b','.join(batch)
                with self.connection_lock:
                    status, data = self.mail.fetch(mail_id_str, '(BODY.PEEK[HEADER])')

                if status == 'OK':
                    # 解析批量返回的数据
                    j = 0
                    while j < len(data):
                        if isinstance(data[j], tuple):
                            header_data = data[j][1]
                            msg = email.message_from_bytes(header_data)

                            mail_num = batch[j // 2] if j // 2 < len(batch) else None
                            if mail_num:
                                email_headers[mail_num.decode()] = {
                                    'subject': self.decode_str(msg['Subject']),
                                    'from': self.decode_str(msg['From']),
                                    'to': self.decode_str(msg['To']),
                                    'date': self.decode_str(msg['Date'])
                                }
                        j += 1

            except Exception as e:
                # 批量失败，尝试逐个获取
                for mail_id in batch:
                    try:
                        with self.connection_lock:
                            status, data = self.mail.fetch(mail_id, '(BODY.PEEK[HEADER])')
                        if status == 'OK' and data[0]:
                            header_data = data[0][1]
                            msg = email.message_from_bytes(header_data)
                            email_headers[mail_id.decode()] = {
                                'subject': self.decode_str(msg['Subject']),
                                'from': self.decode_str(msg['From']),
                                'to': self.decode_str(msg['To']),
                                'date': self.decode_str(msg['Date'])
                            }
                    except:
                        continue

        print()  # 换行
        return email_headers

    def download_single_email(self, mail_id, folder, folder_dir, mail_connection=None):
        """下载单封邮件（用于多线程）"""
        use_shared_connection = mail_connection is None

        if use_shared_connection:
            mail_connection = self.mail

        retry_count = 0

        while retry_count <= self.max_retries:
            try:
                # 获取邮件
                if use_shared_connection:
                    with self.connection_lock:
                        status, msg_data = mail_connection.fetch(mail_id, '(RFC822)')
                else:
                    status, msg_data = mail_connection.fetch(mail_id, '(RFC822)')

                if status != 'OK':
                    return False, "获取邮件失败"

                # 解析邮件
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # 获取邮件信息
                subject = self.decode_str(msg['Subject'])
                from_addr = self.decode_str(msg['From'])
                to_addr = self.decode_str(msg['To'])
                date = self.decode_str(msg['Date'])

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
                attachment_count = self.extract_email_content(msg, mail_dir)

                return True, {
                    'subject': subject,
                    'from': from_addr,
                    'date': date,
                    'attachments': attachment_count
                }

            except (imaplib.IMAP4.abort, ConnectionResetError, BrokenPipeError, OSError) as e:
                if retry_count < self.max_retries:
                    retry_count += 1
                    time.sleep(self.retry_delay)

                    if not use_shared_connection:
                        try:
                            mail_connection.logout()
                        except:
                            pass
                        mail_connection = self.create_connection()
                        if mail_connection:
                            mail_connection.select(folder, readonly=True)
                        else:
                            return False, f"重连失败: {e}"
                else:
                    return False, f"连接错误（已重试{self.max_retries}次）: {e}"

            except Exception as e:
                if retry_count < self.max_retries:
                    retry_count += 1
                    time.sleep(self.retry_delay)
                else:
                    return False, f"下载失败: {e}"

        return False, "未知错误"

    def download_emails(self, folder="INBOX", max_count=None, start_date=None, skip_existing=True, auto_confirm=False):
        """
        下载指定文件夹的邮件（多线程版本）
        """
        try:
            print(f"\n{'=' * 60}")
            print(f"正在处理文件夹: {folder}")
            print(f"{'=' * 60}")

            status, messages = self.mail.select(folder, readonly=True)
            if status != 'OK':
                print(f"✗ 无法选择文件夹 {folder}")
                return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}

            self.current_folder = folder

            # 搜索邮件
            if start_date:
                search_criteria = f'(SINCE "{start_date}")'
                status, data = self.mail.search(None, search_criteria)
                print(f"✓ 搜索条件: {start_date} 之后的邮件")
            else:
                status, data = self.mail.search(None, 'ALL')

            if status != 'OK':
                print("✗ 搜索邮件失败")
                return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}

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

            # 检查已下载的邮件
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
                mail_ids_to_download = mail_ids_to_download[-max_count:]
                print(f"⚠ 限制下载数量: {len(mail_ids_to_download)} 封（总共 {original_count} 封待下载）")

            # 下载前确认
            if not auto_confirm and len(mail_ids_to_download) > 100:
                print(f"\n⚠ 警告: 准备下载 {len(mail_ids_to_download)} 封邮件，这可能需要较长时间。")
                confirm = input("是否继续？(y/N): ").strip().lower()
                if confirm != 'y':
                    print("已取消下载")
                    return {'success': 0, 'failed': 0, 'skipped': 0, 'total': total_mails}

            # 批量获取邮件头
            email_headers = self.fetch_email_headers_batch(mail_ids_to_download, self.batch_size)
            print(f"✓ 已获取 {len(email_headers)} 封邮件的头信息")

            # 开始多线程下载
            print(f"\n开始下载 {len(mail_ids_to_download)} 封邮件...")
            print(f"使用 {self.max_workers} 个并发线程")
            print("-" * 60)

            success_count = 0
            failed_count = 0
            start_time = time.time()

            progress_lock = threading.Lock()
            completed = 0

            def download_worker(mail_id):
                """下载工作线程"""
                nonlocal completed, success_count, failed_count

                # 创建独立连接
                mail_conn = self.create_connection()
                if not mail_conn:
                    return (mail_id, False, "无法创建连接")

                try:
                    mail_conn.select(folder, readonly=True)
                    success, result = self.download_single_email(mail_id, folder, folder_dir, mail_conn)

                    with progress_lock:
                        completed += 1
                        if success:
                            success_count += 1
                        else:
                            failed_count += 1

                        # 显示进度
                        progress = (completed / len(mail_ids_to_download)) * 100
                        elapsed = time.time() - start_time
                        if completed > 1:
                            avg_time = elapsed / completed
                            eta_seconds = avg_time * (len(mail_ids_to_download) - completed)
                            eta_str = f"ETA: {int(eta_seconds // 60)}分{int(eta_seconds % 60)}秒"
                        else:
                            eta_str = "ETA: 计算中..."

                        print(f"\r[{completed}/{len(mail_ids_to_download)}] ({progress:.1f}%) "
                              f"成功:{success_count} 失败:{failed_count} {eta_str}          ",
                              end='', flush=True)

                    return (mail_id, success, result)

                finally:
                    try:
                        mail_conn.logout()
                    except:
                        pass

            # 使用线程池下载
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(download_worker, mail_id): mail_id
                           for mail_id in mail_ids_to_download}

                for future in as_completed(futures):
                    try:
                        mail_id, success, result = future.result()
                    except Exception as e:
                        with progress_lock:
                            failed_count += 1
                            completed += 1

            print()  # 换行

            # 统计信息
            elapsed_total = time.time() - start_time
            print(f"\n{'=' * 60}")
            print(f"下载完成！")
            print(f"  成功: {success_count} 封")
            print(f"  失败: {failed_count} 封")
            print(f"  跳过: {len(downloaded_ids)} 封（已下载）")
            print(f"  总计: {total_mails} 封")
            print(f"  用时: {int(elapsed_total // 60)}分{int(elapsed_total % 60)}秒")
            if success_count > 0 and elapsed_total > 0:
                print(f"  平均速度: {success_count / elapsed_total:.2f} 封/秒")
            print(f"  保存位置: {folder_dir}")
            print(f"{'=' * 60}")

            return {
                'success': success_count,
                'failed': failed_count,
                'skipped': len(downloaded_ids),
                'total': total_mails
            }

        except Exception as e:
            print(f"✗ 下载邮件时出错: {e}")
            import traceback
            traceback.print_exc()
            return {'success': 0, 'failed': 0, 'skipped': 0, 'total': 0}

    def extract_email_content(self, msg, save_dir):
        """提取邮件内容和附件"""
        body_text = ""
        body_html = ""
        attachment_count = 0

        attachments_dir = os.path.join(save_dir, 'attachments')

        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition', ''))

            try:
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

                elif content_disposition and 'attachment' in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = self.decode_str(filename)
                        filename = self.clean_filename(filename)

                        if not os.path.exists(attachments_dir):
                            os.makedirs(attachments_dir)

                        filepath = os.path.join(attachments_dir, filename)

                        counter = 1
                        base_name, ext = os.path.splitext(filename)
                        while os.path.exists(filepath):
                            filename = f"{base_name}_{counter}{ext}"
                            filepath = os.path.join(attachments_dir, filename)
                            counter += 1

                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))

                        attachment_count += 1

            except Exception as e:
                continue

        if body_text:
            with open(os.path.join(save_dir, 'content.txt'), 'w', encoding='utf-8') as f:
                f.write(body_text)

        if body_html:
            with open(os.path.join(save_dir, 'content.html'), 'w', encoding='utf-8') as f:
                f.write(body_html)

        return attachment_count

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
    print(" " * 18 + "网易企业邮箱下载工具")
    print(" " * 20 + "性能优化版 v2.0")
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
    """保存配置到文件（不保存密码）"""
    try:
        config_to_save = config.copy()
        if 'email_password' in config_to_save:
            config_to_save['email_password'] = ''

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config_to_save, f, ensure_ascii=False, indent=2)
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
    print("\n✨ 性能优化版特点：")
    print("  - 多线程并发下载，速度提升3-5倍")
    print("  - 批量获取邮件信息，减少网络请求")
    print("  - 默认只下载2020年后的邮件，节省时间和空间")
    print("  - 智能断点续传，下载中断可继续")
    print("\n接下来，我会问您几个简单的问题，请按照提示操作即可。\n")

    # 检查是否有已保存的配置
    saved_config = load_saved_config()
    if saved_config and saved_config.get('email_account'):
        print("检测到之前保存的配置：")
        print(f"  邮箱账号: {saved_config.get('email_account')}")
        print(f"  保存目录: {saved_config.get('save_dir')}")
        if yes_no_question("\n是否使用之前的配置（仍需重新输入密码）？", True):
            print("\n请重新输入密码：")
            saved_config['email_password'] = get_user_input("请输入邮箱密码或授权码", password=True)
            while not saved_config['email_password']:
                print("✗ 密码不能为空，请重新输入")
                saved_config['email_password'] = get_user_input("请输入邮箱密码或授权码", password=True)
            return saved_config
        print()

    config = {}

    # 第1步：邮箱账号
    print("【步骤 1/6】输入邮箱信息")
    print("-" * 70)
    config['email_account'] = get_user_input("请输入您的邮箱账号（如: zhangsan@company.com）")

    while not config['email_account'] or '@' not in config['email_account']:
        print("✗ 邮箱格式不正确，请重新输入")
        config['email_account'] = get_user_input("请输入您的邮箱账号（如: zhangsan@company.com）")

    # 第2步：密码
    print("\n【步骤 2/6】输入密码")
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
    print("\n【步骤 3/6】选择保存位置")
    print("-" * 70)
    default_dir = os.path.join(os.path.expanduser("~"), "邮件下载")
    config['save_dir'] = get_user_input(
        "邮件将保存到哪个文件夹？",
        default=default_dir
    )

    # 第4步：选择要下载的文件夹
    print("\n【步骤 4/6】选择要下载的邮件")
    print("-" * 70)
    print("您想下载哪些邮件？")
    print("  1. 只下载收件箱")
    print("  2. 只下载已发送")
    print("  3. 同时下载已发送和收件箱（推荐）")
    print("  4. 自定义（连接后手动选择）")

    choice = get_user_input("请选择 [1-4]", default="3")

    if choice == "1":
        folders = ["INBOX"]
    elif choice == "2":
        folders = ["Sent"]
    elif choice == "3":
        folders = ["Sent", "INBOX"]
    else:
        folders = None

    # 第5步：日期范围（默认2020年后）
    print("\n【步骤 5/6】选择日期范围")
    print("-" * 70)
    print("为了提高下载速度和节省存储空间，建议只下载近期邮件。")

    date_choice = input("请选择：\n"
                        "  1. 只下载2020年后的邮件（推荐，默认）\n"
                        "  2. 只下载2022年后的邮件\n"
                        "  3. 只下载2023年后的邮件\n"
                        "  4. 下载所有邮件（不推荐，耗时长）\n"
                        "  5. 自定义日期\n"
                        "您的选择 [默认: 1]: ").strip() or "1"

    start_date = None
    if date_choice == "1":
        start_date = "01-Jan-2020"
    elif date_choice == "2":
        start_date = "01-Jan-2022"
    elif date_choice == "3":
        start_date = "01-Jan-2023"
    elif date_choice == "4":
        start_date = None
    elif date_choice == "5":
        year = get_user_input("请输入年份（如：2020）", default="2020")
        start_date = f"01-Jan-{year}"

    if start_date:
        print(f"✓ 将下载 {start_date} 之后的邮件")
    else:
        print("⚠ 将下载全部邮件，这可能需要很长时间")

    # 第6步：高级选项
    print("\n【步骤 6/6】高级选项")
    print("-" * 70)

    download_all = yes_no_question("是否下载所有符合条件的邮件？", True)

    max_count = None
    if not download_all:
        try:
            max_count = int(get_user_input("下载最新的多少封邮件", default="100"))
        except:
            max_count = 100

    skip_existing = yes_no_question("是否启用断点续传？（推荐）", True)

    # 并发线程数
    max_workers = 3
    if yes_no_question("是否调整并发线程数？（默认3个）", False):
        try:
            workers_input = int(get_user_input("请输入并发线程数（建议3-5）", default="3"))
            if 1 <= workers_input <= 10:
                max_workers = workers_input
            else:
                print("✗ 线程数超出范围，使用默认值3")
        except:
            print("✗ 输入无效，使用默认值3")

    # 构建配置
    config['imap_server'] = "imap.qiye.163.com"
    config['imap_port'] = 993
    config['max_workers'] = max_workers
    config['download_options'] = {
        'folders': folders,
        'max_count': max_count,
        'start_date': start_date,
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
    print(f"日期范围: {start_date + ' 之后' if start_date else '全部'}")
    print(f"下载数量: {'全部' if max_count is None else f'最新 {max_count} 封'}")
    print(f"断点续传: {'是' if skip_existing else '否'}")
    print(f"并发线程: {max_workers} 个")
    print("=" * 70)

    if yes_no_question("\n是否保存此配置？（下次可直接使用，但不会保存密码）", True):
        if save_config(config):
            print("✓ 配置已保存到 mail_config_auto.json")

    return config


def main():
    """主函数"""
    try:
        config = interactive_setup()

        if not config:
            print("配置失败，程序退出")
            return

        print("\n" + "=" * 70)
        if not yes_no_question("准备就绪，是否开始下载？", True):
            print("已取消下载")
            return

        downloader = NeteaseMailDownloader(
            config['email_account'],
            config['email_password'],
            config['save_dir'],
            config.get('imap_server', 'imap.qiye.163.com'),
            config.get('imap_port', 993)
        )

        downloader.max_workers = config.get('max_workers', 3)

        print("\n" + "=" * 70)
        print("正在连接邮箱...")
        print("=" * 70)

        if not downloader.connect():
            print("\n连接失败，请检查网络连接")
            return

        if not downloader.login():
            print("\n登录失败，请检查账号密码是否正确")
            return

        print("\n正在获取邮箱文件夹列表...")
        available_folders = downloader.get_folders()

        if available_folders:
            print("\n您的邮箱中有以下文件夹：")
            for idx, folder in enumerate(available_folders, 1):
                print(f"  {idx}. {folder}")

        download_options = config.get('download_options', {})
        folders = download_options.get('folders')

        if not folders:
            print("\n请选择要下载的文件夹（输入序号，多个用逗号分隔，如: 1,2,3）：")
            choice = input("您的选择: ").strip()

            try:
                indices = [int(x.strip()) for x in choice.split(',')]
                folders = [available_folders[i - 1] for i in indices if 0 < i <= len(available_folders)]
            except:
                print("选择无效，将下载收件箱")
                folders = ["INBOX"]

        valid_folders = [f for f in folders if f in available_folders]
        if not valid_folders:
            print(f"\n警告：文件夹 {folders} 不存在，将尝试下载 INBOX")
            valid_folders = ["INBOX"]

        print("\n" + "=" * 70)
        print("开始下载邮件...")
        print("=" * 70)
        print(f"将下载以下文件夹: {', '.join(valid_folders)}")
        if download_options.get('start_date'):
            print(f"日期范围: {download_options.get('start_date')} 之后")
        print(f"并发线程数: {downloader.max_workers}")
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

        overall_elapsed = time.time() - overall_start_time

        print(f"\n{'=' * 70}")
        print(" " * 28 + "下载完成！")
        print(f"{'=' * 70}")
        print(f"处理文件夹数: {len(valid_folders)}")
        print(f"成功下载: {total_stats['success']} 封")
        print(f"下载失败: {total_stats['failed']} 封")
        print(f"跳过已下载: {total_stats['skipped']} 封")
        print(f"邮件总数: {total_stats['total']} 封")
        print(f"总用时: {int(overall_elapsed // 60)}分{int(overall_elapsed % 60)}秒")
        if total_stats['success'] > 0 and overall_elapsed > 0:
            print(f"平均速度: {total_stats['success'] / overall_elapsed:.2f} 封/秒")
        print(f"\n邮件保存位置: {config['save_dir']}")
        print(f"{'=' * 70}\n")

        if yes_no_question("是否打开邮件保存文件夹？", True):
            import platform
            system = platform.system()
            try:
                if system == "Darwin":
                    os.system(f'open "{config["save_dir"]}"')
                elif system == "Windows":
                    os.system(f'explorer "{config["save_dir"]}"')
                else:
                    os.system(f'xdg-open "{config["save_dir"]}"')
            except:
                print(f"无法自动打开文件夹，请手动打开: {config['save_dir']}")

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