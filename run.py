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
#debug_insert_max = 5


#files = [ f for f in listdir(disk_path) ]

#print files
#debug_insert_count = 0

def scan_media():
    for dirname, dirnames, filenames in os.walk(disk_path):
        #global debug_insert_count
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
                           # debug_insert_count += 1
                            insert_db(db_name, main_table, track.width, track.height, \
                                track.duration, file_mtime, filename)
                           # if debug_insert_count > debug_insert_max:
                             #   return
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
    
def print_range():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(''' SELECT MIN(begin_time) from %s
    ''' % main_table)
    #print "Min begin:", c.fetchall()
    row = c.fetchall()
    min_begin = row[0][0]
    #conn.close()
    print "min:", min_begin, ", as:", time.ctime(min_begin)
    
    c.execute(''' SELECT MAX(end_time) from %s
    ''' % main_table)
    
    row = c.fetchall()
    max_end = row[0][0]
    
    print "max:", max_end, ", as:", time.ctime(max_end)
    conn.close()
    
    return min_begin, max_end
    
def query_time_t():
    min_t, max_t = print_range()
    user_time = input("Please type a time_t:")
    print "Your input(",user_time,") is local time:", time.ctime(user_time)
    #print "Your input: [", user_time, "]"
    if user_time < min_t or user_time > max_t:
        print "Your input(", user_time,") is out of range: [", min_t, ",", max_t,"]"
        return
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    bind = (user_time, user_time,)
    c.execute(''' SELECT file_path, begin_time, end_time
    FROM %s WHERE begin_time <= ? AND end_time >= ?
    ''' % main_table, bind )
    rows = c.fetchall()
    for row in rows:
        f_name, b_time, e_time = row
        offset = user_time - b_time
        offset_mins = offset / 60
        offset_secs = offset % 60
        print "File [",f_name,"], offset:", offset_mins, "mins", offset_secs, "secs, range [", \
            time.ctime(b_time), "to", time.ctime(e_time),"]"
            
    conn.close()
    

#scan_media()
#create_db_table()
if check_db_exist(main_table):
    print "Table %s already exists" % main_table
else:
    print "Table %s not exist, creating..." % main_table
    create_db_table(main_table)

#test_db()
#scan_media()
#print_range()
query_time_t()
print "done"

                        #print track.bit_rate, track.bit_rate_mode, track.codec, filename
                #print(filename, file_size_mb , "MB")
            
        #print(subdir)

# list all dirs that has at least one MP4 file, and filesize greater than 2GB
