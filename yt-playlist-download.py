import os
import subprocess

from pytube import Playlist, YouTube

def run(pl):
    # Create a folder where all the songs will be put
    print(pl.title)
    if not(os.path.isdir("./"+pl.title)):
        os.mkdir(pl.title)
    # Change working directory to that one
    os.chdir(pl.title)

    # get linked list of links in the playlist
    links = pl.video_urls  # Thanks to https://github.com/modkhi/yt-playlist/issues/5
    # download each item in the list
    for i, l in enumerate(links):
        print("Progress: "+str(i)+" of "+str(len(links))+" ("+str(round(((i/len(links))*100), 2))+"%)")
        # converts the link to a YouTube object
        yt = YouTube(l, use_oauth=True, allow_oauth_cache=True) 
        # takes the best resolution stream to get the best possible audio result
        music = yt.streams.get_highest_resolution()
        # gets the filename of the first audio stream
        default_filename = music.default_filename
        print("Downloading " + default_filename + "...")
        # downloads first audio stream
        music.download()
        # creates mp3 filename for downloaded file
        new_filename = default_filename[0:-3] + "mp3"
        
        # converts mp4 video to mp3 audio
        cmd = "ffmpeg -i \""+default_filename+"\" \""+new_filename+"\""
        
        subprocess.run(cmd, capture_output=True, text=True, input="y")
        
        # Deleting the mp4 video file used to generate mp3
        os.remove(default_filename)

    
    print("Download finished.")

if __name__ == "__main__":
    url = input("Please enter the url of the playlist you wish to download: ")
    pl = Playlist(url)
    run(pl)