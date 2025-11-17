#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
递归检测目录结构问题:
1. 单个目录下文件/文件夹数量超过9500
2. 文件名超过255字节
"""

import os
import sys


def check_directory(path='.'):
    """
    递归检查目录结构

    Args:
        path: 要检查的根目录路径,默认为当前目录
    """
    issues_found = []
    dir_stats = []  # 存储每个目录的统计信息
    total_files = 0
    total_dirs = 0

    print(f"开始检查目录: {os.path.abspath(path)}\n")
    print("=" * 70)

    for root, dirs, files in os.walk(path):
        num_files = len(files)
        num_dirs = len(dirs)
        total_items = num_files + num_dirs

        # 统计信息
        total_files += num_files
        total_dirs += num_dirs
        dir_stats.append({
            'path': root,
            'files': num_files,
            'dirs': num_dirs,
            'total': total_items
        })

        # 检查1: 单个目录下的项目总数
        if total_items > 9500:
            issue = f"⚠️  目录包含过多项目: {root}\n   项目数量: {total_items} (目录: {num_dirs}, 文件: {num_files})"
            issues_found.append(issue)
            print(issue)
            print("-" * 70)

        # 检查2: 文件名长度(以字节计)
        for name in dirs + files:
            name_bytes = len(name.encode('utf-8'))
            if name_bytes > 255:
                full_path = os.path.join(root, name)
                issue = f"⚠️  文件/目录名过长: {full_path}\n   名称: {name}\n   字节长度: {name_bytes}"
                issues_found.append(issue)
                print(issue)
                print("-" * 70)

    # 输出检查结果摘要
    print("\n" + "=" * 70)
    print("检查完成!")
    print("=" * 70)

    # 输出统计信息
    print("\n📊 目录统计信息:")
    print("-" * 70)
    print(f"总文件数: {total_files}")
    print(f"总目录数: {total_dirs}")
    print(f"总计: {total_files + total_dirs}")

    print("\n📁 各目录详细统计:")
    print("-" * 70)
    # 按文件数量排序,方便查看
    dir_stats.sort(key=lambda x: x['total'], reverse=True)
    for stat in dir_stats:
        rel_path = os.path.relpath(stat['path'], path)
        if rel_path == '.':
            rel_path = '(根目录)'
        print(f"{rel_path}")
        print(f"  文件: {stat['files']}, 目录: {stat['dirs']}, 合计: {stat['total']}")

    if issues_found:
        print("\n" + "=" * 70)
        print(f"⚠️  发现 {len(issues_found)} 个问题:")
        print("=" * 70)
        for i, issue in enumerate(issues_found, 1):
            print(f"\n{i}. {issue}")
    else:
        print("\n" + "=" * 70)
        print("✅ 未发现任何问题!")
        print("=" * 70)

    return issues_found


def main():
    """主函数"""
    # 获取命令行参数指定的目录,默认为当前目录
    target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

    # 检查目录是否存在
    if not os.path.exists(target_dir):
        print(f"错误: 目录不存在 - {target_dir}")
        sys.exit(1)

    if not os.path.isdir(target_dir):
        print(f"错误: 路径不是目录 - {target_dir}")
        sys.exit(1)

    try:
        issues = check_directory(target_dir)
        # 如果发现问题,返回非零退出码
        sys.exit(1 if issues else 0)
    except PermissionError as e:
        print(f"\n错误: 权限不足 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()