#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高性能文件类型统计工具
递归统计目录下各类型文件数量
"""

import os
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys


def get_file_extension(filepath):
    """
    获取文件扩展名，统一转为小写
    无扩展名的文件标记为 'no_extension'
    """
    ext = Path(filepath).suffix.lower()
    return ext if ext else 'no_extension'


def scan_directory(directory):
    """
    扫描单个目录，返回该目录下的文件扩展名列表
    使用 os.scandir() 提高性能
    """
    extensions = []
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                try:
                    if entry.is_file(follow_symlinks=False):
                        ext = get_file_extension(entry.path)
                        extensions.append(ext)
                except (PermissionError, OSError):
                    # 忽略权限错误和其他OS错误
                    continue
    except (PermissionError, OSError):
        # 忽略无法访问的目录
        pass

    return extensions


def get_all_directories(root_path):
    """
    获取所有子目录路径（包括根目录）
    使用 os.walk 一次性获取所有目录
    """
    directories = [root_path]
    try:
        for dirpath, dirnames, _ in os.walk(root_path):
            # 过滤掉符号链接，避免循环
            dirnames[:] = [d for d in dirnames
                           if not os.path.islink(os.path.join(dirpath, d))]

            for dirname in dirnames:
                directories.append(os.path.join(dirpath, dirname))
    except (PermissionError, OSError):
        pass

    return directories


def count_files_parallel(root_path, max_workers=None):
    """
    使用多线程并行统计文件类型

    Args:
        root_path: 根目录路径
        max_workers: 最大线程数，默认为None（自动选择）

    Returns:
        Counter对象，包含各文件类型的数量
    """
    # 获取所有目录
    directories = get_all_directories(root_path)

    # 使用线程池并行处理
    file_counter = Counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有目录的扫描任务
        future_to_dir = {
            executor.submit(scan_directory, directory): directory
            for directory in directories
        }

        # 收集结果
        for future in as_completed(future_to_dir):
            try:
                extensions = future.result()
                file_counter.update(extensions)
            except Exception:
                # 忽略处理过程中的错误
                continue

    return file_counter


def count_files_simple(root_path):
    """
    简单版本：单线程统计（适合小目录或调试）
    """
    file_counter = Counter()

    try:
        for dirpath, _, filenames in os.walk(root_path):
            for filename in filenames:
                try:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.isfile(filepath):
                        ext = get_file_extension(filepath)
                        file_counter[ext] += 1
                except (PermissionError, OSError):
                    continue
    except (PermissionError, OSError):
        pass

    return file_counter


def format_results(counter, show_top=20):
    """
    格式化输出结果

    Args:
        counter: Counter对象
        show_top: 显示前N个最多的类型
    """
    if not counter:
        print("未找到任何文件")
        return

    total_files = sum(counter.values())
    print(f"\n{'=' * 60}")
    print(f"文件统计结果")
    print(f"{'=' * 60}")
    print(f"总文件数: {total_files:,}")
    print(f"文件类型数: {len(counter)}")
    print(f"\n前 {min(show_top, len(counter))} 种最多的文件类型:")
    print(f"{'-' * 60}")
    print(f"{'排名':<6}{'扩展名':<20}{'数量':<15}{'占比'}")
    print(f"{'-' * 60}")

    for rank, (ext, count) in enumerate(counter.most_common(show_top), 1):
        percentage = (count / total_files) * 100
        ext_display = ext if ext != 'no_extension' else '(无扩展名)'
        print(f"{rank:<6}{ext_display:<20}{count:<15,}{percentage:>6.2f}%")

    if len(counter) > show_top:
        other_count = sum(count for ext, count in counter.items()
                          if ext not in dict(counter.most_common(show_top)))
        other_percentage = (other_count / total_files) * 100
        print(f"{'-' * 60}")
        print(f"{'':6}{'其他类型':<20}{other_count:<15,}{other_percentage:>6.2f}%")

    print(f"{'=' * 60}\n")


def main():
    """主函数"""
    # 获取目标路径（默认为当前目录）
    target_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    target_path = os.path.abspath(target_path)

    if not os.path.isdir(target_path):
        print(f"错误: '{target_path}' 不是有效的目录")
        sys.exit(1)

    print(f"正在统计目录: {target_path}")
    print("请稍候...\n")

    # 使用并行版本（速度更快）
    result = count_files_parallel(target_path)

    # 如果需要单线程版本，取消下面的注释
    # result = count_files_simple(target_path)

    # 输出结果
    format_results(result, show_top=20)


if __name__ == '__main__':
    main()