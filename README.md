youtube-dl-playlist
===================

Requirements:
-------------
  - [youtube-dl](https://github.com/rg3/youtube-dl):
it must be up to date, check it with this command (two times if needed)
<blockquote>youtube-dl -U</blockquote>

  - BeautifulSoup, on Ubuntu :
<blockquote>sudo apt-get install python-beautifulsoup</blockquote>



Usage:
------
  - With GUI: <blockquote>python youtube-dl-playlist.py</blockquote>
  - Without GUI : <blockquote>python youtube-dl-playlist.py [name_playlist | all]</blockquote>

File playlist.ini:
------------------

When you launch the script the first time, no playlists is record in the playlist.ini file.
So it will ask your Youtube identifier to construct automatically your playlist.

<blockquote>
test=PLivBbUaI8nnSU_k_y2WYVgX8H5SDJpFeX
</blockquote>
  - test is the name of your playlist
  - PLivBbUaI8nnSU_k_y2WYVgX8H5SDJpFeX is the reference of your playlist known by Youtube.
You will find it on the Youtube webpage of your playlist, example :
<blockquote>
https://www.youtube.com/playlist?list=PLivBbUaI8nnSU_k_y2WYVgX8H5SDJpFeX
</blockquote>
  
