import os
import subprocess
import cv2
import shutil
import sys


def resize_frames(raw_root: str, H: int = 256, W: int = 256, save_raw_dir: bool = False,
                  print_: bool = True):  # 对文件夹内的图像帧进行resize
    '''
    :param raw_root: 要放缩帧的文件夹地址
    :param H: 目标高
    :param W: 目标宽
    :param save_raw_dir: 是否保存原始文件夹地址
    :param print_: 要不要打印第一句话
    :return:
    '''

    if print_:
        print("*" * 20)
        print("对文件夹内的视频帧进行resize处理: [{}]".format(raw_root))
        print("修改尺寸为H/W为{}/{}, 是否保留原始帧文件夹: [{}]".format(H, W, save_raw_dir))
        print("*" * 20)
        print(" ")
    dir_name = raw_root.split('/')[-1]
    raw_dir = os.path.join(os.path.dirname(raw_root), dir_name + '_raw')
    os.rename(raw_root, raw_dir)  # 先修改文件夹名字
    new_root = os.path.join(os.path.dirname(raw_root), dir_name)
    os.makedirs(new_root, exist_ok=True)
    default = True  # 判断是否成功

    for imgs_name in os.listdir(raw_dir):
        try:
            img = cv2.imread(os.path.join(raw_dir, imgs_name))
            res_img = cv2.resize(img, (W, H))  # 注意是W,H,   interpolation这里选择默认的双线性插值
            cv2.imwrite(os.path.join(new_root, imgs_name), res_img)
        except:
            # 有问题,直接文件夹删掉
            shutil.rmtree(new_root)
            default = False
            break

    if os.path.exists(new_root):  # 代表已经成功放缩了
        if not save_raw_dir:
            shutil.rmtree(raw_dir)
    if print_:
        if default:
            print("处理完成!")
        else:
            print("处理失败!")

    return default


def extract_frames_ffmpeg(root: str, save_root: str, fps=None, resize: bool = False, H: int = 256, W: int = 256,
                          save_raw_dir: bool = False):  # 提取视频帧,利用ffmpeg
    '''
    :param root: 输入视频地址 或 视频所属文件夹地址                  /A/f.mp4 -> 即 /A
    :param save_root: 所有视频的帧所要保存的文件夹地址               /B/f/.png -> 即 /B
    :param fps: 设定采样帧率 每秒采样多少帧  如果为None,则默认原始帧率
    :param resize: 是否修改帧尺寸大小
    :param save_raw_dir: 如果修改尺寸的话, 是否保留原来的帧文件夹
    :return:
    '''
    print("*" * 20)
    print("提取视频帧,采用ffmpeg,帧率[{}], 是否修改尺寸为H/W为{}/{}: [{}], 是否保留原始帧文件夹: [{}]".format(fps, H, W,
                                                                                                              resize,
                                                                                                              save_raw_dir))
    print("*" * 20)
    print(" ")
    if os.path.isdir(root):  # 文件夹
        print("输入的是视频文件夹地址: ", root)
        files = os.listdir(root)
        video_list = [file for file in files if file.endswith('.mp4')]
        if len(files) != len(video_list):
            print("#" * 10)
            print("请注意,文件夹内除了mp4格式,还有其他格式!!!!")
            print("#" * 10)
        print("视频总量:", len(video_list))
        print("视频列表:", video_list)
        count = 0
        print("要保存的所有视频帧的文件夹地址: ", save_root)

        for i in video_list:
            input_file = os.path.join(root, i)
            name = input_file.split('/')[-1][:-4]
            frames_root = os.path.join(save_root, name)
            if os.path.exists(frames_root) and (len(os.listdir(frames_root)) > 0):
                continue
            else:
                os.makedirs(frames_root, exist_ok=True)

            try:
                if fps:
                    command = [
                        'ffmpeg',
                        '-i', input_file,
                        '-vf', 'fps={}'.format(fps),
                        f'{frames_root}/%08d.png'  # 8位数名字 00000000.png
                    ]
                else:
                    command = [
                        'ffmpeg',
                        '-i', input_file,
                        f'{frames_root}/%08d.png'  # 8位数名字 00000000.png
                    ]
                subprocess.run(command)
            except:
                print("有问题的视频名字:", name)
                shutil.rmtree(frames_root)
                count += 1
                continue

            # 修改帧
            if resize:
                _ = resize_frames(raw_root=frames_root, H=H, W=W, save_raw_dir=save_raw_dir, print_=False)


    elif os.path.isfile(root):  # 文件
        print("输入的是视频文件地址: ", root)
        name = root.split('/')[-1][:-4]
        frames_root = os.path.join(save_root, name)
        if os.path.exists(frames_root) and (len(os.listdir(frames_root)) > 0):
            sys.exit(0)
        else:
            os.makedirs(frames_root, exist_ok=True)
        try:
            if fps:
                command = [
                    'ffmpeg',
                    '-i', root,
                    '-vf', 'fps={}'.format(fps),
                    f'{frames_root}/%08d.png',  # 8位数名字 00000000.png
                ]
            else:
                command = [
                    'ffmpeg',
                    '-i', root,
                    f'{frames_root}/%08d.png'  # 8位数名字 00000000.png
                ]
            subprocess.run(command)
        except:
            shutil.rmtree(frames_root)
            raise ValueError("有问题的视频名字:", name)

        # 修改帧
        if resize:
            _ = resize_frames(raw_root=frames_root, H=H, W=W, save_raw_dir=save_raw_dir, print_=False)

    else:
        assert 1 == 2, "地址有问题:[{}]".format(root)


if __name__ == "__main__":
    # ffmpeg的输出似乎可以屏蔽,还未尝试
    extract_frames_ffmpeg(root='/data4T/下载tmp/samples/xxx.mp4',
                          save_root='/data4T/下载tmp/frames',
                          fps=None, resize=True, H=256, W=256, save_raw_dir=False
                          )
