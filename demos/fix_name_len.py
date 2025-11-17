#!/usr/bin/env python3
"""
批量处理过长的文件路径和文件名
确保文件名不超过255字符，路径不超过4096字符

安全特性：
- 只在预览模式下默认运行
- 需要明确 --execute 参数才会修改文件
- 完整的错误处理
- 避免符号链接循环
- 验证路径安全性
"""
import os
import re
import sys
from pathlib import Path

# 系统限制
MAX_FILENAME_LENGTH = 200  # 文件名安全长度（低于255）
MAX_PATH_LENGTH = 3500  # 路径安全长度（低于4096）


def is_safe_path(path):
    """检查路径是否安全（避免符号链接、特殊路径等）"""
    try:
        # 获取绝对路径
        abs_path = os.path.abspath(path)

        # 检查是否是符号链接
        if os.path.islink(path):
            return False

        # 检查路径是否存在
        if not os.path.exists(path):
            return False

        return True
    except Exception:
        return False


def shorten_name(name, is_file=True, max_length=50):
    """缩短过长的名称 - 安全版本"""
    if len(name) <= max_length:
        return name

    # 防止空名称
    if not name or name in ['.', '..']:
        return name

    # 尝试提取5-6位数字
    match = re.match(r'^(\d{5,6})_', name)

    if match:
        number = match.group(1)
        if is_file:
            ext = Path(name).suffix
            # 确保扩展名不会太长
            if len(ext) > 20:
                ext = ext[:20]
            return f"{number}{ext}"
        else:
            return number
    else:
        # 没有数字模式，智能截断
        if is_file:
            ext = Path(name).suffix
            # 确保扩展名不会太长
            if len(ext) > 20:
                ext = ext[:20]
            # 确保有足够空间给扩展名
            base_max = max(10, max_length - len(ext) - 5)
            base = Path(name).stem[:base_max]
            # 移除可能的危险字符
            base = re.sub(r'[^\w\-.]', '_', base)
            return f"{base}{ext}"
        else:
            truncated = name[:max_length]
            # 移除可能的危险字符
            truncated = re.sub(r'[^\w\-.]', '_', truncated)
            return truncated


def get_safe_new_name(directory, old_name, new_name):
    """获取不冲突的新名称 - 安全版本"""
    # 防止空名称和特殊名称
    if not new_name or new_name in ['.', '..']:
        return None

    # 防止路径遍历攻击
    if '/' in new_name or '\\' in new_name:
        new_name = new_name.replace('/', '_').replace('\\', '_')

    new_path = os.path.join(directory, new_name)

    # 如果不存在冲突，直接返回
    if not os.path.exists(new_path) or os.path.samefile(os.path.join(directory, old_name), new_path):
        return new_name

    # 处理重名，最多尝试1000次
    base, ext = os.path.splitext(new_name) if '.' in new_name else (new_name, '')

    for counter in range(1, 1001):
        if ext:
            candidate = f"{base}_{counter}{ext}"
        else:
            candidate = f"{base}_{counter}"

        candidate_path = os.path.join(directory, candidate)
        if not os.path.exists(candidate_path):
            return candidate

    # 如果1000次都冲突，返回None表示失败
    return None


def calculate_needed_length(path, name, is_file=True):
    """计算路径需要缩短的长度"""
    full_path = os.path.join(path, name)
    current_length = len(full_path)
    name_length = len(name)

    problems = []

    # 检查文件名长度
    if name_length > MAX_FILENAME_LENGTH:
        problems.append(f"文件名过长: {name_length} > {MAX_FILENAME_LENGTH}")

    # 检查路径长度
    if current_length > MAX_PATH_LENGTH:
        problems.append(f"路径过长: {current_length} > {MAX_PATH_LENGTH}")
        # 计算需要缩短多少
        excess = current_length - MAX_PATH_LENGTH
        max_name_length = max(10, name_length - excess - 50)  # 额外留50字符余量
        return problems, max_name_length

    if name_length > MAX_FILENAME_LENGTH:
        return problems, MAX_FILENAME_LENGTH

    return problems, name_length


def process_directory(path, depth=0, dry_run=True, visited=None):
    """递归处理目录 - 安全版本"""
    # 防止无限递归
    if depth > 50:
        print(f"{'  ' * depth}⚠️  目录层级过深，跳过: {path}")
        return

    # 防止符号链接循环
    if visited is None:
        visited = set()

    try:
        real_path = os.path.realpath(path)
        if real_path in visited:
            print(f"{'  ' * depth}⚠️  检测到循环引用，跳过: {path}")
            return
        visited.add(real_path)
    except Exception as e:
        print(f"{'  ' * depth}⚠️  无法解析路径: {path} - {e}")
        return

    # 检查路径安全性
    if not is_safe_path(path):
        print(f"{'  ' * depth}⚠️  不安全的路径，跳过: {path}")
        return

    indent = "  " * depth

    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        print(f"{indent}⚠️  无权限访问: {path}")
        return
    except Exception as e:
        print(f"{indent}⚠️  错误: {path} - {e}")
        return

    # 分离文件和文件夹
    files = []
    dirs = []

    for item in items:
        # 跳过特殊文件
        if item in ['.', '..', '.DS_Store', 'Thumbs.db']:
            continue

        item_path = os.path.join(path, item)

        try:
            if os.path.isfile(item_path) and not os.path.islink(item_path):
                files.append(item)
            elif os.path.isdir(item_path) and not os.path.islink(item_path):
                dirs.append(item)
        except Exception:
            continue

    # 先处理文件
    for filename in files:
        file_path = os.path.join(path, filename)
        problems, max_length = calculate_needed_length(path, filename, is_file=True)

        if problems:
            new_name = shorten_name(filename, is_file=True, max_length=max_length)

            if not new_name:
                print(f"{indent}❌ 无法生成安全的文件名: {filename}")
                continue

            new_name = get_safe_new_name(path, filename, new_name)

            if not new_name:
                print(f"{indent}❌ 无法解决命名冲突: {filename}")
                continue

            new_path = os.path.join(path, new_name)

            print(f"{indent}📄 文件: {filename}")
            for problem in problems:
                print(f"{indent}   ⚠️  {problem}")
            print(f"{indent}   ➜  {new_name}")
            print(f"{indent}   原路径长度: {len(file_path)}, 新路径长度: {len(new_path)}")

            if not dry_run:
                try:
                    # 再次确认源文件存在
                    if not os.path.exists(file_path):
                        print(f"{indent}   ❌ 源文件不存在")
                        continue

                    # 确认目标路径不存在或是同一文件
                    if os.path.exists(new_path) and not os.path.samefile(file_path, new_path):
                        print(f"{indent}   ❌ 目标路径已存在")
                        continue

                    os.rename(file_path, new_path)
                    print(f"{indent}   ✅ 已重命名")
                except Exception as e:
                    print(f"{indent}   ❌ 重命名失败: {e}")
            print()

    # 再处理文件夹（从最深层开始）
    for dirname in dirs:
        dir_path = os.path.join(path, dirname)

        # 先递归处理子目录
        process_directory(dir_path, depth + 1, dry_run, visited)

        # 然后处理当前文件夹名
        problems, max_length = calculate_needed_length(path, dirname, is_file=False)

        if problems:
            new_name = shorten_name(dirname, is_file=False, max_length=max_length)

            if not new_name:
                print(f"{indent}❌ 无法生成安全的文件夹名: {dirname}")
                continue

            new_name = get_safe_new_name(path, dirname, new_name)

            if not new_name:
                print(f"{indent}❌ 无法解决命名冲突: {dirname}")
                continue

            new_path = os.path.join(path, new_name)

            print(f"{indent}📁 文件夹: {dirname}")
            for problem in problems:
                print(f"{indent}   ⚠️  {problem}")
            print(f"{indent}   ➜  {new_name}")
            print(f"{indent}   原路径长度: {len(dir_path)}, 新路径长度: {len(new_path)}")

            if not dry_run:
                try:
                    # 再次确认源目录存在
                    if not os.path.exists(dir_path):
                        print(f"{indent}   ❌ 源目录不存在")
                        continue

                    # 确认目标路径不存在或是同一目录
                    if os.path.exists(new_path) and not os.path.samefile(dir_path, new_path):
                        print(f"{indent}   ❌ 目标路径已存在")
                        continue

                    os.rename(dir_path, new_path)
                    print(f"{indent}   ✅ 已重命名")
                except Exception as e:
                    print(f"{indent}   ❌ 重命名失败: {e}")
            print()


def main():
    print("=" * 60)
    print("批量处理过长路径工具 (安全版本)")
    print("=" * 60)
    print(f"文件名最大长度: {MAX_FILENAME_LENGTH}")
    print(f"路径最大长度: {MAX_PATH_LENGTH}")
    print()

    # 检查参数
    dry_run = True
    start_path = "."

    if len(sys.argv) > 1:
        if sys.argv[1] == "--execute":
            # 需要二次确认
            print("⚠️  警告：即将执行实际重命名操作！")
            print("   这将修改您的文件系统")
            print()
            confirm = input("请输入 'YES' 确认执行（其他输入取消）: ")

            if confirm != "YES":
                print("❌ 操作已取消")
                return

            dry_run = False
            print("✅ 确认执行模式")

            if len(sys.argv) > 2:
                start_path = sys.argv[2]
        elif sys.argv[1] == "--help":
            print("用法:")
            print("  python3 script.py                    # 预览模式（不实际修改）")
            print("  python3 script.py --execute          # 执行模式（需要确认）")
            print("  python3 script.py /path              # 指定路径预览")
            print("  python3 script.py --execute /path    # 指定路径执行")
            print()
            print("安全特性:")
            print("  - 默认预览模式，不会修改文件")
            print("  - 执行模式需要输入 'YES' 二次确认")
            print("  - 自动跳过符号链接")
            print("  - 防止路径遍历攻击")
            print("  - 限制递归深度防止无限循环")
            print("  - 完整的错误处理")
            return
        else:
            start_path = sys.argv[1]
            if len(sys.argv) > 2 and sys.argv[2] == "--execute":
                print("⚠️  警告：即将执行实际重命名操作！")
                confirm = input("请输入 'YES' 确认执行: ")
                if confirm != "YES":
                    print("❌ 操作已取消")
                    return
                dry_run = False
    else:
        print("🔍 预览模式：不会实际修改文件")
        print("   运行 'python3 script.py --execute' 执行实际重命名")

    print()

    # 验证起始路径
    if not os.path.exists(start_path):
        print(f"❌ 错误：路径不存在: {start_path}")
        return

    if not os.path.isdir(start_path):
        print(f"❌ 错误：不是目录: {start_path}")
        return

    abs_path = os.path.abspath(start_path)
    print(f"处理路径: {abs_path}")
    print("-" * 60)
    print()

    try:
        process_directory(start_path, dry_run=dry_run)
    except KeyboardInterrupt:
        print()
        print("⚠️  用户中断操作")
        return
    except Exception as e:
        print()
        print(f"❌ 发生错误: {e}")
        return

    print("-" * 60)
    if dry_run:
        print("✅ 预览完成！")
        print("   运行 'python3 script.py --execute' 执行实际重命名")
        print("   （需要输入 'YES' 确认）")
    else:
        print("✅ 处理完成！")


if __name__ == "__main__":
    main()