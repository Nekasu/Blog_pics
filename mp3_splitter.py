# 该脚本用于将单个mp3文件分成多个片段, 以方便放入mp3中供游泳时听
# 要运行这个程序，需要1. pydub包， 2。 FFmpeg或avconv
# FFmpeg安装教程见https://blog.csdn.net/csdn_yudong/article/details/129182648
from fileinput import filename
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import os

def split_audio(file_path, output_dir, segment_minutes=4, trim_start=20, trim_end=10):
    """
    切割音频文件，去除开头和结尾的指定时长，并将剩余部分分段保存
    :param file_path: 输入文件路径
    :param output_dir: 输出目录
    :param segment_minutes: 每个片段的分钟数
    :param trim_start: 去除开头的秒数
    :param trim_end: 去除结尾的秒数
    """
    try:
        # 加载音频文件
        audio = AudioSegment.from_file(file_path)
        print(f"成功加载文件: {file_path}")
        file_name = file_path.split('/')[-1].split('.')[0]

        # 去除开头和结尾
        start_trim = trim_start * 1000  # 转换为毫秒
        end_trim = trim_end * 1000  # 转换为毫秒
        trimmed_audio = audio[start_trim:-end_trim] if end_trim > 0 else audio[start_trim:]
        print(f"已去除开头 {trim_start} 秒和结尾 {trim_end} 秒")

        # 计算分段参数（毫秒）
        segment_ms = segment_minutes * 60 * 1000
        total_length = len(trimmed_audio)
        num_segments = total_length // segment_ms + 1  # 计算需要的分段数

        print(f"音频剩余时长: {total_length / 1000:.1f} 秒")
        print(f"将分割为 {num_segments} 个片段")

        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 分割并导出
        for i in range(num_segments):
            start = i * segment_ms
            end = (i + 1) * segment_ms
            segment = trimmed_audio[start:end]

            output_file = os.path.join(output_dir, f"{file_name}-segment_{i + 1}.mp3")
            segment.export(output_file, format="mp3")
            print(f"已保存: {output_file} ({len(segment) / 1000:.1f} 秒)")

    except CouldntDecodeError as e:
        print(f"解码失败: {e}（请确保文件格式正确且未损坏）")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")

def process_directory(input_dir, output_dir, segment_minutes=4, trim_start=20, trim_end=10):
    """
    批量处理目录中的所有音频文件
    :param input_dir: 输入目录
    :param output_dir: 输出目录
    :param segment_minutes: 每个片段的分钟数
    :param trim_start: 去除开头的秒数
    :param trim_end: 去除结尾的秒数
    """
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".mp3"):  # 仅处理 MP3 文件
            input_file = os.path.join(input_dir, filename)
            file_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])

            print(f"\n正在处理文件: {input_file}")
            split_audio(input_file, file_output_dir, segment_minutes, trim_start, trim_end)

if __name__ == "__main__":
    # 配置输入和输出目录
    input_directory = "./"  # 替换为你的输入目录
    output_directory = "./sound_processing/split"  # 替换为你的输出目录

    # 配置切割参数
    segment_duration_minutes = 4  # 每个片段的分钟数
    trim_start_seconds = 20  # 去除开头的秒数
    trim_end_seconds = 10  # 去除结尾的秒数

    # 处理所有文件
    process_directory(input_directory, output_directory, segment_duration_minutes, trim_start_seconds, trim_end_seconds)
    print("\n所有文件处理完成！")