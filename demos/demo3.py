import os
import subprocess


def convert_quicktime_to_mp3(input_file, output_file=None, bitrate='192k'):
    """
    将QuickTime视频文件转换为MP3音频文件

    Args:
        input_file (str): 输入QuickTime文件路径
        output_file (str, optional): 输出MP3文件路径，如果不指定则自动生成
        bitrate (str, optional): 音频比特率，默认'192k'

    Returns:
        str: 输出文件路径
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")

    # 如果未指定输出文件名，则自动生成
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.mp3"

    # 使用FFmpeg进行转换
    cmd = [
        'ffmpeg',
        '-i', input_file,  # 输入文件
        '-vn',  # 不处理视频
        '-acodec', 'libmp3lame',  # 使用MP3编码器
        '-ab', bitrate,  # 音频比特率
        '-ar', '44100',  # 采样率
        '-y',  # 覆盖输出文件（如果存在）
        output_file  # 输出文件
    ]

    try:
        # 执行命令
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"转换成功: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")
        print(f"错误输出: {e.stderr.decode() if e.stderr else 'None'}")
        raise
    except FileNotFoundError:
        print("错误: 未找到FFmpeg。请确保已安装FFmpeg并添加到系统PATH中。")
        print("安装FFmpeg的方法:")
        print("  - macOS: brew install ffmpeg")
        print("  - Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  - Windows: 下载安装包并添加到PATH")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='将QuickTime视频转换为MP3音频')
    parser.add_argument('input', help='输入QuickTime文件路径')
    parser.add_argument('-o', '--output', help='输出MP3文件路径（可选）')
    parser.add_argument('-b', '--bitrate', default='192k', help='音频比特率（默认: 192k）')

    args = parser.parse_args()

    try:
        convert_quicktime_to_mp3(args.input, args.output, args.bitrate)
    except Exception as e:
        print(f"发生错误: {e}")