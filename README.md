# youtube_downloader
Download youtube videos saved in Google Chrome's bookmarks folders.

Only tested with Google Chrome in Ubuntu 18.04

### Prerequisites
ffmpeg is needed to convert the ```.mp4``` to ```.mp3``` files aswell as joining together the audio and thumbnail.
Installation instrucions are available in [ffmpeg](https://www.ffmpeg.org/)

### Installation
```
git clone https://github.com/Turr0n/youtube_downloader.git
cd youtube_downloader
pip install -r requirements.txt
```
Non-standar python modules used:
* [pytube](https://github.com/nficano/pytube)
* [requests](https://github.com/requests/requests)

### Usage

```
python3 you.py [-n folder_name] [-p 4] [--no-thumb] [--path path]
```

Arguments:
```
    -n          Name of the bookmarks folder. Required!
    -p          Number of parallel processes to run. Default: 4
    --no-thumb  Don't include thumbnails.
    --path      The path where the downloaded files will be saved.
```

The script will download all the YouTube videos bookmarked in the given folder. They will get converted to mp3 and thumbnails will be included. If no path is given, the files will be saved to folder called: ```[name]_downloads```.

### Credits

This tools is built around the awsome module [pytube](https://github.com/nficano/pytube) written by @nficano.
