#!/usr/bin/env python3
"""
SVG 转 PNG 转换器 - 支持高分辨率输出
方案1: 使用 svglib + reportlab (纯Python，无需系统依赖)
依赖: pip install svglib reportlab pillow
"""

import os
import sys
from pathlib import Path

try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    from PIL import Image
except ImportError:
    print("错误: 缺少必要的库")
    print("请运行: pip install svglib reportlab pillow")
    sys.exit(1)


def svg_to_png_svglib(svg_path, output_path=None, scale=2.0, dpi=None):
    """
    使用 svglib 将SVG转换为PNG (纯Python方案)

    参数:
        svg_path: SVG文件路径
        output_path: 输出PNG文件路径
        scale: 分辨率倍数
        dpi: 输出DPI (如果指定，会覆盖scale)
    """
    if not os.path.exists(svg_path):
        raise FileNotFoundError(f"SVG文件不存在: {svg_path}")

    if output_path is None:
        svg_file = Path(svg_path)
        output_path = svg_file.with_suffix(f'.{int(scale)}x.png')

    # 读取SVG
    drawing = svg2rlg(svg_path)

    if drawing is None:
        raise ValueError(f"无法解析SVG文件: {svg_path}")

    # 计算输出尺寸
    original_width = drawing.width
    original_height = drawing.height

    # 应用缩放
    drawing.width = original_width * scale
    drawing.height = original_height * scale
    drawing.scale(scale, scale)

    # 转换为PNG
    if dpi:
        renderPM.drawToFile(drawing, str(output_path), fmt='PNG', dpi=dpi)
    else:
        # 使用更高的DPI以获得更好的质量
        effective_dpi = int(72 * scale)
        renderPM.drawToFile(drawing, str(output_path), fmt='PNG', dpi=effective_dpi)

    # 获取输出信息
    img = Image.open(output_path)
    width, height = img.size

    print(f"✅ 转换成功!")
    print(f"   输入: {svg_path}")
    print(f"   输出: {output_path}")
    print(f"   尺寸: {width} × {height} 像素")
    print(f"   倍数: {scale}x")

    return str(output_path)


def batch_convert(input_dir, output_dir=None, scale=2.0):
    """批量转换目录中的所有SVG文件"""
    input_path = Path(input_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"目录不存在: {input_dir}")

    if output_dir is None:
        output_path = input_path
    else:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

    svg_files = list(input_path.glob('*.svg'))

    if not svg_files:
        print(f"⚠️  在 {input_dir} 中没有找到SVG文件")
        return

    print(f"找到 {len(svg_files)} 个SVG文件")
    print(f"开始批量转换 ({scale}x)...\n")

    success_count = 0
    for svg_file in svg_files:
        try:
            output_file = output_path / f"{svg_file.stem}.{int(scale)}x.png"
            svg_to_png_svglib(svg_file, output_file, scale)
            success_count += 1
            print()
        except Exception as e:
            print(f"❌ 转换失败 {svg_file.name}: {e}\n")

    print(f"批量转换完成: {success_count}/{len(svg_files)} 成功")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='SVG转PNG转换器 - 支持高分辨率输出 (纯Python方案)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换单个文件 (2倍分辨率)
  python svg_to_png.py input.svg -s 2

  # 转换为4倍分辨率
  python svg_to_png.py input.svg -o output.png -s 4

  # 批量转换目录
  python svg_to_png.py -d ./svgs -s 3

  # 使用自定义DPI
  python svg_to_png.py input.svg --dpi 300
        """
    )

    parser.add_argument('input', nargs='?', help='输入SVG文件路径')
    parser.add_argument('-o', '--output', help='输出PNG文件路径')
    parser.add_argument('-s', '--scale', type=float, default=2.0,
                        help='分辨率倍数 (默认: 2.0)')
    parser.add_argument('--dpi', type=int, help='输出DPI (覆盖scale参数)')
    parser.add_argument('-d', '--directory', help='批量转换目录')
    parser.add_argument('--output-dir', help='批量转换输出目录')

    args = parser.parse_args()

    try:
        if args.directory:
            batch_convert(args.directory, args.output_dir, args.scale)
        elif args.input:
            svg_to_png_svglib(args.input, args.output, args.scale, args.dpi)
        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()