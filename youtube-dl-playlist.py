#!/usr/bin/python
# -*- coding: utf-8 -*-
# youtube-dl-playlist

import os
import sys
import ConfigParser
import argparse
import glob
import shutil
import Tkinter
import ttk


dirVideoName = ".video"


def getPlaylistCode(config, playListName):
   for section in config.sections():
      for (key, value) in config.items(section):
         if playListName == key:
            return value
   print "%s was not found. Add this playlist in your playlist.ini file." % playListName
   return None


def createFolder(playlistName):
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
   createFolder(playlistName)

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
   os.chdir(os.pardir)


def updatePlaylists(config, playlistsName):
   for playlistName in playlistsName:
      updatePlaylist(config, playlistName)


def updateAllPlaylist(config):
   for section in config.sections():
      for (key, value) in config.items(section):
         updatePlaylist(config, key)


class DisplayInterface(Tkinter.Tk):

   def __init__(self,parent,config):
      Tkinter.Tk.__init__(self,parent)
      self.parent = parent
      self.config = config
      self.initialize()

   def initialize(self):
      self.grid()

      self.message = Tkinter.Message(self,text="Select a playlist :",width=200)
      self.message.grid(padx=10,pady=10,column=0,row=0,sticky='W')

      var = Tkinter.StringVar()
      playListvar = [p for p in self.config.options('Music')]
      var.set(playListvar[0])
      self.play = ttk.OptionMenu(self.parent, var, *playListvar)
      self.play.grid(padx=10,pady=10,column=0,row=1,sticky='WENS')

      buttonDownload = Tkinter.Button(self,text=u"Download",command=lambda x=var:self.OnButtonClick(var.get()))
      buttonDownload.grid(column=0,row=2)

      self.title("youtube-dl-playlist")
      self.protocol("WM_DELETE_WINDOW", self.closeWindows)
      self.mainloop()

   def OnButtonClick(self,playList):
      print "# %s selected" % playList
      updatePlaylist(self.config, playList)

   def closeWindows(self):
      self.destroy()


def main():
   # argpars
   parser = argparse.ArgumentParser(description='Download music from your Youtube playlist.')
   parser.add_argument('-a', '--all', action='store_true', help="Update all your playlist")
   parser.add_argument('-p', '--playlist', nargs='*', default=None, action='store', help="Update specific playlist")
   parser.add_argument('-g', '--gui', action='store_true', help="Display graphic interface")
   args = parser.parse_args()

   # check args
   if not (args.all or args.playlist):
      args.gui=1

   # Open playlist.ini
   iniFile = "playlist.ini"
   config = ConfigParser.SafeConfigParser()
   if os.path.isfile(iniFile):
      config.read(iniFile)
   else:
      sys.exit("playlist file does not exist")

   if args.gui:
      app = DisplayInterface(None, config=config)
   elif args.all:
      updateAllPlaylist(config)
   elif args.playlist:
      updatePlaylists(config, args.playlist)

if __name__ == "__main__":
   main()
