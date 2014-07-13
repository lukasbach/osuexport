# osuexport.py
# written 13-July-2014 by Lukas Bach
# 
# Exports all songs from the music rythm game osu! (osugame.com) to a specified directory,
# renames and taggs them with their proper artist and title
#
# Licensed under GNU GENERAL PUBLIC LICENSE 2
# http://www.gnu.org/licenses/gpl-2.0.txt
#
# https://github.com/lukasbach
# https://twitter.com/questcube

import sys
import os
import shutil
from tagger import *

osuSongPath = "C:\Games\osu!\Songs"
targetPath = "E:\music\osu! music"
tempFile = "temp.mp3"
songFileName = "$artist - $title.mp3"

invalidFilenameChars = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
errors = []

def main():
	songDirs = getSongPaths(osuSongPath)

	for songDir in songDirs:
		print songDir
		songMetaData = getSongMetaData(songDir)
		mp3Original = os.sep.join([songDir, songMetaData["AudioFilename"]])
		copyMp3(mp3Original)
		tempFileTag(songMetaData)
		tempFileMove(songMetaData)

	if len(errors) == 0:
		print "Script finished without any errors"
	else:
		print "Script finished with the following errors:"
		for e in errors:
			print e

def getSongPaths(path):
	listOfPaths = []
	for item in os.listdir(path):
		if os.path.isdir(os.sep.join([path, item])):
			listOfPaths.append(os.sep.join([path, item]))
	return listOfPaths

def getSongMetaData(path):
	metaData = {}

	for (dirpath, dirnames, filenames) in os.walk(path):
		for file in filenames:
			if file[-4:] == '.osu':
				#print os.sep.join([path, file])
				osuFile = open(os.sep.join([path, file]), "r")

				for line in osuFile:
					lineSplit = line.split(":")

					if lineSplit[0] == "Title":
						metaData["Title"] = lineSplit[1].replace("\n", "")
					elif lineSplit[0] == "Artist":
						metaData["Artist"] = lineSplit[1].replace("\n", "")
					elif lineSplit[0] == "AudioFilename":
						metaData["AudioFilename"] = lineSplit[1].replace("\n", "")[1:]

					if "Title" in metaData and "Artist" in metaData and "AudioFilename" in metaData:
						return metaData
						
def copyMp3(mp3):
	shutil.copy2(mp3, tempFile)

def tempFileTag(songMetaData):
	try:
		id3 = ID3v2(tempFile)
		setFrame(id3, "TPE1", songMetaData["Artist"])
		setFrame(id3, "TIT2", songMetaData["Title"])
		id3.commit()
	except:
		error("Unable to tag song: " + songMetaData["Artist"] + " - " + songMetaData["Title"])

def setFrame(id3, framename, value):
    new_f = id3.new_frame(framename)
    new_f.set_text(value)
    clearFrame(id3, framename)
    id3.frames.append(new_f)

def clearFrame(id3, framename):
    for frame in id3.frames:
        if(frame.fid == framename):
            id3.frames.remove(frame)

def tempFileMove(songMetaData):
	filename = songFileName
	filename = filename.replace("$artist", songMetaData["Artist"])
	filename = filename.replace("$title", songMetaData["Title"])

	for c in invalidFilenameChars:
		filename = filename.replace(c, "")

	shutil.move(tempFile, targetPath + os.sep + filename)

def error(msg):
	errors.append(msg)
	print "ERROR " + msg

main()