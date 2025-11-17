#!/usr/bin/env python3
"""
递归删除当前目录及其子目录下所有名为 #HowToRecover.txt 的文件
高性能、稳定的实现
"""

import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def delete_file_safe(filepath):
    """
    安全地删除单个文件

    Args:
        filepath: 文件路径

    Returns:
        tuple: (成功标志, 文件路径, 错误信息)
    """
    try:
        os.remove(filepath)
        return (True, filepath, None)
    except PermissionError:
        return (False, filepath, "权限不足")
    except FileNotFoundError:
        return (False, filepath, "文件不存在(可能已被删除)")
    except Exception as e:
        return (False, filepath, str(e))


def find_and_delete_files(root_dir, target_filename, use_threading=True, max_workers=10):
    """
    查找并删除指定文件

    Args:
        root_dir: 根目录
        target_filename: 目标文件名
        use_threading: 是否使用多线程
        max_workers: 最大工作线程数

    Returns:
        dict: 统计信息
    """
    stats = {
        'found': 0,
        'deleted': 0,
        'failed': 0,
        'errors': []
    }

    # 使用 Path.rglob 进行快速递归搜索
    root_path = Path(root_dir)
    files_to_delete = []

    logger.info(f"开始扫描目录: {root_dir}")

    try:
        # 查找所有匹配的文件
        for filepath in root_path.rglob(target_filename):
            if filepath.is_file():
                files_to_delete.append(filepath)
                stats['found'] += 1

        logger.info(f"找到 {stats['found']} 个匹配文件")

        if not files_to_delete:
            logger.info("没有找到需要删除的文件")
            return stats

        # 删除文件
        if use_threading and len(files_to_delete) > 5:
            # 使用多线程处理大量文件
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(delete_file_safe, str(fp)): fp
                    for fp in files_to_delete
                }

                for future in as_completed(futures):
                    success, filepath, error = future.result()
                    if success:
                        stats['deleted'] += 1
                        logger.info(f"已删除: {filepath}")
                    else:
                        stats['failed'] += 1
                        stats['errors'].append((filepath, error))
                        logger.error(f"删除失败: {filepath} - {error}")
        else:
            # 单线程处理少量文件
            for filepath in files_to_delete:
                success, fp, error = delete_file_safe(str(filepath))
                if success:
                    stats['deleted'] += 1
                    logger.info(f"已删除: {fp}")
                else:
                    stats['failed'] += 1
                    stats['errors'].append((fp, error))
                    logger.error(f"删除失败: {fp} - {error}")

    except PermissionError as e:
        logger.error(f"访问目录权限不足: {e}")
    except Exception as e:
        logger.error(f"发生错误: {e}")

    return stats


def main():
    """主函数"""
    import argparse

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='递归删除指定目录下所有名为 #HowToRecover.txt 的文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s                          # 删除当前目录下的文件
  %(prog)s /path/to/dir             # 删除指定目录下的文件
  %(prog)s /path/to/dir -y          # 跳过确认直接删除
  %(prog)s /path/to/dir -w 20       # 使用20个线程
  %(prog)s /path/to/dir --no-thread # 使用单线程模式
        '''
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='要扫描的根目录 (默认: 当前目录)'
    )
    parser.add_argument(
        '-f', '--filename',
        default='#HowToRecover.txt',
        help='要删除的文件名 (默认: #HowToRecover.txt)'
    )
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='跳过确认，直接删除'
    )
    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=10,
        help='最大工作线程数 (默认: 10)'
    )
    parser.add_argument(
        '--no-thread',
        action='store_true',
        help='禁用多线程，使用单线程模式'
    )

    args = parser.parse_args()

    # 配置参数
    TARGET_FILENAME = args.filename
    ROOT_DIR = os.path.abspath(args.directory)
    USE_THREADING = not args.no_thread
    MAX_WORKERS = args.workers

    # 检查目录是否存在
    if not os.path.exists(ROOT_DIR):
        logger.error(f"错误: 目录不存在: {ROOT_DIR}")
        sys.exit(1)

    if not os.path.isdir(ROOT_DIR):
        logger.error(f"错误: 路径不是目录: {ROOT_DIR}")
        sys.exit(1)

    logger.info("=" * 60)
    logger.info(f"目标目录: {ROOT_DIR}")
    logger.info(f"目标文件: {TARGET_FILENAME}")
    logger.info(f"多线程模式: {'启用 (%d线程)' % MAX_WORKERS if USE_THREADING else '禁用'}")
    logger.info("=" * 60)

    # 确认操作
    if not args.yes:
        try:
            confirm = input(
                f"\n⚠️  警告: 将递归删除 '{ROOT_DIR}' 下所有名为 '{TARGET_FILENAME}' 的文件\n是否继续? (yes/no): ")
            if confirm.lower() not in ['yes', 'y']:
                logger.info("操作已取消")
                return
        except KeyboardInterrupt:
            logger.info("\n操作已取消")
            return

    # 执行删除
    stats = find_and_delete_files(
        ROOT_DIR,
        TARGET_FILENAME,
        use_threading=USE_THREADING,
        max_workers=MAX_WORKERS
    )

    # 输出统计信息
    logger.info("=" * 60)
    logger.info("删除完成!")
    logger.info(f"找到文件: {stats['found']}")
    logger.info(f"成功删除: {stats['deleted']}")
    logger.info(f"删除失败: {stats['failed']}")

    if stats['errors']:
        logger.info("\n失败详情:")
        for filepath, error in stats['errors']:
            logger.error(f"  {filepath}: {error}")

    logger.info("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序异常: {e}")
        sys.exit(1)