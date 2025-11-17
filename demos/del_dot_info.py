#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件清理工具
递归删除符合以下条件的文件和文件夹:
1. 后缀为 .info (以.info结尾)
2. 前缀为 ~$ (以~$开头,通常是Office临时文件)

作者: Auto Generated
版本: 2.0
"""

import os
from pathlib import Path
import logging
import shutil
from typing import Tuple, List
from datetime import datetime
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def format_size(size_bytes: int) -> str:
    """
    格式化文件大小为人类可读格式

    Args:
        size_bytes: 字节数

    Returns:
        格式化后的字符串 (如: 1.23 MB)
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def collect_target_items(directory: Path) -> List[Path]:
    """
    递归收集所有符合条件的文件和文件夹

    删除条件:
    1. 后缀为.info (以.info结尾)
    2. 前缀为~$ (以~$开头)

    Args:
        directory: 要扫描的目录

    Returns:
        符合条件的项目列表(按深度从深到浅排序)
    """
    target_items = []

    try:
        # 使用rglob递归遍历所有子目录
        for item in directory.rglob('*'):
            # 检查是否以.info结尾 或 以~$开头
            if item.name.endswith('.info') or item.name.startswith('~$'):
                target_items.append(item)
    except PermissionError as e:
        logger.warning(f"无权限访问某些目录: {e}")
    except Exception as e:
        logger.error(f"扫描时出错: {e}")

    # 按路径深度降序排序(先删除深层的,避免删除父目录后子项不存在)
    target_items.sort(key=lambda x: len(x.parts), reverse=True)

    return target_items


def generate_deletion_log(base_dir: Path, deleted_items: List, failed_items: List) -> str:
    """
    生成删除操作的日志文件

    Args:
        base_dir: 基础目录
        deleted_items: 成功删除的项目列表 [(类型, 路径, 大小), ...]
        failed_items: 删除失败的项目列表 [(类型, 路径, 错误信息), ...]

    Returns:
        日志文件路径
    """
    # 生成日志文件名(带时间戳)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"deletion_log_{timestamp}.txt"
    log_path = Path.cwd() / log_filename

    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            # 写入文件头
            f.write("=" * 80 + "\n")
            f.write("文件删除日志\n")
            f.write("=" * 80 + "\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"扫描目录: {base_dir}\n")
            f.write(f"成功删除: {len(deleted_items)} 个\n")
            f.write(f"删除失败: {len(failed_items)} 个\n")
            f.write("=" * 80 + "\n\n")

            # 写入成功删除的项目
            if deleted_items:
                f.write("【成功删除的项目】\n")
                f.write("-" * 80 + "\n")
                f.write(f"{'序号':<6} {'类型':<10} {'路径':<50} {'大小':<15}\n")
                f.write("-" * 80 + "\n")

                for idx, item in enumerate(deleted_items, 1):
                    if len(item) == 3:
                        item_type, path, size = item
                        f.write(f"{idx:<6} {item_type:<10} {path:<50} {size:<15}\n")
                    else:
                        item_type, path = item
                        f.write(f"{idx:<6} {item_type:<10} {path:<50} {'N/A':<15}\n")

                f.write("-" * 80 + "\n\n")

            # 写入删除失败的项目
            if failed_items:
                f.write("【删除失败的项目】\n")
                f.write("-" * 80 + "\n")
                f.write(f"{'序号':<6} {'类型':<10} {'路径':<40} {'失败原因':<20}\n")
                f.write("-" * 80 + "\n")

                for idx, (item_type, path, error) in enumerate(failed_items, 1):
                    f.write(f"{idx:<6} {item_type:<10} {path:<40} {error:<20}\n")

                f.write("-" * 80 + "\n\n")

            # 写入文件尾
            f.write("=" * 80 + "\n")
            f.write("日志结束\n")
            f.write("=" * 80 + "\n")

        return str(log_path)

    except Exception as e:
        logger.error(f"生成日志文件失败: {e}")
        return ""


def delete_target_items(directory: str = '.', dry_run: bool = False, recursive: bool = True) -> Tuple[int, int]:
    """
    删除指定目录下所有符合条件的文件和文件夹

    删除条件:
    1. 后缀为.info (以.info结尾)
    2. 前缀为~$ (以~$开头)

    Args:
        directory: 目标目录路径,默认为当前目录
        dry_run: 是否为演练模式(只显示不删除)
        recursive: 是否递归扫描子目录

    Returns:
        (成功删除数, 失败数)
    """
    # 用于记录删除的文件列表
    deleted_items = []
    failed_items = []
    try:
        dir_path = Path(directory).resolve()

        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"目录不存在或不是有效目录: {dir_path}")
            return 0, 0

        logger.info(f"扫描目录: {dir_path}")
        if recursive:
            logger.info("扫描模式: 递归扫描所有子目录")
        else:
            logger.info("扫描模式: 仅扫描当前目录")

        logger.info("删除条件: 1) 后缀为.info  2) 前缀为~$")

        # 收集所有符合条件的文件和文件夹
        if recursive:
            target_items = collect_target_items(dir_path)
        else:
            target_items = [item for item in dir_path.iterdir()
                            if item.name.endswith('.info') or item.name.startswith('~$')]

        if not target_items:
            logger.info("未找到任何符合条件的文件或文件夹")
            return 0, 0

        # 分类统计
        files = []
        dirs = []
        symlinks = []
        info_items = []
        temp_items = []

        for item in target_items:
            try:
                if item.is_symlink():
                    symlinks.append(item)
                elif item.is_file():
                    files.append(item)
                elif item.is_dir():
                    dirs.append(item)

                # 统计匹配类型
                if item.name.endswith('.info'):
                    info_items.append(item)
                if item.name.startswith('~$'):
                    temp_items.append(item)
            except:
                # 处理可能已被删除的项目(父目录先被删除)
                pass

        logger.info(f"\n找到 {len(target_items)} 个符合条件的项目:")
        logger.info(f"  ├─ 文件: {len(files)} 个")
        logger.info(f"  ├─ 文件夹: {len(dirs)} 个")
        logger.info(f"  └─ 符号链接: {len(symlinks)} 个")
        logger.info(f"\n按匹配类型统计:")
        logger.info(f"  ├─ 后缀为.info: {len(info_items)} 个")
        logger.info(f"  └─ 前缀为~$: {len(temp_items)} 个")

        # ==================== 演练模式 ====================
        if dry_run:
            logger.info("\n" + "=" * 60)
            logger.info("📋 演练模式 - 以下文件将被删除(不会实际删除)")
            logger.info("=" * 60)

            # 显示详细列表
            for item in target_items:
                try:
                    relative_path = item.relative_to(dir_path)
                    if item.is_dir():
                        item_type = "📁 DIR "
                        # 计算文件夹大小
                        try:
                            total_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                            size_str = format_size(total_size)
                            logger.info(f"  [{item_type}] {relative_path} ({size_str})")
                        except:
                            logger.info(f"  [{item_type}] {relative_path}")
                    elif item.is_symlink():
                        item_type = "🔗 LINK"
                        logger.info(f"  [{item_type}] {relative_path}")
                    else:
                        item_type = "📄 FILE"
                        try:
                            size_str = format_size(item.stat().st_size)
                            logger.info(f"  [{item_type}] {relative_path} ({size_str})")
                        except:
                            logger.info(f"  [{item_type}] {relative_path}")
                except:
                    pass

            # 统计结论
            logger.info("\n" + "=" * 60)
            logger.info("📊 统计结论")
            logger.info("=" * 60)
            logger.info(f"总计: {len(target_items)} 个符合条件的项目")
            logger.info(f"  ├─ 文件: {len(files)} 个")
            logger.info(f"  ├─ 文件夹: {len(dirs)} 个")
            logger.info(f"  └─ 符号链接: {len(symlinks)} 个")
            logger.info(f"\n按匹配类型:")
            logger.info(f"  ├─ 后缀为.info: {len(info_items)} 个")
            logger.info(f"  └─ 前缀为~$: {len(temp_items)} 个")

            # 计算总大小
            total_size = 0
            for item in target_items:
                try:
                    if item.is_file():
                        total_size += item.stat().st_size
                    elif item.is_dir():
                        total_size += sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                except:
                    pass

            if total_size > 0:
                logger.info(f"\n💾 预计释放空间: {format_size(total_size)}")

            logger.info("=" * 60)
            logger.info("💡 提示: 使用 -y 参数执行实际删除操作")
            logger.info("=" * 60 + "\n")

            return len(target_items), 0

        # ==================== 实际删除模式 ====================
        success_count = 0
        fail_count = 0

        logger.info("\n" + "=" * 60)
        logger.info("🗑️  开始删除操作")
        logger.info("=" * 60 + "\n")

        # 按深度从深到浅删除(避免删除父目录后子项报错)
        for item in target_items:
            try:
                # 检查项目是否还存在(可能父目录已被删除)
                if not item.exists():
                    continue

                relative_path = item.relative_to(dir_path)

                if item.is_symlink():
                    # 删除符号链接
                    item.unlink()
                    logger.info(f"✓ 已删除符号链接: {relative_path}")
                    deleted_items.append(("符号链接", str(relative_path)))
                    success_count += 1

                elif item.is_file():
                    # 删除文件
                    if not os.access(item, os.W_OK):
                        logger.error(f"✗ 无写权限: {relative_path}")
                        failed_items.append(("文件", str(relative_path), "无写权限"))
                        fail_count += 1
                        continue

                    file_size = item.stat().st_size
                    item.unlink()
                    logger.info(f"✓ 已删除文件: {relative_path}")
                    deleted_items.append(("文件", str(relative_path), format_size(file_size)))
                    success_count += 1

                elif item.is_dir():
                    # 删除文件夹
                    if not os.access(item, os.W_OK):
                        logger.error(f"✗ 无写权限: {relative_path}")
                        failed_items.append(("文件夹", str(relative_path), "无写权限"))
                        fail_count += 1
                        continue

                    # 计算文件夹大小
                    try:
                        dir_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                    except:
                        dir_size = 0

                    shutil.rmtree(item)
                    logger.info(f"✓ 已删除文件夹: {relative_path}")
                    deleted_items.append(("文件夹", str(relative_path), format_size(dir_size)))
                    success_count += 1

            except PermissionError:
                try:
                    relative_path = item.relative_to(dir_path)
                    logger.error(f"✗ 权限不足: {relative_path}")
                    failed_items.append(("未知", str(relative_path), "权限不足"))
                except:
                    logger.error(f"✗ 权限不足: {item.name}")
                    failed_items.append(("未知", item.name, "权限不足"))
                fail_count += 1

            except FileNotFoundError:
                # 已被删除(父目录删除导致),忽略
                pass

            except OSError as e:
                try:
                    relative_path = item.relative_to(dir_path)
                    logger.error(f"✗ 删除失败 {relative_path}: {e}")
                    failed_items.append(("未知", str(relative_path), str(e)))
                except:
                    logger.error(f"✗ 删除失败 {item.name}: {e}")
                    failed_items.append(("未知", item.name, str(e)))
                fail_count += 1

            except Exception as e:
                try:
                    relative_path = item.relative_to(dir_path)
                    logger.error(f"✗ 未知错误 {relative_path}: {e}")
                    failed_items.append(("未知", str(relative_path), str(e)))
                except:
                    logger.error(f"✗ 未知错误 {item.name}: {e}")
                    failed_items.append(("未知", item.name, str(e)))
                fail_count += 1

        # 汇总结果
        logger.info("\n" + "=" * 60)
        logger.info("✅ 删除操作完成")
        logger.info("=" * 60)
        logger.info(f"成功: {success_count} 个")
        logger.info(f"失败: {fail_count} 个")
        logger.info(f"总计: {success_count + fail_count} 个")
        logger.info("=" * 60 + "\n")

        # 生成删除日志文件
        if success_count > 0 or fail_count > 0:
            log_filename = generate_deletion_log(dir_path, deleted_items, failed_items)
            logger.info(f"📄 删除日志已保存到: {log_filename}\n")

        return success_count, fail_count

    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        return 0, 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='递归删除文件清理工具 - 删除后缀为.info和前缀为~$的文件/文件夹',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s --dry-run              # 演练模式,查看将删除什么
  %(prog)s -y                     # 直接删除当前目录
  %(prog)s -d /path/to/dir -y     # 删除指定目录
  %(prog)s --no-recursive -y      # 仅删除当前目录,不递归

删除条件:
  1. 后缀为 .info (如: data.info, backup.info)
  2. 前缀为 ~$ (如: ~$document.docx, ~$temp.xlsx)
        """
    )

    parser.add_argument('-d', '--directory', default='.',
                        help='目标目录路径 (默认: 当前目录)')
    parser.add_argument('--dry-run', action='store_true',
                        help='演练模式,只显示将删除的文件,不实际删除')
    parser.add_argument('-y', '--yes', action='store_true',
                        help='跳过确认,直接执行删除')
    parser.add_argument('--no-recursive', action='store_true',
                        help='不递归子目录,仅扫描当前目录')

    args = parser.parse_args()

    recursive = not args.no_recursive

    # 如果不是演练模式且未指定-y参数,则需要确认
    if not args.dry_run and not args.yes:
        mode_text = "递归扫描所有子目录" if recursive else "仅扫描当前目录"
        print("\n" + "=" * 60)
        print("⚠️  警告: 此操作将删除以下类型的文件和文件夹:")
        print("=" * 60)
        print("  1) 后缀为 .info (以.info结尾)")
        print("  2) 前缀为 ~$ (以~$开头)")
        print(f"\n扫描模式: {mode_text}")
        print(f"目标目录: {os.path.abspath(args.directory)}")
        print("=" * 60)
        confirm = input("\n确认继续? (y/n): ")
        if confirm.lower() != 'y':
            logger.info("❌ 操作已取消")
            return
        print()

    delete_target_items(args.directory, args.dry_run, recursive)


if __name__ == "__main__":
    main()