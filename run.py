#!/usr/bin/env python
from os import listdir

disk_path="/Volumes/NO NAME"

files = [ f for f in listdir(disk_path) ]

print files
