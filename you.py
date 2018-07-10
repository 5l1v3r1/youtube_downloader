from subprocess import Popen, DEVNULL, STDOUT
from argparse import ArgumentParser
from multiprocessing import Pool
from pytube import YouTube
from pytube import Playlist
from getpass import getuser
import requests
import json
import os


def args():
    '''
    Function handling the arguments supplied by the user.
    '''

    parser = ArgumentParser()
    parser.add_argument('-n', dest='name', type=str, required=True, help='Name of the bookmarks folder.')
    parser.add_argument('-p', dest='process', type=int, required=False, default=4, help='Number of parallel processes to run. Default: 4')
    parser.add_argument('--no-thumb', action='store_true', default=False, required=False, help="Don't include thumbnails.")
    parser.add_argument('--path', dest='path', type=str, default=False, required=False, help='The path where the downloaded files will be saved.')

    return parser.parse_args()


def strip_format(fn):
    '''
    Get rig of the format in the given filename.
    '''

    return '.'.join(fn.split('.')[:-1])


def download_thumbnail(fn, url):
    '''
    Download the thumbnail specified by the url and save it to a file
    so the ffmpeg is able to included as covert art.
    '''

    print('Downloading thumbnail...')
    r = requests.get(url, stream=True)
    
    if r.status_code == 200:
        with open(path+'{}_thumb'.format(strip_format(fn)), 'wb') as f:
            [f.write(chunk) for chunk in r]
        
        return True
    
    else:
        return False


def convert(file, thumbnail=None):
    '''
    Convert the video to mp3 including or not the thumbnail.
    '''

    print('[...] Converting: ', file)

    if thumbnail != None and download_thumbnail(file, thumbnail):
        Popen(['ffmpeg', '-i', path+file, '-i', '{}{}_thumb'.format(path, strip_format(file)),
            '-map', '0', '-map', '1', path+'.'.join(file.split('.')[:-1])+'.mp3'],
            stdout=DEVNULL, 
            stderr=STDOUT).wait()
        
        '''Deleting the thumbnail file as it's no longer needed.'''
        Popen(['rm', path+'{}_thumb'.format(strip_format(file))])

    else:
        Popen(['ffmpeg', '-i', path+file, path+'.'.join(file.split('.')[:-1])+'.mp3'], 
            stdout=DEVNULL, 
            stderr=STDOUT).wait()


def download(url):
    '''
    Download the video using pytube. Although the downloaded video will
    just include audio, further conversion needs to be done using ffmpeg.
    '''

    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    fn = stream.default_filename

    if strip_format(fn) in files:
        print('[!]   {} already downloaded'.format(fn))
        return
    
    print('[...] Downloading: ', fn)
    stream.download(output_path=path)
    print('\n[+]   Done! ', fn)
    
    if not args.no_thumb:
        convert(fn, thumbnail=yt.thumbnail_url)
    
    else:
        convert(fn)
    
    '''Deleting the video file once the conversion to mp3 has finished.'''
    Popen(['rm', path+fn])


def load_urls():
    '''
    Load urls saved in the specified bookmark folder.
    '''

    with open('/home/{}/.config/google-chrome/Default/Bookmarks'.format(getuser())) as f:
        eco = json.load(f)
    
    bookmarks = [entry for entry in eco['roots']['bookmark_bar']['children'] if entry['name'] == args.name][0]['children']
    return [entry['url'] for entry in bookmarks if entry['url'].startswith('https://www.youtube.com/watch?v=')]


def handle(url):
    '''
    Handle playlists and single videos.
    '''

    if '&list=' in url:
        lst = Playlist(url).video_urls
        [download(url) for url in lst]

    else:
        download(url)



if __name__ == '__main__':
    args = args()

    '''
    Set the path where the downloaded files will be saved. 
    If it doesn't exist yet, create it.
    '''
    path = os.getcwd()+'/{}_downloads/'.format(args.name) if not args.path else args.path
    if not os.path.exists(path):
        Popen(['mkdir', path]).wait()

    files = [strip_format(file) for file in os.listdir(path)]
    urls = load_urls()

    print('Videos to download: ', len(urls), '\n')
    
    p = Pool(args.process)
    p.map(handle, urls)