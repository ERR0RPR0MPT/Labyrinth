# Labyrinth

Labyrinth 用于将视频画面混淆化，从而规避一些版权限制。

!!EXPERIMENTAL VERSION!!

警告：请遵守当地法规，不要用于非法用途。

## 安装

下载源代码：

`git clone https://github.com/ERR0RPR0MPT/Labyrinth.git`

安装依赖：

`pip install -r requirements.txt`

## TODO

目前仅支持 CPU 运算，这导致转换 1080P 甚至 720P 的视频都较为吃力，因此未来将重写 PyTorch 版本并使用 GPU 进行加速。

## 效果

原视频(720P)：

<video src="https://raw.githubusercontent.com/ERR0RPR0MPT/Labyrinth/main/static/BD720P2.mp4" controls="controls" width="100%" height="auto" align=center></video>

加密后的视频：

<video src="https://raw.githubusercontent.com/ERR0RPR0MPT/Labyrinth/main/static/FROMB720P2.mp4" controls="controls" width="100%" height="auto" align=center></video>

上传B站后下载得到的加密视频进行恢复操作后的原视频：

<video src="https://raw.githubusercontent.com/ERR0RPR0MPT/Labyrinth/main/static/FROMB720P2_output.mp4" controls="controls" width="100%" height="auto" align=center></video>

B站视频地址：https://www.bilibili.com/video/BV1u24y157LH/
