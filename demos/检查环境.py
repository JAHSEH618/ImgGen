#!/usr/bin/env python3
"""
环境检查脚本 - 确保程序能正常运行
"""

import sys
import os

def check_environment():
    """检查运行环境"""
    print("\n" + "=" * 60)
    print(" " * 20 + "环境检查")
    print("=" * 60 + "\n")

    # 检查 Python 版本
    print("1. 检查 Python 版本...")
    py_version = sys.version_info
    print(f"   ✓ Python {py_version.major}.{py_version.minor}.{py_version.micro}")

    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 6):
        print("   ✗ 警告: Python 版本过低，建议使用 3.6 或更高版本")
        return False

    # 检查是否有冲突的文件
    print("\n2. 检查文件冲突...")
    conflict_files = ['email.py', 'json.py', 'os.py', 'sys.py', 'time.py']
    conflicts_found = []

    for filename in conflict_files:
        if os.path.exists(filename):
            # 检查是否是空文件或我们自己的文件
            size = os.path.getsize(filename)
            if size < 100:  # 可能是冲突文件
                conflicts_found.append(filename)

    if conflicts_found:
        print(f"   ✗ 发现可能冲突的文件: {', '.join(conflicts_found)}")
        print("   建议删除这些文件")
        return False
    else:
        print("   ✓ 未发现文件冲突")

    # 检查必要的模块
    print("\n3. 检查必要的模块...")
    required_modules = [
        ('imaplib', 'IMAP 协议支持'),
        ('email', '邮件处理'),
        ('json', 'JSON 配置'),
        ('os', '文件操作'),
        ('sys', '系统操作'),
        ('time', '时间处理'),
        ('datetime', '日期时间'),
    ]

    all_ok = True
    for module_name, description in required_modules:
        try:
            __import__(module_name)
            print(f"   ✓ {module_name:15s} - {description}")
        except ImportError as e:
            print(f"   ✗ {module_name:15s} - 导入失败: {e}")
            all_ok = False

    # 检查程序文件
    print("\n4. 检查程序文件...")
    program_files = [
        'easy_mail_downloader.py',
        '启动邮件下载工具.command',
        '启动邮件下载工具.sh',
        '启动邮件下载工具.bat',
    ]

    for filename in program_files:
        if os.path.exists(filename):
            print(f"   ✓ {filename}")
        else:
            print(f"   ✗ {filename} - 文件不存在")

    # 总结
    print("\n" + "=" * 60)
    if all_ok:
        print(" " * 15 + "✓ 环境检查通过！")
        print("\n可以运行启动脚本开始使用程序")
    else:
        print(" " * 15 + "✗ 环境检查失败")
        print("\n请解决上述问题后再运行程序")
    print("=" * 60 + "\n")

    return all_ok


if __name__ == "__main__":
    try:
        result = check_environment()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n检查过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
