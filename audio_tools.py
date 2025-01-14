import subprocess
import os
import soundfile as sf
import numpy as np
import soundfile as sf
from moviepy.editor import AudioFileClip


def split_audio(input_file, start_time, duration, output_file):  # 裁剪音频
    '''
    :param input_file: 输入的音频文件地址
    :param start_time: 起始时间
    :param duration: 时长
    :param output_file: 保存的音频文件地址
    :return:
    '''
    command = f"ffmpeg -i {input_file} -ss {start_time} -t {duration} {output_file}"
    subprocess.run(command, shell=True)


def wav_repeat(input_file, output_file, repeat_time):  # 直接重复音频
    '''
    :param input_file: 输入的音频文件地址
    :param output_file: 保存的音频文件地址
    :param repeat_time: 重复倍数
    :return:
    '''
    assert repeat_time > 0
    wav, sr = sf.read(input_file)  # [44100,2]
    new_signal = np.tile(wav, (repeat_time, 1))
    sf.write(output_file, new_signal, sr)


def extract_audio_and_save(root, save_root):  # 提取视频中的音频流,并保存
    '''
    :param root: 输入视频地址 或 视频所属文件夹地址
    :param save_root: 音频流所要保存的文件夹地址
    :return:
    '''

    if os.path.isdir(root):  # 文件夹
        print("输入的是视频文件夹地址: ", root)
        files = os.listdir(root)
        video_list = [file for file in files if file.endswith('.mp4')]
        if len(files) != len(video_list):
            print("#" * 10)
            print("请注意,文件夹内除了mp4格式,还有其他格式!!!!")
            print("#" * 10)
        print("视频总量:", len(video_list))
        print("视频列表:",video_list)
        count = 0

        save_root = '/data4T/下载tmp/XD-Violence_OneDrive_Testvideos/audios'
        os.makedirs(save_root, exist_ok=True)

        for i in video_list:
            input_file = os.path.join(root, i)
            name = input_file.split('/')[-1][:-4]
            save_path = '{}/{}.wav'.format(save_root, name)
            if os.path.exists(save_path):  # 如果之前处理过了,就可以直接跳过
                continue

            try:
                audio = AudioFileClip(input_file)
                audio.write_audiofile(save_path)  # 除了wav,m4v,mp3等音频格式貌似也行
            except:
                print("有问题的视频名字:", name)
                count += 1
        print("有问题的视频总量:", count)

    elif os.path.isfile(root):  # 文件
        print("输入的是视频文件地址: ", root)
        name = root.split('/')[-1][:-4]
        save_path = '{}/{}.wav'.format(save_root, name)
        if os.path.exists(save_path):  # 如果之前处理过了,就可以直接跳过
            pass

        try:
            audio = AudioFileClip(root)
            audio.write_audiofile(save_path)  # 除了wav,m4v,mp3等音频格式貌似也行
        except:
            raise ValueError("视频有问题:[{}]".format(root))

    else:
        assert 1 == 2, "地址有问题:[{}]".format(root)


def read_audio_check(root):  # 读取音频看哪些有问题
    '''
    :param root: 输入音频地址 或 音频所属文件夹地址
    :return:
    '''
    if os.path.isdir(root):  # 文件夹
        print("输入的是音频文件夹地址: ", root)
        files = os.listdir(root)
        audio_list = [file for file in files if file.endswith('.wav')]
        if len(files) != len(audio_list):
            print("#"*10)
            print("请注意,文件夹内除了wav格式,还有其他格式!!!!")
            print("#" * 10)

        print("音频总量:", len(audio_list))
        print("音频列表:",audio_list)
        count = 0
        for i in audio_list:
            input_file = os.path.join(root, i)
            try:
                wav, sr = sf.read(input_file)
            except:
                print("有问题的音频名字:", input_file.split('/')[-1][:-4])
                count += 1
        print("有问题的音频数量:", count)

    elif os.path.isfile(root):  # 文件
        print("输入的是音频文件地址: ", root)
        try:
            wav, sr = sf.read(root)
        except:
            raise ValueError("视频有问题:[{}]".format(root))

    else:
        assert 1 == 2, "地址有问题:[{}]".format(root)


if __name__ == "__main__":
    # 裁剪音频
    # input_file = "/home/media/桌面/LWcZGccvDpg.wav"  # 输入音频文件
    # start_time = "00:00:00"  # 分割起始时间
    # duration = "00:00:01"  # 分割持续时间
    # output_file = "/home/media/桌面/split_audio.wav"  # 输出分割后的音频文件名
    # split_audio(input_file, start_time, duration, output_file)

    # 重复音频
    # input_file = "/home/media/桌面/split_audio.wav"
    # output_file = "/home/media/桌面/repeat_audio.wav"
    # wav_repeat(input_file, output_file, 10)

    # 提取视频中的音频,
    extract_audio_and_save(root='/data4T/下载tmp/XD-Violence_OneDrive_Testvideos/samples',save_root='/data4T/下载tmp/XD-Violence_OneDrive_Testvideos/samples_audio')
    # 读取音频,查看行不行
    # read_audio_check('/data4T/下载tmp/XD-Violence_OneDrive_Testvideos/samples_audios')
