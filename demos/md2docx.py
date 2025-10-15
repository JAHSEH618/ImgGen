import re
import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import markdown
from bs4 import BeautifulSoup


def parse_markdown_to_docx(md_file_path, output_docx_path=None):
    """
    将Markdown文件转换为DOCX文档，支持图片嵌入

    参数:
        md_file_path: Markdown文件路径
        output_docx_path: 输出的DOCX文件路径（可选，默认与md文件同名）
    """
    # 读取Markdown文件
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 获取Markdown文件所在目录
    md_dir = Path(md_file_path).parent
    md_name = Path(md_file_path).stem

    # 图片目录（与md文件同名的文件夹）
    img_dir = md_dir / f"{md_name}"

    # 设置输出路径
    if output_docx_path is None:
        output_docx_path = md_dir / f"{md_name}.docx"

    # 创建Word文档
    doc = Document()

    # 分割Markdown内容为行
    lines = md_content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # 处理标题
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            title_text = line.lstrip('#').strip()
            heading = doc.add_heading(title_text, level=min(level, 9))

        # 处理图片 ![alt](image_path)
        elif '![' in line:
            img_matches = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', line)
            for alt_text, img_path in img_matches:
                # 处理图片路径
                # 如果是相对路径，需要结合md文件目录
                if not os.path.isabs(img_path):
                    # 处理URL编码的路径
                    img_path = img_path.replace('%20', ' ')

                    # 尝试多种可能的路径
                    possible_paths = [
                        md_dir / img_path,  # 相对于md文件的路径
                        img_dir / Path(img_path).name,  # 图片文件夹中的文件名
                        md_dir / Path(img_path).name,  # md文件夹中的文件名
                    ]

                    img_full_path = None
                    for p in possible_paths:
                        if p.exists():
                            img_full_path = p
                            break
                else:
                    img_full_path = Path(img_path)

                # 插入图片
                if img_full_path and img_full_path.exists():
                    try:
                        # 添加图片，设置最大宽度为6英寸
                        paragraph = doc.add_paragraph()
                        run = paragraph.add_run()
                        run.add_picture(str(img_full_path), width=Inches(6))
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

                        # 如果有alt文本，添加为图片说明
                        if alt_text:
                            caption = doc.add_paragraph(alt_text)
                            caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            caption.runs[0].font.size = Pt(9)
                            caption.runs[0].italic = True
                    except Exception as e:
                        # 如果图片插入失败，添加错误信息
                        doc.add_paragraph(f"[图片加载失败: {img_path}]")
                        print(f"警告: 无法插入图片 {img_path}: {e}")
                else:
                    doc.add_paragraph(f"[图片未找到: {img_path}]")
                    print(f"警告: 图片未找到 {img_path}")

        # 处理代码块
        elif line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1

            code_text = '\n'.join(code_lines)
            code_para = doc.add_paragraph(code_text)
            code_para.style = 'List Number'  # 使用等宽字体样式
            for run in code_para.runs:
                run.font.name = 'Courier New'
                run.font.size = Pt(9)

        # 处理列表
        elif line.startswith('- ') or line.startswith('* '):
            list_text = line[2:].strip()
            doc.add_paragraph(list_text, style='List Bullet')

        elif re.match(r'^\d+\.\s', line):
            list_text = re.sub(r'^\d+\.\s', '', line).strip()
            doc.add_paragraph(list_text, style='List Number')

        # 处理普通段落
        elif line:
            # 处理行内格式（粗体、斜体等）
            paragraph = doc.add_paragraph()

            # 简单的粗体和斜体处理
            parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = paragraph.add_run(part[2:-2])
                    run.bold = True
                elif part.startswith('*') and part.endswith('*'):
                    run = paragraph.add_run(part[1:-1])
                    run.italic = True
                elif part.startswith('`') and part.endswith('`'):
                    run = paragraph.add_run(part[1:-1])
                    run.font.name = 'Courier New'
                else:
                    paragraph.add_run(part)

        i += 1

    # 保存文档
    doc.save(output_docx_path)
    print(f"✓ 转换完成: {output_docx_path}")
    return output_docx_path


# 使用示例
if __name__ == "__main__":
    # 设置你的Markdown文件路径
    md_file = "/Users/okonma/Downloads/w/Whatmore 26cb851bd74d80588d73fc5553ac4421.md"

    # 转换
    # parse_markdown_to_docx(md_file)

    # 也可以指定输出路径
    parse_markdown_to_docx(md_file, "/Users/okonma/Downloads/my_document.docx")