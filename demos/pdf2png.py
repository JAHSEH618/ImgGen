#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF转PNG转换器
支持单个PDF文件转换为多个PNG图片，每页一个PNG文件
"""

import os
import sys
import io
from pathlib import Path

try:
    import fitz  # PyMuPDF
    from PIL import Image
except ImportError as e:
    print(f"缺少必要的库: {e}")
    print("请安装所需库:")
    print("pip install PyMuPDF Pillow")
    sys.exit(1)


def pdf_to_png(pdf_path, output_dir=None, dpi=150, image_format='PNG'):
    """
    将PDF文件转换为PNG图片

    参数:
    pdf_path: PDF文件路径
    output_dir: 输出目录，默认为PDF文件同目录下的同名文件夹
    dpi: 图片分辨率，默认150
    image_format: 输出格式，默认PNG

    返回:
    转换成功的图片文件路径列表
    """
    try:
        # 验证PDF文件存在
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

        # 设置输出目录
        if output_dir is None:
            output_dir = pdf_path.parent / pdf_path.stem
        else:
            output_dir = Path(output_dir)

        # 创建输出目录
        output_dir.mkdir(parents=True, exist_ok=True)

        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)
        image_paths = []

        print(f"开始转换PDF: {pdf_path.name}")
        print(f"总页数: {len(pdf_document)}")
        print(f"输出目录: {output_dir}")
        print(f"分辨率: {dpi} DPI")

        # 转换每一页
        for page_num in range(len(pdf_document)):
            # 获取页面
            page = pdf_document[page_num]

            # 设置转换矩阵（控制分辨率）
            zoom = dpi / 72  # 72是PDF的默认DPI
            mat = fitz.Matrix(zoom, zoom)

            # 渲染页面为图片
            pix = page.get_pixmap(matrix=mat)

            # 生成输出文件名
            output_filename = f"{pdf_path.stem}_page_{page_num + 1:03d}.png"
            output_path = output_dir / output_filename

            # 保存图片
            pix.save(output_path)
            image_paths.append(str(output_path))

            print(f"已转换第 {page_num + 1} 页 -> {output_filename}")

        # 关闭PDF文件
        pdf_document.close()

        print(f"\n转换完成！共生成 {len(image_paths)} 个PNG文件")
        return image_paths

    except Exception as e:
        print(f"转换过程中出现错误: {e}")
        return []


def pdf_to_long_png(pdf_path, output_path=None, dpi=150):
    """
    将PDF文件转换为一张长PNG图片（所有页面垂直拼接）

    参数:
    pdf_path: PDF文件路径
    output_path: 输出PNG文件路径，默认为PDF文件同目录下的同名PNG文件
    dpi: 图片分辨率，默认150

    返回:
    转换成功的图片文件路径
    """
    try:
        # 验证PDF文件存在
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

        # 设置输出路径
        if output_path is None:
            output_path = pdf_path.parent / f"{pdf_path.stem}_long.png"
        else:
            output_path = Path(output_path)

        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)
        
        print(f"开始转换PDF: {pdf_path.name}")
        print(f"总页数: {len(pdf_document)}")
        print(f"分辨率: {dpi} DPI")

        # 设置转换矩阵（控制分辨率）
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)

        # 收集所有页面的图片数据
        page_images = []
        total_height = 0
        max_width = 0

        # 转换每一页并收集尺寸信息
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap(matrix=mat)
            
            # 将pixmap转换为PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            page_images.append(img)
            total_height += img.height
            max_width = max(max_width, img.width)
            
            print(f"已处理第 {page_num + 1} 页")

        # 创建长图画布
        long_image = Image.new('RGB', (max_width, total_height), 'white')

        # 将所有页面拼接到长图上
        current_y = 0
        for i, img in enumerate(page_images):
            # 如果页面宽度小于最大宽度，居中放置
            x_offset = (max_width - img.width) // 2
            long_image.paste(img, (x_offset, current_y))
            current_y += img.height
            print(f"已拼接第 {i + 1} 页")

        # 保存长图
        long_image.save(output_path)
        
        # 关闭PDF文件
        pdf_document.close()

        print(f"\n转换完成！生成长PNG图片: {output_path}")
        print(f"图片尺寸: {max_width} x {total_height} 像素")
        return str(output_path)

    except Exception as e:
        print(f"转换过程中出现错误: {e}")
        return None


def batch_pdf_to_png(input_dir, output_dir=None, dpi=150):
    """
    批量转换目录下的所有PDF文件

    参数:
    input_dir: 包含PDF文件的目录
    output_dir: 输出根目录
    dpi: 图片分辨率
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"输入目录不存在: {input_dir}")
        return

    # 查找所有PDF文件
    pdf_files = list(input_path.glob("*.pdf")) + list(input_path.glob("*.PDF"))

    if not pdf_files:
        print(f"在目录 {input_dir} 中没有找到PDF文件")
        return

    print(f"找到 {len(pdf_files)} 个PDF文件")

    # 转换每个PDF文件
    for pdf_file in pdf_files:
        if output_dir:
            file_output_dir = Path(output_dir) / pdf_file.stem
        else:
            file_output_dir = None

        print(f"\n{'=' * 50}")
        pdf_to_png(pdf_file, file_output_dir, dpi)


def main():
    """主函数 - 提供命令行接口"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("1. 转换单个PDF文件为多个PNG:")
        print("   python pdf_to_png.py <pdf_file_path> [output_dir] [dpi]")
        print("2. 转换单个PDF文件为一张长PNG:")
        print("   python pdf_to_png.py --long <pdf_file_path> [output_path] [dpi]")
        print("3. 批量转换目录下的PDF文件:")
        print("   python pdf_to_png.py --batch <input_dir> [output_dir] [dpi]")
        print("\n示例:")
        print("   python pdf_to_png.py document.pdf")
        print("   python pdf_to_png.py --long document.pdf ./output.png 300")
        print("   python pdf_to_png.py document.pdf ./images 300")
        print("   python pdf_to_png.py --batch ./pdfs ./output 200")
        return

    # 长PNG模式
    if sys.argv[1] == '--long':
        if len(sys.argv) < 3:
            print("长PNG模式需要指定PDF文件")
            return

        pdf_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else None
        dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 150

        pdf_to_long_png(pdf_path, output_path, dpi)

    # 批量处理模式
    elif sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("批量模式需要指定输入目录")
            return

        input_dir = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 150

        batch_pdf_to_png(input_dir, output_dir, dpi)

    # 单文件处理模式
    else:
        pdf_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150

        pdf_to_png(pdf_path, output_dir, dpi)


# 使用示例
if __name__ == "__main__":
    # 如果直接运行脚本，执行命令行模式
    if len(sys.argv) > 1:
        main()
    else:
        pdf_to_long_png('/Users/okonma/Downloads/四层商业模式.pdf', '/Users/okonma/Downloads/四层商业模式.png', dpi=400)