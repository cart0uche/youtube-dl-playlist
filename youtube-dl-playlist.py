#!/usr/bin/python
# youtube-dl-playlist


import os
import sys
import ConfigParser
import argparse
import glob
import shutil

dirVideoName = ".video"


def getPlaylistCode(config, playListName):
   for section in config.sections():
      for (key, value) in config.items(section):
         if playListName == key:
            return value
   print "%s was not found. Add this playlist in your playlist.ini file." % playListName
   return None


def setFolder(playlistName):
   if os.path.isdir(playlistName) == False:
      os.mkdir(playlistName)
      os.mkdir(os.path.join(playlistName, dirVideoName))
      print "Folder %s and %s created" % (playlistName, os.path.join(playlistName, dirVideoName))


def updatePlaylist(config, playlistName):
   # Get playlist
   playlistCode = getPlaylistCode(config, playlistName)
   if playlistCode == None:
      return

   # Create folder if needed
   setFolder(playlistName)

   # Call to youtube-dl
   os.chdir(os.path.join(playlistName, dirVideoName))
   os.system('youtube-dl --title --continue --ignore-errors --no-overwrite --no-post-overwrites --keep-video --extract-audio --audio-format=mp3 --audio-quality 0 ' + playlistCode)
   musicFiles = glob.glob('*.mp3')
   for musicFile in musicFiles:
      if not os.path.isfile(os.path.join(os.pardir, musicFile)):
         shutil.move(musicFile, os.pardir)
         open(musicFile,'w')
   videoTypes = ('*.flv', '*.mp4')
   videoFiles = []
   for videoType in videoTypes:
      videoFiles.extend(glob.glob(videoType))
   for videoFile in videoFiles:
      open(videoFile,'w')
   os.chdir(os.pardir)


def updatePlaylists(config, playlistsName):
   for playlistName in playlistsName:
      updatePlaylist(config, playlistName)


def updateAllPlaylist(config):
   for section in config.sections():
      for (key, value) in config.items(section):
         updatePlaylist(config, key)


def main():
   iniFile = "playlist.ini"

   # argpars
   parser = argparse.ArgumentParser(description='Download music from your Youtube playlist.')
   parser.add_argument('-a', '--all', action='store_true', help="Update all your playlist")
   parser.add_argument('-p', '--playlist', nargs='*', default=None, action='store', help="Update specific playlist")
   args = parser.parse_args()

   # check args
   if not (args.all or args.playlist):
      parser.error('No action required, add --all or --playlist')

   # Open playlist.ini
   config = ConfigParser.SafeConfigParser()
   if os.path.isfile(iniFile):
      config.read(iniFile)
   else:
      print "%s does not exist" % iniFile
      return

   # Update playlist
   if args.all :
      updateAllPlaylist(config)
   else:
      updatePlaylists(config, args.playlist)

if __name__ == "__main__":
   main()
