# Labyrinth

Labyrinth 用于将视频画面混淆化，从而规避一些版权和审查限制。

警告：请遵守当地法规，请勿用于非法用途，开放者不承担使用者因不正当行为而导致严重后果的任何责任。

```
!!EXPERIMENTAL VERSION!!
此项目为实验版本，并且可能不再更新，可用实现请使用 Go 版本：转到 https://github.com/ERR0RPR0MPT/Labyrinth-go
```

## 安装

下载源代码：

`git clone https://github.com/ERR0RPR0MPT/Labyrinth.git`

安装依赖：

`pip install -r requirements.txt`

## TODO

- Bug: 加密后还原的视频会出现部分像素丢失/错误
- 图片颜色位移
- 视频帧间重排
- 音频分段重排
- 音频正倒放混淆
- 音调混淆
- 加密: 文件加密到音视频、图片
- 进一步提高运行效率

## 效果

原视频(1080P60fps)：https://www.bilibili.com/video/BV1x5411o7Kn

加密后的视频(1080P60fps)：https://www.bilibili.com/video/BV1ks4y127nM

恢复后的视频(1080P60fps)：https://www.bilibili.com/video/BV17g4y1g798
