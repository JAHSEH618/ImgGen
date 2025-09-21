import os
import subprocess
from pathlib import Path
from moviepy import VideoFileClip


def convert_mp4_to_mp3_moviepy(input_path, output_path=None, bitrate="320k"):
    """
    使用MoviePy库将MP4转换为高质量MP3

    Args:
        input_path (str): 输入MP4文件路径
        output_path (str): 输出MP3文件路径（可选）
        bitrate (str): 音频比特率，默认320k（高质量）
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    # 如果没有指定输出路径，则自动生成
    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.with_suffix('.mp3'))

    try:
        # 加载视频文件
        video_clip = VideoFileClip(input_path)

        # 提取音频
        audio_clip = video_clip.audio

        # 保存为MP3（高质量）
        audio_clip.write_audiofile(
            output_path,
            bitrate=bitrate,
            verbose=False,
            logger=None
        )

        # 释放资源
        audio_clip.close()
        video_clip.close()

        print(f"转换成功: {input_path} -> {output_path}")
        return output_path

    except Exception as e:
        print(f"转换失败: {str(e)}")
        return None


def convert_mp4_to_mp3_ffmpeg(input_path, output_path=None, bitrate="320k", sample_rate=48000):
    """
    使用FFmpeg命令行工具进行高质量转换（需要安装FFmpeg）

    Args:
        input_path (str): 输入MP4文件路径
        output_path (str): 输出MP3文件路径（可选）
        bitrate (str): 音频比特率
        sample_rate (int): 采样率，48000Hz为高质量
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.with_suffix('.mp3'))

    try:
        # FFmpeg命令：高质量转换参数
        cmd = [
            'ffmpeg',
            '-i', input_path,  # 输入文件
            '-vn',  # 不包含视频流
            '-acodec', 'libmp3lame',  # 使用LAME MP3编码器
            '-ab', bitrate,  # 音频比特率
            '-ar', str(sample_rate),  # 采样率
            '-ac', '2',  # 双声道
            '-f', 'mp3',  # 输出格式
            '-y',  # 覆盖已存在文件
            output_path
        ]

        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"FFmpeg转换成功: {input_path} -> {output_path}")
            return output_path
        else:
            print(f"FFmpeg转换失败: {result.stderr}")
            return None

    except FileNotFoundError:
        print("错误: 未找到FFmpeg，请确保已安装FFmpeg并添加到PATH")
        return None
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return None


def batch_convert_mp4_to_mp3(input_folder, output_folder=None, method="moviepy", bitrate="320k"):
    """
    批量转换文件夹中的所有MP4文件

    Args:
        input_folder (str): 输入文件夹路径
        output_folder (str): 输出文件夹路径（可选）
        method (str): 转换方法 "moviepy" 或 "ffmpeg"
        bitrate (str): 音频比特率
    """
    input_path = Path(input_folder)

    if not input_path.exists():
        print(f"输入文件夹不存在: {input_folder}")
        return

    # 设置输出文件夹
    if output_folder is None:
        output_path = input_path / "converted_mp3"
    else:
        output_path = Path(output_folder)

    output_path.mkdir(exist_ok=True)

    # 查找所有MP4文件
    mp4_files = list(input_path.glob("*.mp4")) + list(input_path.glob("*.MP4"))

    if not mp4_files:
        print("未找到MP4文件")
        return

    print(f"找到 {len(mp4_files)} 个MP4文件，开始批量转换...")

    success_count = 0
    for mp4_file in mp4_files:
        output_file = output_path / (mp4_file.stem + ".mp3")

        print(f"正在转换: {mp4_file.name}")

        if method.lower() == "ffmpeg":
            result = convert_mp4_to_mp3_ffmpeg(str(mp4_file), str(output_file), bitrate)
        else:
            result = convert_mp4_to_mp3_moviepy(str(mp4_file), str(output_file), bitrate)

        if result:
            success_count += 1

    print(f"批量转换完成: {success_count}/{len(mp4_files)} 个文件转换成功")


def get_audio_info(file_path):
    """
    获取音频文件的详细信息
    """
    try:
        if file_path.endswith('.mp4'):
            clip = VideoFileClip(file_path)
            audio = clip.audio
            duration = audio.duration
            fps = audio.fps
            clip.close()
        else:
            from moviepy import AudioFileClip
            audio = AudioFileClip(file_path)
            duration = audio.duration
            fps = audio.fps
            audio.close()

        print(f"文件: {file_path}")
        print(f"时长: {duration:.2f} 秒")
        print(f"采样率: {fps} Hz")

    except Exception as e:
        print(f"无法获取文件信息: {str(e)}")


# 使用示例
if __name__ == "__main__":
    # 单个文件转换示例
    input_file = "/Users/okonma/Downloads/lin.mp4"

    # 方法1: 使用MoviePy（推荐，无需额外安装）
    print("=== 使用MoviePy转换 ===")
    convert_mp4_to_mp3_moviepy(
        input_file,
        "output_moviepy.mp3",
        bitrate="320k"  # 高质量比特率
    )

    # 方法2: 使用FFmpeg（需要安装FFmpeg）
    print("\n=== 使用FFmpeg转换 ===")
    convert_mp4_to_mp3_ffmpeg(
        input_file,
        "output_ffmpeg.mp3",
        bitrate="320k",
        sample_rate=24000  # 高采样率
    )

    # 批量转换示例
    print("\n=== 批量转换 ===")
    batch_convert_mp4_to_mp3(
        input_folder="./videos",
        output_folder="./audio_output",
        method="moviepy",
        bitrate="320k"
    )

    # 查看转换后的音频信息
    print("\n=== 音频信息 ===")
    get_audio_info("output_moviepy.mp3")