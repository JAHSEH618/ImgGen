#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Office文档4位数字密码暴力破解脚本
仅用于恢复您自己忘记的文档密码

使用方法:
1. 安装依赖: pip install msoffcrypto-tool tqdm
2. 修改下面的文件路径
3. 在PyCharm中右键点击运行
"""

import msoffcrypto
import io
import os
import sys
import time

# ==================== 配置区域 ====================
# 在这里修改您的文件路径
ENCRYPTED_FILE = r"/Users/okonma/Downloads/ddd.xlsx"  # 加密文件路径
OUTPUT_FILE = r"/Users/okonma/Downloads/ddddd.xlsx"  # 解密后保存路径

# 可选: 自定义密码范围
START_NUM = 0  # 起始数字
END_NUM = 9999  # 结束数字


# =================================================


def try_decrypt(file_path, password):
    """
    尝试使用给定密码解密文档

    Args:
        file_path: 加密文件路径
        password: 尝试的密码

    Returns:
        bool: 密码是否正确
    """
    try:
        with open(file_path, 'rb') as f:
            office_file = msoffcrypto.OfficeFile(f)
            office_file.load_key(password=password)

            # 尝试解密到内存
            decrypted = io.BytesIO()
            office_file.decrypt(decrypted)
            return True
    except Exception as e:
        # 如果是密码错误会抛出异常,返回False
        return False


def brute_force_4digits(file_path, output_path, start=0, end=9999):
    """
    暴力破解数字密码

    Args:
        file_path: 加密文档路径
        output_path: 解密后保存路径
        start: 起始数字
        end: 结束数字

    Returns:
        str: 找到的密码,如果未找到返回None
    """
    print(f"\n开始破解文件: {file_path}")
    print(f"密码范围: {start:04d} - {end:04d}")
    print(f"总共需要尝试: {end - start + 1} 个密码")
    print("-" * 60)

    start_time = time.time()

    try:
        # 导入tqdm用于显示进度条
        from tqdm import tqdm
        use_tqdm = True
    except ImportError:
        print("提示: 安装tqdm可以显示进度条 (pip install tqdm)")
        use_tqdm = False

    # 遍历所有数字
    iterator = range(start, end + 1)
    if use_tqdm:
        iterator = tqdm(iterator, desc="破解进度", ncols=80)

    for num in iterator:
        password = f"{num:04d}"  # 格式化为4位数字

        # 每100次尝试显示一次进度(如果没有tqdm)
        if not use_tqdm and num % 100 == 0:
            elapsed = time.time() - start_time
            speed = (num - start + 1) / elapsed if elapsed > 0 else 0
            remaining = (end - num) / speed if speed > 0 else 0
            print(f"当前尝试: {password} | 速度: {speed:.1f}次/秒 | 预计剩余: {remaining / 60:.1f}分钟")

        if try_decrypt(file_path, password):
            elapsed = time.time() - start_time

            print("\n" + "=" * 60)
            print(f"✓ 成功找到密码: {password}")
            print(f"✓ 用时: {elapsed:.1f} 秒 ({elapsed / 60:.1f} 分钟)")
            print("=" * 60)

            # 使用找到的密码解密并保存
            print("\n正在保存解密文件...")
            with open(file_path, 'rb') as f:
                office_file = msoffcrypto.OfficeFile(f)
                office_file.load_key(password=password)

                with open(output_path, 'wb') as out:
                    office_file.decrypt(out)

            print(f"✓ 文件已解密并保存到: {output_path}")
            return password

    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"✗ 未找到密码 (用时: {elapsed:.1f}秒)")
    print("=" * 60)
    return None


def main():
    """主函数"""
    print("=" * 60)
    print("Office文档4位数字密码破解工具")
    print("=" * 60)
    print()
    print("⚠️  警告: 仅用于恢复您自己的文档密码")
    print("⚠️  破解他人文档可能违法")
    print()

    # 检查文件是否存在
    if not os.path.exists(ENCRYPTED_FILE):
        print("=" * 60)
        print(f"❌ 错误: 文件不存在")
        print(f"路径: {ENCRYPTED_FILE}")
        print("=" * 60)
        print()
        print("请修改代码中的 ENCRYPTED_FILE 变量为正确的文件路径")
        print()
        print("示例 (Windows):")
        print('  ENCRYPTED_FILE = r"C:\\Users\\YourName\\Documents\\locked.xlsx"')
        print()
        print("示例 (相对路径):")
        print('  ENCRYPTED_FILE = "encrypted.xlsx"  # 与脚本在同一目录')
        print()
        input("按回车键退出...")
        sys.exit(1)

    # 检查输出目录是否存在
    output_dir = os.path.dirname(OUTPUT_FILE)
    if output_dir and not os.path.exists(output_dir):
        print(f"❌ 错误: 输出目录不存在: {output_dir}")
        input("按回车键退出...")
        sys.exit(1)

    print(f"✓ 加密文件: {ENCRYPTED_FILE}")
    print(f"✓ 输出文件: {OUTPUT_FILE}")
    print()

    # 确认开始
    print("准备开始破解...")
    print(f"将尝试 {START_NUM:04d} 到 {END_NUM:04d} 之间的所有密码")
    print()
    response = input("是否继续? (y/n): ")

    if response.lower() != 'y':
        print("已取消")
        sys.exit(0)

    # 开始破解
    result = brute_force_4digits(ENCRYPTED_FILE, OUTPUT_FILE, START_NUM, END_NUM)

    print()
    if result:
        print("=" * 60)
        print(f"🎉 破解成功!")
        print(f"🔑 密码: {result}")
        print(f"📁 解密文件: {OUTPUT_FILE}")
        print("=" * 60)
    else:
        print()
        print("💡 建议:")
        print("1. 确认密码确实是纯数字")
        print("2. 尝试扩大范围 (修改 START_NUM 和 END_NUM)")
        print("3. 考虑密码可能包含字母或特殊字符")

    print()
    input("按回车键退出...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断,程序退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback

        traceback.print_exc()
        print()
        input("按回车键退出...")
        sys.exit(1)