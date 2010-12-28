#!/usr/bin/env python

#Author: Victor Fontes Costa 
#Email: vitufc [at] g mail [dot] com
#Website: http://victorfontes.com
#January 2010

#This script will make playlists based on info thats avalilable on lastfm`s public API
# you`ll need appscrpit: sudo easy_install appscript


from appscript import *
from urllib import urlopen
from xml.dom import minidom

METODOS = {
'loved_tracks':('user.getlovedtracks','track'),
'weekly_tracks':('user.getweeklytrackChart', 'track'),
'top_tracks':('user.gettoptracks', 'track'),
'top_albums':('user.gettopalbums','album'),
'top_artists':('user.gettopartists', 'artist'),
'weekly_albums':('user.getweeklyalbumChart','album'),
'weekly_artists':('user.getweeklyartistChart', 'artist'),
}


class LastfmPublicData():
	def __init__(self, user, api="b25b959554ed76058ac220b7b2e0a026"):
		self.user = user
		self.api = api
	def __get_data(self, method):
		URL = "http://ws.audioscrobbler.com/2.0/?method=%s&user=%s&api_key=%s" % (METODOS[method][0], self.user, self.api)
		return minidom.parse(urlopen(URL))
	def strings_by_method(self, method):
		dom = self.__get_data(method)
		musicas = []
		for album in dom.getElementsByTagName(METODOS[method][1]):
			str = album.getElementsByTagName("name")[0].firstChild.nodeValue
			str += " " + album.getElementsByTagName("name")[1].firstChild.nodeValue
			musicas.append(str)
			print str
		return musicas
		
class ITunesPlaylistManager():
	def __init__(self, playlist):
		self.playlist = playlist
		self.itunes = app('iTunes')
		self.playlists = self.itunes.user_playlists()
		if not self.playlist in [p.name() for p in self.playlists]:
			self.itunes.make(new=k.user_playlist, with_properties={k.name: self.playlist})
		self.itunes.reveal(self.itunes.playlists[self.playlist])
	
	def find_tracks_in_library(self, t):
		try: return (self.itunes.search(self.playlists[0], for_=unicode(t)))
		except UnicodeDecodeError: pass
		
	def add_tracks(self, track):
		if hasattr(track, '__iter__'): 
			self.itunes.add(track[0].location(), to=self.itunes.playlists[self.playlist])
		else:
			self.itunes.add(track.location(), to=self.itunes.playlists[self.playlist])

lastfm = LastfmPublicData(u'come_here')
tracks_str = lastfm.strings_by_method(u'loved_tracks')
itunes = ITunesPlaylistManager(u'Loved Tracks')
for track_str in tracks_str:
	track = itunes.find_tracks_in_library(track_str)
	itunes.add_tracks(track)
