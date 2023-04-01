import os
import random
from PIL import Image
import numpy as np
import shutil
import subprocess
import multiprocessing


def laby_to_file(arr, name="laby.npy"):
    a1 = np.array(arr)
    np.save(name, a1)
    return True


def laby_to_list(name="laby.npy"):
    arr = np.load(name)
    arr_list = arr.tolist()
    return arr_list


def generate_random_laby(width, height, mode="hr"):
    arr = []
    for i in range(0, height):
        row = []
        for j in range(0, width):
            row.append([j, i])
        if mode == "r" or mode == "vr":  # 随机排列
            random.shuffle(row)
        arr.append(row)
    if mode == "r" or mode == "hr":  # 随机排行
        random.shuffle(arr)
    return arr


def generate_random_laby_to_file(name="laby.npy", width="1920", height="1080", mode="hr"):
    try:
        with open(name, "w") as f:
            f.write(decode_list(generate_random_laby(width, height, mode)))
        return True
    except:
        return False


def generate_random_image(lst=None, origin="origin.png", output="output.png"):
    print(f"开始加密：{output}")
    if lst is None:
        print("[WARN] 无对应的列表文件")
        exit(0)
    original_image = Image.open(origin)
    width, height = original_image.size
    if len(lst) != height or len(lst[0]) != width:
        print(f"[WARN] 不适合的尺寸：{str(len(lst))}x{str(len(lst[0]))} != {str(height)}x{str(width)}")
        exit(0)
    new_image = Image.new('RGB', (width, height))
    for _height in range(len(lst)):
        for _width in range(len(lst[_height])):
            try:
                pixel = original_image.getpixel((lst[_height][_width][0], lst[_height][_width][1]))
            except:
                print(lst[_height][_width][0], lst[_height][_width][1])
                print(width, height)
                return None
            new_image.putpixel((_width, _height), pixel)
    new_image.save(output, **original_image.info)
    return True


def restore_original_image(lst=None, origin="output.png", restore="restore.png"):
    print(f"开始解密：{restore}")
    if lst is None:
        print("[WARN] 无对应的列表文件")
        exit(0)
    original_image = Image.open(origin)
    width, height = original_image.size
    if len(lst) != height or len(lst[0]) != width:
        print(f"[WARN] 不适合的尺寸：{str(len(lst))}x{str(len(lst[0]))} != {str(height)}x{str(width)}")
        exit(0)
    new_image = Image.new('RGB', (width, height))
    for _height in range(len(lst)):
        for _width in range(len(lst[_height])):
            try:
                pixel = original_image.getpixel((_width, _height))
            except:
                print(lst[_height][_width][0], lst[_height][_width][1])
                print(width, height)
                return None
            new_image.putpixel((lst[_height][_width][0], lst[_height][_width][1]), pixel)
    new_image.save(restore, **original_image.info)
    return True


def generate(width=1920, height=1080, mode="hr", name="laby.npy"):
    arr = generate_random_laby(width, height, mode)
    laby_to_file(arr, name)
    laby_arr = laby_to_list(name)
    if arr == laby_arr:
        print("Success")
    else:
        print("出现错误")
    return


def encrypt(laby="laby.npy", source="origin.png", output="output.png"):
    laby_arr = laby_to_list(laby)
    generate_random_image(laby_arr, source, output)
    print("Success")
    exit(0)

def decrypt(laby="laby.npy", source="output.png", output="restore.png"):
    laby_arr = laby_to_list(laby)
    restore_original_image(laby_arr, source, output)
    print("Success")
    exit(0)

def video_encrypt(laby="laby.npy", source="origin.mp4", threads=8, framerate=30):
    output_dir = ""
    source_dir = ""
    source_name = os.path.basename(source).split(".")[0]
    if not "/" in source or not "\\" in source:
        output_dir = os.path.join(os.getcwd(), os.path.basename(source).split(".")[0])
        source_dir = os.path.join(os.getcwd(), os.path.basename(source))
    else:
        output_dir = os.path.join(os.path.dirname(source), os.path.basename(source).split(".")[0])
        source_dir = source
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    output_dir_source = os.path.join(output_dir, "source")
    output_dir_output = os.path.join(output_dir, "output")
    if not os.path.exists(output_dir_source):
        os.mkdir(output_dir_source)
    if not os.path.exists(output_dir_output):
        os.mkdir(output_dir_output)
    command = f'ffmpeg -i "{source_dir}" -vn -acodec libmp3lame "{output_dir}/{source_name}_output.mp3"'
    print(f"开始提取音乐：{command}")
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(command, shell=True, stdout=devnull, stderr=subprocess.STDOUT)
        print("提取成功")
    except:
        print("提取失败")
        return False
    command = f'ffmpeg -i "{source_dir}" "{output_dir_source}/%d.png"'
    print(f"开始转换图片序列：{command}")
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(command, shell=True, stdout=devnull, stderr=subprocess.STDOUT)
        print("转换成功")
    except:
        print("转换失败")
        return False

    print("开始加密图片序列")
    # 创建线程池
    pool = multiprocessing.Pool(processes=threads)
    # 遍历所有文件夹和文件
    laby_arr = laby_to_list(laby)
    for subdir, dirs, files in os.walk(output_dir_source):
        for file in files:
            source = os.path.join(subdir, file)
            output = os.path.join(output_dir_output, file)
            # 将任务提交到线程池中
            pool.apply_async(generate_random_image, args=(laby_arr, source, output))
    # 关闭进程池，防止新的任务被提交
    pool.close()
    # 等待所有任务完成
    pool.join()

    command = f'ffmpeg -r {framerate} -i "{output_dir_output}/%d.png" -i "{output_dir}/{source_name}_output.mp3" -vcodec libx264 -pix_fmt yuv420p -c:a copy "{output_dir}/{source_name}_output.mp4"'
    print(f"开始合成视频：{command}")
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(command, shell=True, stdout=devnull, stderr=subprocess.STDOUT)
        print("转换成功")
    except:
        print("转换失败")
        return False

    print("Success")
    exit(0)


def video_decrypt(laby="laby.npy", source="output.mp4", threads=8, framerate=30):
    output_dir = ""
    source_dir = ""
    source_name = os.path.basename(source).split(".")[0]
    if not "/" in source or not "\\" in source:
        output_dir = os.path.join(os.getcwd(), os.path.basename(source).split(".")[0])
        source_dir = os.path.join(os.getcwd(), os.path.basename(source))
    else:
        output_dir = os.path.join(os.path.dirname(source), os.path.basename(source).split(".")[0])
        source_dir = source
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    output_dir_restore = os.path.join(output_dir, "restore_source")
    output_dir_output = os.path.join(output_dir, "restore_output")
    if not os.path.exists(output_dir_restore):
        os.mkdir(output_dir_restore)
    if not os.path.exists(output_dir_output):
        os.mkdir(output_dir_output)
    command = f'ffmpeg -i "{source_dir}" -vn -acodec libmp3lame "{output_dir}/{source_name}_output.mp3"'
    print(f"开始提取音乐：{command}")
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(command, shell=True, stdout=devnull, stderr=subprocess.STDOUT)
        print("提取成功")
    except:
        print("提取失败")
        return False
    command = f'ffmpeg -i "{source_dir}" "{output_dir_restore}/%d.png"'
    print(f"开始转换图片序列：{command}")
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(command, shell=True, stdout=devnull, stderr=subprocess.STDOUT)
        print("转换成功")
    except:
        print("转换失败")
        return False

    print("开始解密图片序列")
    # 创建线程池
    pool = multiprocessing.Pool(processes=threads)
    # 遍历所有文件夹和文件
    laby_arr = laby_to_list(laby)
    for subdir, dirs, files in os.walk(output_dir_restore):
        for file in files:
            source = os.path.join(subdir, file)
            output = os.path.join(output_dir_output, file)
            # 将任务提交到线程池中
            pool.apply_async(restore_original_image, args=(laby_arr, source, output))
    # 关闭进程池，防止新的任务被提交
    pool.close()
    # 等待所有任务完成
    pool.join()

    command = f'ffmpeg -r {framerate} -i "{output_dir_output}/%d.png" -i "{output_dir}/{source_name}_output.mp3" -vcodec libx264 -pix_fmt yuv420p -c:a copy "{output_dir}/{source_name}_output.mp4"'
    print(f"开始合成视频：{command}")
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(command, shell=True, stdout=devnull, stderr=subprocess.STDOUT)
        print("转换成功")
    except:
        print("转换失败")
        return False

    print("Success")
    exit(0)


if __name__ == "__main__":
    # generate(640, 360, "r", "labyrinth_r_360P.npy")
    # generate(854, 480, "r", "labyrinth_r_480P.npy")
    # generate(1280, 720, "r", "labyrinth_r_720P.npy")
    # generate(1920, 1080, "r", "labyrinth_r_1080P.npy")
    # generate(3840, 2160, "r", "labyrinth_r_4K.npy")
    # generate(1920, 1080, "hr", "labyrinth_hr_1080P.npy")
    # generate(640, 360, "hr", "labyrinth_hr_360P.npy")
    # generate(854, 480, "hr", "labyrinth_hr_480P.npy")
    # generate(1280, 720, "hr", "labyrinth_hr_720P.npy")
    # generate(1920, 1080, "hr", "labyrinth_hr_1080P.npy")
    # generate(3840, 2160, "hr", "labyrinth_hr_4K.npy")
    # encrypt("labyrinth_hr_1080P.npy", "d.png", "outpute.png")
    # decrypt("labyrinth_hr_1080P.npy", "outputd.png", "restore.png")
    # generate(852, 480, "hr", "labyrinth_hr_480P.npy")
    # video_encrypt("labyrinth_r_1080P.npy", "坏苹果.mp4", threads=12, framerate=60)
    # video_decrypt("labyrinth_r_1080P.npy", "坏苹果_output.mp4", threads=12, framerate=60)
    video_encrypt("labyrinth_hr_720P.npy", "坏苹果.mp4", threads=12, framerate=30)
    video_decrypt("labyrinth_hr_720P.npy", "坏苹果_output.mp4", threads=12, framerate=30)
    # video_encrypt("labyrinth_r_4K.npy", "BD4K.mp4", threads=3, framerate=60)
