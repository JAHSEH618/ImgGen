import socket
import mimetypes
from typing import List
from datetime import datetime, timedelta
from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
import traceback
import pytz


def to_rfc1132(d=None):
    if not d:
        d = datetime.now(pytz.timezone('Asia/Shanghai'))
    return d.strftime("%a, %d %b %Y %H:%M:%S %z")


mail_provider: str = 'qq'
tls: bool = True

# NGPLSRFEYQPWAEPF
    # mail_host: str = 'smtp.163.com'
    # mail_user: str = 'luka_ganziqi@163.com'
    # mail_pass: str = 'VWUFLZHUWKWDYZTE'
    # sender: str = 'luka_ganziqi@163.com'
    # qfeqyvlwjblubgjc gzq
    # hocwajiojwbsbeef wzq

if mail_provider == 'qq':
    mail_host: str = 'smtp.qq.com'
    mail_user: str = '393477346@qq.com'
    mail_pass: str = 'qfeqyvlwjblubgjc'
    sender: str = '393477346@qq.com'
else:
    mail_host: str = 'smtp.163.com'
    mail_user: str = 'tjhttw@163.com'
    mail_pass: str = 'FRSFNCPYVFCARPKM'
    sender: str = 'tjhttw@163.com'

receivers: List[str] = [
    'yybshyp@qq.com'
]

# 自定义发件人的显示名称
custom_sender = "393477346<393477346@qq.com>"

# 创建MIMEMultipart对象用于包含文本和附件
message = MIMEMultipart()
message['Subject'] = Header('关于北大会议中心项目的咨询', 'utf-8')
message['From'] = custom_sender
message['To'] = ', '.join(receivers)

# 添加邮件正文
text = "杨总：\n     我周一拜访了北大会议中心的张勇老师，他分管讲堂信息化建设的工作，之后有技术开发的需求。不过我听说会议中心自负盈亏，预算比较有限，同时也需要走招投标流程。想让您帮忙打听这个信息化项目的预算，以及会议中心这种项目的决策流程。感谢杨总！"
body = MIMEText(text, "plain", "utf-8")
message.attach(body)

# 添加附件部分
attachment_path = '/Users/ziqiwang/Desktop/wzq/email/T70跨境cc项目设计图（二期）.zip'  # 修改为你要发送的附件路径
attachment_name = 'T70跨境cc项目设计图（二期）.zip'  # 修改为附件显示的文件名

try:
    # with open(attachment_path, 'rb') as attachment_file:
    #     # 自动检测 MIME 类型
    #     mime_type, _ = mimetypes.guess_type(attachment_path)
    #     if not mime_type:
    #         mime_type = 'application/octet-stream'
    #     maintype, subtype = mime_type.split('/', 1)

    #     # 创建 MIMEBase 对象并设置为附件的 MIME 类型
    #     part = MIMEBase(maintype, subtype)
    #     part.set_payload(attachment_file.read())
    #     encoders.encode_base64(part)  # 对附件进行 base64 编码

    #     # 安全处理文件名编码，确保邮件客户端正确显示
    #     encoded_attachment_name = Header(attachment_name, 'utf-8').encode()

    #     # 设置附件的头信息
    #     part.add_header(
    #         'Content-Disposition',
    #         f'attachment; filename="{encoded_attachment_name}"; filename*="utf-8''{encoded_attachment_name}"'
    #     )
    #     part.add_header(
    #         'Content-Type',
    #         f'{mime_type}; name="{encoded_attachment_name}"'
    #     )
    #     message.attach(part)

    date = to_rfc1132(datetime(2021, 9, 15, 12, 54, 0, tzinfo=pytz.timezone('Asia/Shanghai')))
    message['Date'] = date
    print(f"Date set in email header: {date}")

    smtp_obj: SMTP = SMTP(host=mail_host, port=25, timeout=10)
    smtp_obj.set_debuglevel(1)
    smtp_obj.ehlo()
    if tls:
        smtp_obj.starttls()
        smtp_obj.ehlo()
    smtp_obj.login(mail_user, mail_pass)
    smtp_obj.sendmail(sender, receivers, message.as_string())
    print("Email sent successfully!")

except SMTPException as e:
    print("Error: unable to send email")
    traceback.print_exc()
except FileNotFoundError:
    print(f"Attachment file '{attachment_path}' not found.")
except Exception as e:
    print("An unexpected error occurred:", str(e))
    traceback.print_exc()
finally:
    try:
        smtp_obj.quit()
    except SMTPException:
        print("Failed to properly close the SMTP connection.")
    except NameError:
        print("smtp_obj was not defined.")