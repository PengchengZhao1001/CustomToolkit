import subprocess
import os
import soundfile as sf
import numpy as np

'''裁剪音频'''
def split_audio(input_file, start_time, duration, output_file):
    command = f"ffmpeg -i {input_file} -ss {start_time} -t {duration} {output_file}"
    subprocess.run(command, shell=True)

'''直接重复音频'''
def wav_repeat(input_file, output_file, repeat_time):
    assert repeat_time>0
    wav, sr = sf.read(input_file) # [44100,2]
    new_signal = np.tile(wav, (repeat_time, 1))
    sf.write(output_file, new_signal, sr)


if __name__ == "__main__":
    # 裁剪音频
    # input_file = "/home/media/桌面/LWcZGccvDpg.wav"  # 输入音频文件
    # start_time = "00:00:00"  # 分割起始时间
    # duration = "00:00:01"  # 分割持续时间
    # output_file = "/home/media/桌面/split_audio.wav"  # 输出分割后的音频文件名
    # split_audio(input_file, start_time, duration, output_file)

    # 重复音频
    input_file = "/home/media/桌面/split_audio.wav"
    output_file = "/home/media/桌面/repeat_audio.wav"
    wav_repeat(input_file,output_file,10)
