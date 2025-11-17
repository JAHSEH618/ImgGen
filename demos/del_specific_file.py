#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件过滤清理工具
仅保留指定后缀的文件，删除其他文件
"""

import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import time

# 允许保留的文件扩展名（统一小写）
ALLOWED_EXTENSIONS = {
    '.txt', '.jpg', '.xlsx', '.docx', '.pdf', '.doc',
    '.xls', '.pptx', '.jpeg', '.rtf', '.psd',
    '.json', '.ppt', '.xlsm', '.wps'
}


class FileFilter:
    """文件过滤器类"""

    def __init__(self, root_path, dry_run=True, parallel=True):
        """
        初始化

        Args:
            root_path: 根目录路径
            dry_run: 是否为试运行模式（不实际删除）
            parallel: 是否使用并行处理
        """
        self.root_path = os.path.abspath(root_path)
        self.dry_run = dry_run
        self.parallel = parallel
        self.stats = defaultdict(int)
        self.to_delete = []
        self.to_keep = []
        self.errors = []

    def should_keep_file(self, filepath):
        """判断文件是否应该保留"""
        ext = Path(filepath).suffix.lower()
        return ext in ALLOWED_EXTENSIONS

    def scan_directory(self, directory):
        """
        扫描单个目录
        返回: (保留的文件列表, 删除的文件列表)
        """
        keep_files = []
        delete_files = []

        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    try:
                        if entry.is_file(follow_symlinks=False):
                            if self.should_keep_file(entry.path):
                                keep_files.append(entry.path)
                            else:
                                delete_files.append(entry.path)
                    except (PermissionError, OSError) as e:
                        self.errors.append((entry.path, str(e)))
                        continue
        except (PermissionError, OSError) as e:
            self.errors.append((directory, str(e)))

        return keep_files, delete_files

    def get_all_directories(self):
        """获取所有子目录"""
        directories = [self.root_path]
        try:
            for dirpath, dirnames, _ in os.walk(self.root_path):
                # 过滤符号链接
                dirnames[:] = [d for d in dirnames
                               if not os.path.islink(os.path.join(dirpath, d))]

                for dirname in dirnames:
                    directories.append(os.path.join(dirpath, dirname))
        except (PermissionError, OSError) as e:
            self.errors.append((self.root_path, str(e)))

        return directories

    def scan_all_parallel(self):
        """并行扫描所有目录"""
        directories = self.get_all_directories()

        with ThreadPoolExecutor() as executor:
            future_to_dir = {
                executor.submit(self.scan_directory, directory): directory
                for directory in directories
            }

            for future in as_completed(future_to_dir):
                try:
                    keep_files, delete_files = future.result()
                    self.to_keep.extend(keep_files)
                    self.to_delete.extend(delete_files)
                except Exception as e:
                    directory = future_to_dir[future]
                    self.errors.append((directory, str(e)))

    def scan_all_simple(self):
        """单线程扫描所有目录"""
        try:
            for dirpath, _, filenames in os.walk(self.root_path):
                for filename in filenames:
                    try:
                        filepath = os.path.join(dirpath, filename)
                        if os.path.isfile(filepath):
                            if self.should_keep_file(filepath):
                                self.to_keep.append(filepath)
                            else:
                                self.to_delete.append(filepath)
                    except (PermissionError, OSError) as e:
                        self.errors.append((filepath, str(e)))
        except (PermissionError, OSError) as e:
            self.errors.append((self.root_path, str(e)))

    def delete_files(self):
        """执行文件删除"""
        deleted_count = 0
        failed_count = 0

        for filepath in self.to_delete:
            try:
                if not self.dry_run:
                    os.remove(filepath)
                    deleted_count += 1
                else:
                    # 试运行模式，只统计
                    deleted_count += 1
            except (PermissionError, OSError) as e:
                self.errors.append((filepath, str(e)))
                failed_count += 1

        return deleted_count, failed_count

    def get_file_stats(self, files):
        """统计文件类型"""
        stats = defaultdict(int)
        for filepath in files:
            ext = Path(filepath).suffix.lower() or 'no_extension'
            stats[ext] += 1
        return stats

    def run(self):
        """执行主流程"""
        print(f"{'=' * 70}")
        print(f"文件过滤清理工具")
        print(f"{'=' * 70}")
        print(f"目标目录: {self.root_path}")
        print(f"运行模式: {'试运行（不会实际删除）' if self.dry_run else '实际删除'}")
        print(f"处理方式: {'并行处理' if self.parallel else '单线程处理'}")
        print(f"\n允许保留的文件类型:")
        print(f"{', '.join(sorted(ALLOWED_EXTENSIONS))}")
        print(f"\n正在扫描文件...")

        start_time = time.time()

        # 扫描文件
        if self.parallel:
            self.scan_all_parallel()
        else:
            self.scan_all_simple()

        scan_time = time.time() - start_time

        # 统计信息
        keep_stats = self.get_file_stats(self.to_keep)
        delete_stats = self.get_file_stats(self.to_delete)

        # 显示扫描结果
        print(f"\n{'=' * 70}")
        print(f"扫描完成 (耗时: {scan_time:.2f}秒)")
        print(f"{'=' * 70}")
        print(f"\n📁 将保留的文件: {len(self.to_keep):,} 个")
        if keep_stats:
            for ext, count in sorted(keep_stats.items(), key=lambda x: -x[1])[:10]:
                print(f"  {ext:15s}: {count:,}")

        print(f"\n🗑️  将删除的文件: {len(self.to_delete):,} 个")
        if delete_stats:
            for ext, count in sorted(delete_stats.items(), key=lambda x: -x[1])[:10]:
                print(f"  {ext:15s}: {count:,}")

        if self.errors:
            print(f"\n⚠️  遇到错误: {len(self.errors)} 个")
            print(f"  (详细错误信息见下方)")

        # 如果是试运行，显示示例文件
        if self.dry_run and self.to_delete:
            print(f"\n示例将被删除的文件 (前10个):")
            for filepath in self.to_delete[:10]:
                print(f"  - {filepath}")
            if len(self.to_delete) > 10:
                print(f"  ... 还有 {len(self.to_delete) - 10} 个文件")

        # 确认删除
        if not self.dry_run:
            print(f"\n{'!' * 70}")
            print(f"⚠️  警告: 即将删除 {len(self.to_delete):,} 个文件!")
            print(f"{'!' * 70}")
            confirm = input("\n确认删除? 输入 'YES' 继续: ")

            if confirm != 'YES':
                print("\n❌ 操作已取消")
                return

            print("\n正在删除文件...")
            delete_start = time.time()
            deleted, failed = self.delete_files()
            delete_time = time.time() - delete_start

            print(f"\n{'=' * 70}")
            print(f"删除完成 (耗时: {delete_time:.2f}秒)")
            print(f"{'=' * 70}")
            print(f"✅ 成功删除: {deleted:,} 个文件")
            if failed > 0:
                print(f"❌ 删除失败: {failed:,} 个文件")

        # 显示错误详情
        if self.errors:
            print(f"\n{'=' * 70}")
            print(f"错误详情:")
            print(f"{'=' * 70}")
            for path, error in self.errors[:20]:
                print(f"  {path}")
                print(f"    错误: {error}")
            if len(self.errors) > 20:
                print(f"  ... 还有 {len(self.errors) - 20} 个错误")

        print(f"\n{'=' * 70}")
        print(f"总耗时: {time.time() - start_time:.2f}秒")
        print(f"{'=' * 70}\n")


def main():
    """主函数"""
    # 获取目标路径
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = '.'

    # 检查路径有效性
    if not os.path.isdir(target_path):
        print(f"❌ 错误: '{target_path}' 不是有效的目录")
        sys.exit(1)

    # 解析参数
    dry_run = '--execute' not in sys.argv  # 默认试运行
    parallel = '--no-parallel' not in sys.argv  # 默认并行

    if dry_run:
        print("ℹ️  提示: 当前为试运行模式，不会实际删除文件")
        print("ℹ️  如需实际删除，请添加 --execute 参数\n")

    # 创建过滤器并运行
    filter_tool = FileFilter(target_path, dry_run=dry_run, parallel=parallel)
    filter_tool.run()


if __name__ == '__main__':
    main()