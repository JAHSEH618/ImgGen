import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metadata_parser.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MetadataParser:
    """高性能、稳定的metadata.json解析器"""

    def __init__(self, max_workers: int = 4, max_file_size: int = 10 * 1024 * 1024):
        """
        初始化解析器

        Args:
            max_workers: 最大并发线程数
            max_file_size: 最大文件大小限制(字节), 默认10MB
        """
        self.max_workers = max_workers
        self.max_file_size = max_file_size
        self.excluded_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}

    def should_skip_directory(self, dirname: str) -> bool:
        """判断是否应该跳过某个目录"""
        return dirname in self.excluded_dirs or dirname.startswith('.')

    def find_metadata_files(self, root_path: str = '.') -> List[str]:
        """
        查找所有metadata.json文件

        Args:
            root_path: 根目录路径

        Returns:
            metadata.json文件路径列表
        """
        metadata_files = []

        try:
            for root, dirs, files in os.walk(root_path):
                # 过滤掉不需要搜索的目录，提高性能
                dirs[:] = [d for d in dirs if not self.should_skip_directory(d)]

                if 'metadata.json' in files:
                    file_path = os.path.join(root, 'metadata.json')
                    metadata_files.append(file_path)

        except PermissionError as e:
            logger.warning(f"权限不足，无法访问: {e}")
        except Exception as e:
            logger.error(f"遍历目录时出错: {e}")

        return metadata_files

    def parse_single_file(self, file_path: str) -> Optional[Dict]:
        """
        解析单个metadata.json文件

        Args:
            file_path: 文件路径

        Returns:
            包含id、subject和path的字典，失败返回None
        """
        try:
            # 检查文件大小
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                logger.warning(f"文件过大，跳过: {file_path} ({file_size} bytes)")
                return None

            if file_size == 0:
                logger.warning(f"文件为空，跳过: {file_path}")
                return None

            # 读取并解析JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 提取字段（使用.get()避免KeyError）
            return {
                'id': data.get('id', 'N/A'),
                'subject': data.get('subject', 'N/A'),
                'path': file_path
            }

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误 [{file_path}]: {e}")
            return None
        except UnicodeDecodeError as e:
            logger.error(f"编码错误 [{file_path}]: {e}")
            # 尝试使用其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    data = json.load(f)
                return {
                    'id': data.get('id', 'N/A'),
                    'subject': data.get('subject', 'N/A'),
                    'path': file_path
                }
            except Exception:
                return None
        except PermissionError:
            logger.warning(f"权限不足，无法读取: {file_path}")
            return None
        except Exception as e:
            logger.error(f"读取文件时出错 [{file_path}]: {e}")
            return None

    def parse_all_files(self, file_paths: List[str]) -> List[Dict]:
        """
        并发解析所有文件

        Args:
            file_paths: 文件路径列表

        Returns:
            解析结果列表
        """
        results = []

        # 使用线程池并发处理
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {
                executor.submit(self.parse_single_file, path): path
                for path in file_paths
            }

            for future in as_completed(future_to_path):
                try:
                    result = future.result(timeout=5)  # 5秒超时
                    if result:
                        results.append(result)
                except TimeoutError:
                    path = future_to_path[future]
                    logger.error(f"处理超时: {path}")
                except Exception as e:
                    logger.error(f"处理文件时出错: {e}")

        return results

    def print_table(self, results: List[Dict]) -> None:
        """
        以表格形式打印结果

        Args:
            results: 解析结果列表
        """
        if not results:
            print("\n未找到任何有效的metadata.json文件")
            return

        # 计算列宽
        max_id_len = max(len(str(r['id'])) for r in results)
        max_subject_len = min(max(len(str(r['subject'])) for r in results), 100)  # 终端显示限制在100字符

        id_width = max(max_id_len, 10)
        subject_width = max(max_subject_len, 20)

        separator = "=" * (15 + id_width + subject_width)

        print(f"\n{separator}")
        print(f"{'序号':<8} {'ID':<{id_width}} {'主题':<{subject_width}}")
        print(separator)

        for index, item in enumerate(results, 1):
            id_str = str(item['id'])[:id_width]
            subject_str = str(item['subject'])
            # 如果主题过长,截断并添加省略号
            if len(subject_str) > subject_width:
                subject_str = subject_str[:subject_width - 3] + "..."
            print(f"{index:<8} {id_str:<{id_width}} {subject_str:<{subject_width}}")

        print(separator)
        print(f"\n总共找到 {len(results)} 个有效的metadata.json文件\n")

    def save_to_excel(self, results: List[Dict], output_file: str = 'metadata_summary.xlsx') -> None:
        """
        保存结果到Excel文件

        Args:
            results: 解析结果列表
            output_file: 输出文件名
        """
        if not results:
            return

        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

            # 创建工作簿
            wb = Workbook()
            ws = wb.active
            ws.title = "Metadata汇总"

            # 设置表头样式
            header_font = Font(bold=True, size=12, color="FFFFFF")
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")

            # 边框样式
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

            # 写入表头
            headers = ['序号', 'ID', '主题', '文件路径']
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
                cell.border = thin_border

            # 写入数据
            for index, item in enumerate(results, 1):
                ws.cell(row=index + 1, column=1, value=index).border = thin_border
                ws.cell(row=index + 1, column=2, value=str(item['id'])).border = thin_border

                # 主题列 - 支持长文本,自动换行
                subject_cell = ws.cell(row=index + 1, column=3, value=str(item['subject']))
                subject_cell.border = thin_border
                subject_cell.alignment = Alignment(wrap_text=True, vertical="top")

                ws.cell(row=index + 1, column=4, value=item['path']).border = thin_border

                # 居中对齐序号和ID
                ws.cell(row=index + 1, column=1).alignment = Alignment(horizontal="center", vertical="center")
                ws.cell(row=index + 1, column=2).alignment = Alignment(horizontal="center", vertical="center")

                # 文件路径自动换行
                ws.cell(row=index + 1, column=4).alignment = Alignment(wrap_text=True, vertical="top")

            # 自动调整列宽
            ws.column_dimensions['A'].width = 8
            ws.column_dimensions['B'].width = 20
            ws.column_dimensions['C'].width = 80  # 主题列宽度增加到80,支持长文本
            ws.column_dimensions['D'].width = 60

            # 冻结首行
            ws.freeze_panes = 'A2'

            # 保存文件
            output_path = os.path.join(os.getcwd(), output_file)
            wb.save(output_path)

            logger.info(f"结果已保存到 {output_path}")
            print(f"✓ 结果已保存到 Excel 文件: {output_path}")

        except ImportError:
            logger.error("未安装 openpyxl 库,正在尝试安装...")
            print("\n提示: 需要安装 openpyxl 库来生成 Excel 文件")
            print("请运行: pip install openpyxl")
            print("\n尝试保存为CSV格式...")
            self.save_to_csv(results)
        except Exception as e:
            logger.error(f"保存Excel文件时出错: {e}")
            print(f"保存Excel失败: {e}")
            print("尝试保存为CSV格式...")
            self.save_to_csv(results)

    def save_to_csv(self, results: List[Dict], output_file: str = 'metadata_summary.csv') -> None:
        """
        保存结果到CSV文件(备用方案)

        Args:
            results: 解析结果列表
            output_file: 输出文件名
        """
        if not results:
            return

        try:
            import csv
            # 在当前工作目录保存CSV文件
            output_path = os.path.join(os.getcwd(), output_file)
            with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['序号', 'ID', '主题', '文件路径'])
                for index, item in enumerate(results, 1):
                    writer.writerow([
                        index,
                        item['id'],
                        item['subject'],
                        item['path']
                    ])
            logger.info(f"结果已保存到 {output_path}")
            print(f"✓ 结果已保存到 CSV 文件: {output_path}")
        except Exception as e:
            logger.error(f"保存CSV文件时出错: {e}")


def main():
    """主函数"""
    import sys

    print("=" * 60)
    print("Metadata.json 解析器 v2.0")
    print("=" * 60)

    # 获取目标目录
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = input("\n请输入要扫描的目录路径 (直接回车使用当前目录): ").strip()
        if not target_dir:
            target_dir = '.'

    # 验证目录是否存在
    if not os.path.exists(target_dir):
        print(f"\n错误: 目录不存在 - {target_dir}")
        return

    if not os.path.isdir(target_dir):
        print(f"\n错误: 路径不是目录 - {target_dir}")
        return

    # 显示绝对路径
    abs_path = os.path.abspath(target_dir)
    print(f"\n扫描目录: {abs_path}")

    start_time = time.time()

    # 创建解析器实例
    parser = MetadataParser(max_workers=4, max_file_size=10 * 1024 * 1024)

    # 查找所有metadata.json文件
    print("\n正在扫描目录...")
    metadata_files = parser.find_metadata_files(target_dir)
    print(f"找到 {len(metadata_files)} 个 metadata.json 文件")

    if not metadata_files:
        print("未找到任何metadata.json文件")
        return

    # 解析所有文件
    print("\n正在解析文件...")
    results = parser.parse_all_files(metadata_files)

    # 按ID排序（如果ID是数字）
    try:
        results.sort(key=lambda x: int(x['id']) if str(x['id']).isdigit() else x['id'])
    except Exception:
        pass

    # 打印表格
    parser.print_table(results)

    # 保存到Excel
    parser.save_to_excel(results)

    # 显示性能统计
    elapsed_time = time.time() - start_time
    print(f"\n执行时间: {elapsed_time:.2f} 秒")
    print(f"平均处理速度: {len(metadata_files) / elapsed_time:.2f} 文件/秒")
    print(f"成功解析: {len(results)}/{len(metadata_files)} 个文件")

    logger.info(f"解析完成: {len(results)}/{len(metadata_files)} 成功")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        print(f"\n程序出错: {e}")