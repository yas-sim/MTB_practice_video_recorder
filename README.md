# MTB Practice Video Recorder

--------
## Description

 This tool playss back movie from a movie file or a webCam, and keep the frames of the latest 10 minutes. This tool supports several play modes and options such as play/pause control, rewind/feed-forward, advance/back frames, and reverse/normal play so that you can watch your interesting point of the movie instantly. This program can save 10 seconds of movie from the current playback point.  
 The tool is intended for MTB skill practice. You can review your try while keep recording movie. The tool is also applicable for any other sports and so on.  

 このツールはムービーファイルやUSB webCamからの画像を再生しつつ、最新の10分間の映像を保持します。FF/Rewind, 再生/ポーズ, フレームを進める/戻すなどの操作が可能なので、任意の点を見ることが可能です。またプログラムは再生している点から10秒間のムービーを切り出して保存する機能もあります。  
 このツールはMTBのスキルトレーニングに使うことを念頭に開発しました。録画しながら練習し、録画を継続したまま任意の点を再生して確認できるのでスキル向上に役立てることができます。もちろんその他のスポーツの練習などに使うことも可能です。  

![Sample Movie](./resources/sample-movie.gif)

--------
## Prerequisites (必要要件)
 - Python 3.x  
 - OpenCV Python, Numpy  
 ```sh
 $ python -m pip install opencv-python numpy
 ```  

[Python web site](https://www.python.org/)

--------

## How to use (使用方法)

```sh
$ python mtb_recorder.py [-i <movie_file>] [-c <cam#>]
```
Note: cam0 will be used when no option is given.  

**Options:**  
|Options|Descriptions|
|----|----|
|`-i` or `--input`|Specify an input movie file|  
|`-c` or `--cam`|Specify the number of USB webCam (1st camera = 0)|  
  
**Examples:**  
```sh
$ python mtb_recorder.py -i mtb_movie.mp4
$ python mtb_recorder.py -c 0
```

--------
## How to operate (操作方法)

|Keys|Function|
|----|----|
|`z`, `x`| 1 sec back/forward|
|`a`, `s`| 10 sec back/forward|
|`j`, `k`| 1 frame back/forward|
|`<space>`, `p`| Pause/Resume|
|`n`, `m`| Reverse/Normal playback|
|`0`| Back to current recording point (zero time offset)|
|`r`| Save a movie of 10 second from the playback point. Movie file name will be `movie_YYYYMMDD-hhmmss.mp4`|
|`<ESC>`, `q`| Exit program|

--------
## Disclaimer
No support. Provided as-is.
