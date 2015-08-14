#!/usr/bin/env python
import os
import time
from os import listdir
from pymediainfo import MediaInfo
from pprint import pprint
import sqlite3

disk_path="/Volumes/NO NAME"
db_name="media.db"
main_table="media_files"
#disk_path="./testdir"
debug_insert_max = 5


#files = [ f for f in listdir(disk_path) ]

#print files
debug_insert_count = 0

def scan_media():
    for dirname, dirnames, filenames in os.walk(disk_path):
        global debug_insert_count
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
                            debug_insert_count += 1
                            insert_db(db_name, main_table, track.width, track.height, \
                                track.duration, file_mtime, filename)
                            if debug_insert_count > debug_insert_max:
                                return
                        # track.other_duration
                        #pprint(track.to_data())
                        #break

def insert_db(db,tbl, width, height, duration, end_time, file_name):
    print "inserting: db:", db, "tbl:", tbl, ",", width, height, duration, end_time, file_name 
    conn = sqlite3.connect(db)
    c = conn.cursor()
    begin_time = end_time - (duration/1000)
    c.execute('''INSERT INTO %s (file_path,width,height,duration, begin_time, end_time)
    VALUES (?, ?, ?, ?, ?, ?)
    ''' % tbl, (file_name, width, height, duration, begin_time, end_time) )
    conn.commit()
    conn.close()
                            
                        
def test_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('SELECT * from sqlite_master WHERE type="table"')
    print c.fetchall()
    conn.close()
    
def check_db_exist(table_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    bind = (table_name,)
    c.execute('SELECT * from sqlite_master WHERE type="table" AND name=?', bind)
    ret = c.fetchall()
    conn.close()
    
    return ret

def create_db_table(table_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    #bind = (table_name,)
    c.execute('''CREATE TABLE %s 
    (   media_id INTEGER PRIMARY KEY autoincrement not null,
        file_path text,
        width INTEGER,
        height INTEGER,
        duration INTEGER,
        begin_time INTEGER,
        end_time INTEGER    
    )'''
    % table_name) #insecure, but binding does not work on table names..
    conn.commit()
    conn.close()

#scan_media()
#create_db_table()
if check_db_exist(main_table):
    print "Table %s already exists" % main_table
else:
    print "Table %s not exist, creating..." % main_table
    create_db_table(main_table)

#test_db()
scan_media()
print "done"

                        #print track.bit_rate, track.bit_rate_mode, track.codec, filename
                #print(filename, file_size_mb , "MB")
            
        #print(subdir)

# list all dirs that has at least one MP4 file, and filesize greater than 2GB
