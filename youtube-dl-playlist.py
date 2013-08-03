#!/usr/bin/python
# -*- coding: utf-8 -*-
# youtube-dl-playlist

import os
import sys
import ConfigParser
import argparse
import glob
import shutil
import urllib
import PyZenity
from BeautifulSoup import BeautifulSoup


VIDEO_DIRECTORY = '.video'
CONFIG_MUSIC = 'Music'

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
		os.mkdir(os.path.join(playlist_name, VIDEO_DIRECTORY))
		print "Folder %s and %s created" % (playlist_name, os.path.join(playlist_name, VIDEO_DIRECTORY))


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
	os.chdir(os.path.join(playlist_name, VIDEO_DIRECTORY))
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

def genere_playslists_code(youtube_user_name, ini_file):
	page_html = urllib.urlopen('https://www.youtube.com/user/%s' % youtube_user_name)
	soup = BeautifulSoup(page_html.read())
	soup_channel_id = soup.find('meta', attrs={'itemprop': 'channelId'})
	channel_id = soup_channel_id['content']
	print 'channel_id = ' + channel_id

	page_html = urllib.urlopen('https://www.youtube.com/channel/%s/videos?feature=guide&view=1' %channel_id)
	soup = BeautifulSoup(page_html.read())
	soup_channel_id = soup.findAll('div', attrs={'data-context-item-user': youtube_user_name, 'data-context-item-type': 'playlist'})

	playlists_code = [(playlist['data-context-item-title'], playlist['data-context-item-id']) for playlist in soup_channel_id]
	print playlists_code

	if len(playlists_code) == 0:
		PyZenity.Warning('No playlist has been added with user %s.\nLogin is case sensitive and your playlists must be public.' % youtube_user_name)
		return

	config = ConfigParser.RawConfigParser()
	config.read('playlist.ini')
	for playlist_code in playlists_code:
		config.set(CONFIG_MUSIC, playlist_code[0], playlist_code[1])

	with open(ini_file, 'wb') as configfile:
		config.write(configfile)


def main():
	# argpars
	parser = argparse.ArgumentParser(description='Download music from your Youtube playlist.')
	parser.add_argument('-a', '--all', action='store_true', help="Update all your playlist")
	parser.add_argument('-p', '--playlist', nargs='*', default=None, action='store', help="Update specific playlist")
	args = parser.parse_args()

	# Open playlist.ini
	ini_file = "playlist.ini"
	config = ConfigParser.SafeConfigParser()
	if os.path.isfile(ini_file):
		config.read(ini_file)
	else:
		sys.exit("Playlist file does not exist")

	output_path = config.get("Config", "output_path")
	if output_path not in ["", None]:
		if os.path.isdir(output_path) is False:
			sys.exit(output_path + " does not exist")
		else:
			os.chdir(output_path)

	if len(config.options(CONFIG_MUSIC)) == 0:
		youtube_user_name = PyZenity.GetText(text="Enter your Youtube login (no password required): ", entry_text="", password=False)
		genere_playslists_code(youtube_user_name, ini_file)
		config.read(ini_file)

	if args.all:
		updateAllPlaylist(config)

	elif args.playlist:
		updatePlaylists(config, args.playlist)

	else:
		print config.options(CONFIG_MUSIC)
		playlists = [["", playlist] for playlist in config.options(CONFIG_MUSIC)]
		list_result = PyZenity.List(["", "playlist"], title="Select one or more playlist", boolstyle="checklist", data=playlists)
		if list_result is None or list_result == ['']:
			sys.exit()

		progression_callback = PyZenity.Progress(text="Downloading videos and converting in mp3")

		for i, music in enumerate(list_result):
			progression_callback(100*i/len(list_result), "Download playlist : " + music)
			updatePlaylists(config, [music])

		progression_callback(100, "Enjoy.")

if __name__ == "__main__":
	main()
