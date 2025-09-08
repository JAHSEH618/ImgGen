import mimetypes
import os
import magic  # 需要安装python-magic库: pip install python-magic


def get_mime_type(file_path):
    """
    获取文件的MIME类型，使用多种方法以确保准确性

    Args:
        file_path: 文件路径

    Returns:
        str: 文件的MIME类型
    """
    if not os.path.exists(file_path):
        return "文件不存在"

    # 方法1: 使用mimetypes模块(基于文件扩展名)
    mime_type_by_extension = mimetypes.guess_type(file_path)[0]

    # 方法2: 使用python-magic库(基于文件内容)
    try:
        mime_type_by_content = magic.Magic(mime=True).from_file(file_path)
    except Exception as e:
        mime_type_by_content = f"无法检测文件内容: {str(e)}"

    return {
        "文件路径": file_path,
        "文件大小": f"{os.path.getsize(file_path) / 1024:.2f} KB",
        "基于扩展名的MIME类型": mime_type_by_extension or "未知",
        "基于文件内容的MIME类型": mime_type_by_content or "未知"
    }


def main():
    """
    主函数，获取用户输入并显示文件的MIME类型
    """
    file_path = '/Users/okonma/Downloads/dz2.mp3'

    result = get_mime_type(file_path)

    # 打印结果
    print("\n文件MIME类型信息:")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    # 确保mimetypes数据库已初始化
    mimetypes.init()
    main()