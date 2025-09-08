import cairosvg
from PIL import Image
import io
import os


def svg_to_uhd_png(svg_path, output_path, scale=8, background_color='white'):
    """
    将SVG转换为超高清PNG图片

    参数:
    svg_path: SVG文件路径
    output_path: 输出PNG文件路径
    scale: 缩放倍数 (默认8倍，生成超高清图片)
    background_color: 背景颜色 (默认白色)
    """

    try:
        # 读取SVG文件
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()

        # 使用cairosvg将SVG转换为PNG字节流
        # 设置较高的DPI来获得超高清效果
        png_bytes = cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            dpi=300 * scale,  # 高DPI设置
            output_width=None,  # 自动计算宽度
            output_height=None  # 自动计算高度
        )

        # 使用PIL处理图像
        image = Image.open(io.BytesIO(png_bytes))

        # 如果图像是RGBA模式，需要处理透明背景
        if image.mode in ('RGBA', 'LA', 'P'):
            # 创建白色背景
            background = Image.new('RGB', image.size, background_color)
            if image.mode == 'P':
                image = image.convert('RGBA')

            # 将原图像粘贴到白色背景上
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background

        # 保存为PNG
        image.save(output_path, 'PNG', quality=100, optimize=True)

        print(f"✅ 转换成功!")
        print(f"📁 输入文件: {svg_path}")
        print(f"📁 输出文件: {output_path}")
        print(f"📏 图片尺寸: {image.size[0]} x {image.size[1]} 像素")
        print(f"🔍 缩放倍数: {scale}x")

    except FileNotFoundError:
        print(f"❌ 错误: 找不到SVG文件 '{svg_path}'")
    except Exception as e:
        print(f"❌ 转换过程中发生错误: {str(e)}")


def batch_convert_svg_to_png(input_folder, output_folder, scale=8):
    """
    批量转换文件夹中的所有SVG文件

    参数:
    input_folder: 包含SVG文件的输入文件夹
    output_folder: PNG文件输出文件夹
    scale: 缩放倍数
    """

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    svg_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.svg')]

    if not svg_files:
        print(f"❌ 在文件夹 '{input_folder}' 中没有找到SVG文件")
        return

    print(f"🔄 开始批量转换 {len(svg_files)} 个SVG文件...")

    for svg_file in svg_files:
        svg_path = os.path.join(input_folder, svg_file)
        png_file = os.path.splitext(svg_file)[0] + '.png'
        output_path = os.path.join(output_folder, png_file)

        print(f"\n正在处理: {svg_file}")
        svg_to_uhd_png(svg_path, output_path, scale)

    print(f"\n🎉 批量转换完成!")


def create_test_svg():
    """创建一个测试用的SVG文件"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="200" fill="#f0f0f0" stroke="#ccc" stroke-width="2"/>
  <circle cx="100" cy="100" r="80" fill="#4CAF50" opacity="0.8"/>
  <text x="100" y="110" font-family="Arial" font-size="16" text-anchor="middle" fill="white">
    测试SVG
  </text>
  <polygon points="50,150 150,150 100,50" fill="#2196F3" opacity="0.6"/>
</svg>'''

    with open('test.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print("✅ 已创建测试SVG文件: test.svg")


# 使用示例
if __name__ == "__main__":
    print("=== SVG转超高清PNG转换器 (CairoSVG版本) ===")
    print()
    print("📦 macOS安装步骤:")
    print("1. brew install cairo pango gdk-pixbuf libffi")
    print("2. pip install cairosvg Pillow")
    print()
    print("如果遇到问题，可以尝试:")
    print("brew install pkg-config cairo pango gdk-pixbuf libffi libxml2")
    print("export PKG_CONFIG_PATH=\"/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH\"")
    print("pip install --no-cache-dir cairosvg")
    print()
    print("=" * 60)
    print()

    # 创建测试SVG文件
    create_test_svg()

    # 单个文件转换示例
    svg_file = "test.svg"  # 使用创建的测试文件
    png_file = "output_uhd.png"  # 输出PNG文件路径

    if os.path.exists(svg_file):
        print("🔄 开始转换测试文件...")
        svg_to_uhd_png(svg_file, png_file, scale=10)  # 8倍缩放，超高清
        print()
        print("💡 您可以修改 svg_file 变量为您自己的SVG文件路径")

    print("\n" + "=" * 60)

    # 批量转换示例
    input_folder = "svg_files"  # SVG文件所在文件夹
    output_folder = "png_output"  # PNG输出文件夹

    print(f"💡 批量转换使用说明:")
    print(f"1. 创建文件夹: {input_folder}")
    print(f"2. 将SVG文件放入该文件夹")
    print(f"3. 取消下面代码的注释运行批量转换")
    print()

    # 取消注释以启用批量转换
    # if os.path.exists(input_folder):
    #     batch_convert_svg_to_png(input_folder, output_folder, scale=6)
    # else:
    #     print(f"请先创建文件夹: {input_folder}")

    print("📝 使用说明:")
    print("1. 确保已安装所有依赖 (见上方安装步骤)")
    print("2. 修改 svg_file 变量为您的SVG文件路径")
    print("3. 运行脚本即可获得超高清PNG文件")
    print("4. scale参数控制清晰度:")
    print("   - scale=4: 4倍缩放，适合一般用途")
    print("   - scale=6: 6倍缩放，高清")
    print("   - scale=8: 8倍缩放，超高清")
    print("   - scale=10: 10倍缩放，极高清 (文件较大)")
    print()
    print("🎯 输出效果:")
    print("- scale=8 + DPI=2400 = 超高清PNG")
    print("- 自动白色背景处理")
    print("- PNG格式，质量100%，文件优化")