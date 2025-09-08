import os
from moviepy import VideoFileClip
import argparse


def extract_audio_from_mp4(input_file, output_file=None):
    """
    从MP4文件中提取音频并保存为MP3

    参数:
    input_file (str): 输入的MP4文件路径
    output_file (str): 输出的MP3文件路径，如果为None则自动生成
    """
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            print(f"错误: 文件 {input_file} 不存在")
            return False

        # 如果没有指定输出文件名，自动生成
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.mp3"

        print(f"正在处理: {input_file}")

        # 加载视频文件
        video = VideoFileClip(input_file)

        # 提取音频
        audio = video.audio

        # 保存为MP3
        audio.write_audiofile(output_file, codec='mp3')

        # 释放资源
        audio.close()
        video.close()

        print(f"成功转换: {output_file}")
        return True

    except Exception as e:
        print(f"转换失败: {str(e)}")
        return False


def batch_convert(input_folder, output_folder=None):
    """
    批量转换文件夹中的所有MP4文件

    参数:
    input_folder (str): 输入文件夹路径
    output_folder (str): 输出文件夹路径，如果为None则使用输入文件夹
    """
    if output_folder is None:
        output_folder = input_folder

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 获取所有MP4文件
    mp4_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mp4')]

    if not mp4_files:
        print("未找到MP4文件")
        return

    print(f"找到 {len(mp4_files)} 个MP4文件")

    # 批量转换
    for i, mp4_file in enumerate(mp4_files, 1):
        input_path = os.path.join(input_folder, mp4_file)
        output_name = os.path.splitext(mp4_file)[0] + '.mp3'
        output_path = os.path.join(output_folder, output_name)

        print(f"[{i}/{len(mp4_files)}] 正在处理: {mp4_file}")

        if extract_audio_from_mp4(input_path, output_path):
            print(f"✓ 完成: {output_name}")
        else:
            print(f"✗ 失败: {mp4_file}")


def main():
    parser = argparse.ArgumentParser(description='从MP4文件中提取音频并转换为MP3')
    parser.add_argument('input', help='输入的MP4文件或文件夹路径')
    parser.add_argument('-o', '--output', help='输出文件或文件夹路径')
    parser.add_argument('-b', '--batch', action='store_true', help='批量处理文件夹中的所有MP4文件')

    args = parser.parse_args()

    if args.batch:
        batch_convert(args.input, args.output)
    else:
        extract_audio_from_mp4(args.input, args.output)


if __name__ == "__main__":
    # 示例用法
    print("MP4 to MP3 音频提取器")
    print("=" * 30)

    # 单个文件转换示例
    input_file = "/Users/okonma/Downloads/1.mp4"  # 替换为你的MP4文件路径

    if os.path.exists(input_file):
        extract_audio_from_mp4(input_file)
    else:
        print("请修改 input_file 变量为你的MP4文件路径")

    # 也可以直接调用命令行参数
    # main()