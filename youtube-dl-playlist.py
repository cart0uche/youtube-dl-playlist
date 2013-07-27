#!/usr/bin/python
# -*- coding: utf-8 -*-
# youtube-dl-playlist

import os
import sys
import ConfigParser
import argparse
import glob
import shutil
import PyZenity


dirVideoName = ".video"


def getPlaylistCode(config, playlist_name):
	for section in config.sections():
		for (key, value) in config.items(section):
			if playlist_name == key:
				return value
	print "%s was not found. Add this playlist in your playlist.ini file." % playlist_name
	return None


def createFolder(playlist_name):
	if os.path.isdir(playlist_name) is False:
		os.mkdir(playlist_name)
		os.mkdir(os.path.join(playlist_name, dirVideoName))
		print "Folder %s and %s created" % (playlist_name, os.path.join(playlist_name, dirVideoName))


def updatePlaylist(config, playlist_name):
	# Get playlist code
	print "Update playlist " + playlist_name
	playlist_code = getPlaylistCode(config, playlist_name)
	if playlist_code is None:
		print playlist_name + " has no code. Check your playlist.ini"
		return

	# Create folder if needed
	createFolder(playlist_name)

	# Call to youtube-dl
	audio_format = config.get("Config", "audio_format") if config.get("Config", "audio_format") not in ["", None] else "mp3"
	audio_quality = config.get("Config", "audio_quality") if config.get("Config", "audio_quality") not in ["", None] else "0"
	command = 'youtube-dl --title --continue --ignore-errors --no-overwrite --no-post-overwrites --keep-video --extract-audio --audio-format ' + audio_format + ' --audio-quality ' + audio_quality + ' ' + playlist_code
	print command
	os.chdir(os.path.join(playlist_name, dirVideoName))
	os.system(command)

	# Move audio file into user directory and replace by empty one
	musicFiles = glob.glob('*.' + audio_format)
	for musicFile in musicFiles:
		if not os.path.isfile(os.path.join(os.pardir, musicFile)):
			shutil.move(musicFile, os.pardir)
			open(musicFile, 'w')

	# replace all videos files by empty files, to not dowload them again.
	videoTypes = ('*.flv', '*.mp4')
	videoFiles = []
	for videoType in videoTypes:
		videoFiles.extend(glob.glob(videoType))
	for videoFile in videoFiles:
		open(videoFile, 'w')
	os.chdir(os.pardir)
	os.chdir(os.pardir)


def updatePlaylists(config, playlistsName):
	for playlistName in playlistsName:
		updatePlaylist(config, playlistName)


def updateAllPlaylist(config):
	for section in config.sections():
		for (key, value) in config.items(section):
			updatePlaylist(config, key)


def main():
	# argpars
	parser = argparse.ArgumentParser(description='Download music from your Youtube playlist.')
	parser.add_argument('-a', '--all', action='store_true', help="Update all your playlist")
	parser.add_argument('-p', '--playlist', nargs='*', default=None, action='store', help="Update specific playlist")
	args = parser.parse_args()

	# Open playlist.ini
	iniFile = "playlist.ini"
	config = ConfigParser.SafeConfigParser()
	if os.path.isfile(iniFile):
		config.read(iniFile)
	else:
		sys.exit("Playlist file does not exist")

	output_path = config.get("Config", "output_path")
	if output_path not in ["", None]:
		if os.path.isdir(output_path) is False:
			sys.exit(output_path + " does not exist")
		else:
			os.chdir(output_path)

	if args.all:
		updateAllPlaylist(config)

	elif args.playlist:
		updatePlaylists(config, args.playlist)

	else:
		print config.options('Music')
		playlists = [["", playlist] for playlist in config.options('Music')]
		list_result = PyZenity.List(["", "playlist"], boolstyle="checklist", data=playlists)

		progression_callback = PyZenity.Progress(text="Downloading videos and converting in mp3")

		for i, music in enumerate(list_result):
			progression_callback(100*i/len(list_result), "Download playlist : " + music)
			updatePlaylists(config, [music])

		progression_callback(100, "Enjoy.")

if __name__ == "__main__":
	main()
