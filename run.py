#!/usr/bin/env python
import os
import time
from os import listdir
from pymediainfo import MediaInfo
from pprint import pprint

disk_path="/Volumes/NO NAME"
#disk_path="./testdir"


#files = [ f for f in listdir(disk_path) ]

#print files

for dirname, dirnames, filenames in os.walk(disk_path):
    for file in filenames:
        filename = os.path.join(dirname,file)
        file_stem, file_ext = os.path.splitext(filename)
        if file_ext == ".MP4":
            #print(file_stem, file_ext)
            file_size = os.path.getsize(filename)
            file_size_mb = file_size >> 20
            file_mtime = os.path.getmtime(filename)
            file_mtime_h = time.ctime(file_mtime)
            if file_size_mb > 1000:
                media_info = MediaInfo.parse(filename)
                for track in media_info.tracks:
                    if track.track_type == 'Video':
                        print track.width, track.height, track.duration, file_mtime_h, file_mtime, filename
                        # track.other_duration
                        #pprint(track.to_data())
                        #break
                        
                        #print track.bit_rate, track.bit_rate_mode, track.codec, filename
                #print(filename, file_size_mb , "MB")
            
        #print(subdir)

# list all dirs that has at least one MP4 file, and filesize greater than 2GB
