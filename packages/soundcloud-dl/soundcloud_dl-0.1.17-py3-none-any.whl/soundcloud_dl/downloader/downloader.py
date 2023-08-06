import soundcloud, requests, os, re, sys
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC
from mutagen.id3 import ID3, TIT2, TPE1, TCON, TDRC, APIC
from soundcloud import resource
from time import sleep
from contextlib import closing
import socket, json

from .config import secret

class soundcloudDownloader(object):
	def __init__(self, args=None):
		self.args = args
		self.url = args.url
		self.dirname = args.dir
		self.client = soundcloud.Client(client_id=secret)
		self.session = requests.Session()
		self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=2))
		self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries=2))
		self.completed = 0

	def Resolver(self, action, data, resolve=False):
		try:
			if resolve:
				data = self.client.get(str(action), url=str(data))
			else:
				data = self.client.get(str(action), user_id=data)
		except (requests.exceptions.ConnectionError,
				TypeError,
				socket.error):
			print("Connection error. Retrying in 15 seconds.")
			sleep(15)
			self.Resolver(action, data, resolve)
		except requests.exceptions.HTTPError:
			print("Invalid URL.")
			sys.exit(0)
		except KeyboardInterrupt:
			print("Exiting.")
			sys.exit(0)
		if data is not None:
			return data

	def connectionHandler(self, url, stream=False, timeout=15, payload={}):
		try:
			response = self.session.get(url, stream=stream, timeout=timeout, params=payload)
			assert response.status_code == 200
			return response
		except (requests.exceptions.ConnectionError,
				TypeError,
				socket.error):
			print("Connection error. Retrying in 15 seconds.")
			sleep(15)
			self.connectionHandler(url, stream)
		except (AssertionError,
				requests.exceptions.HTTPError):
			print("Connection error or invalid URL.")
			return
		except KeyboardInterrupt:
			print("Exiting.")
			sys.exit(0)

	def getSingleTrack(self, track):
		if isinstance(track, resource.Resource):
			track = track.fields()
		metadata = {
			'title':str(track.get('title', '')),
			'artist': track['user']['username'],
			'year': str(track.get('release_year', '')),
			'genre': str(track.get('genre', ''))
		}
		if track['downloadable']:
			try:
				filename = (track['user']['username'] + ' - ' + \
				track['title'] + '.' + track['original_format'])
				url = track['download_url'] + '?client_id='+secret
			except:
				filename = (track['user']['username'] + ' - ' + \
				track['title'] + '.mp3')
				try:
					url = track['stream_url'].split('?')[0] + '?client_id='+secret
				except KeyError:
					url = 'https://api.soundcloud.com/tracks/' + \
						str(track['id']) + '/stream?client_id=' + browser_id 
		else:
			filename = (track['user']['username'] + ' - ' + \
			track['title'] + '.mp3')
			try:
				url = track['stream_url'].split('?')[0] + '?client_id='+secret
			except KeyError:
				url = 'https://api.soundcloud.com/tracks/' + \
					str(track['id']) + '/stream?client_id=' + browser_id
		try:
			new_filename = self.getFile(filename, url)
			self.completed += 1
			self.tagFile(new_filename, metadata, track['artwork_url'])
		except KeyboardInterrupt:
			sys.exit(0)
		except:
			track['downloadable'] = False
			self.getSingleTrack(track)

	def getPlaylists(self, playlists):
		if isinstance(playlists, resource.ResourceList):
			for playlist in playlists:
				for track in playlist.tracks:
					self.getSingleTrack(track)
		else:
			print("%d tracks found in this playlist" % (len(playlists.tracks)))
			for index, track in enumerate(playlists.tracks):
				if self.checkTrackNumber(index):
					self.getSingleTrack(track)  
	
	def checkTrackNumber(self, index):
		if self.args.limit is not None:
			if self.completed == self.args.limit:
				return False
		if self.args.include is not None:
			if index + 1 not in self.args.include:
				if not self.args.range:
					return False
		if self.args.exclude is not None:
			if index + 1 in self.args.exclude:
				print("Skipping track " + str(index))
				return False
		if self.args.range is not None:
			if not self.args.range[0] <= index + 1 <= self.args.range[1]:
				if self.args.include:
					if index + 1 not in self.args.include:
						return False
				else:
					return False
		return True

	def getUploadedTracks(self, user):
		tracks = self.Resolver('/tracks', user.id)
		for index, track in enumerate(tracks):
			if self.checkTrackNumber(index):
				self.getSingleTrack(track)              

	def getRecommendedTracks(self, track, no_tracks):
		recommended_tracks_url = "https://api-v2.soundcloud.com/tracks/"
		recommended_tracks_url += str(track.id) + "/related?client_id="
		recommended_tracks_url += str(secret) + "&limit="
		recommended_tracks_url += str(no_tracks) + "&offset=0"
		recommended_tracks = self.session.get(recommended_tracks_url)
		recommended_tracks = json.loads(recommended_tracks.text)['collection']
		for track in recommended_tracks:
			self.getSingleTrack(track)

	def getLikedTracks(self):
		liked_tracks = self.Resolver('/resolve', self.url + '/likes', True)
		print(str(len(liked_tracks)) + " liked track(s) found.")
		for index, track in enumerate(liked_tracks):
			if self.checkTrackNumber(index):
				self.getSingleTrack(track)

	def progressBar(self, done, file_size):
		percentage = ((done/file_size)*100)
		sys.stdout.flush()
		sys.stdout.write('\r')
		sys.stdout.write('[' + '#'*int((percentage/5)) + ' '*int((100-percentage)/5) + '] ')
		sys.stdout.write(' | %.2f' % percentage + ' %')

	def validateName(self, name):
		return  re.sub('[\\/:*"?<>|]', '_',name)

	def getFile(self, filename, link, silent=False):
		new_filename = self.validateName(filename)
		if link is not None:
			if silent:
				try:
					#print( link
					link = link.replace('https', 'http')
					with closing(self.connectionHandler(link, True, 15)) as response:
						with open(new_filename, 'wb') as file:
							for chunk in response.iter_content(chunk_size=1024):
								if chunk:
									file.write(chunk)
									file.flush()
					return new_filename
#                except (socket.error,
#                        requests.exceptions.ConnectionError):
#                    self.getFile(filename, link, silent)
				except KeyboardInterrupt:
					print("\nExiting.")
					sys.exit(0)
				except:
					os.remove(filename)
					sleep(15)
					self.getFile(filename, link, silent)

			print("\nConnecting to stream...")
			print(link)
			with closing(self.connectionHandler(link, True, 5)) as response:
				print("Response: "+ str(response.status_code))
				file_size = float(response.headers['content-length'])
				if os.path.isfile(new_filename):
					if os.path.getsize(new_filename) >= float(file_size):
						print(new_filename + " already exists, skipping.")
						self.file_done = False
						return new_filename
					else:
						os.remove(new_filename)
						print("Incomplete download, restarting.")
				print("File Size: " + '%.2f' % (file_size/(1000**2)) + ' MB')
				print("Saving as: " + new_filename)
				done = 0
				try:
					with open(new_filename, 'wb') as file:
						for chunk in response.iter_content(chunk_size=1024):
							if chunk:
								file.write(chunk)
								file.flush()
								done += len(chunk)
								self.progressBar(done, file_size)
					if os.path.getsize(new_filename) < float(file_size):
						os.remove(new_filename)
						print("\nConnection error. Restarting in 15 seconds.")
						sleep(15)
						self.getFile(filename, link, silent)
					print("\nDownload complete.")
					self.file_done = True
					return new_filename
				except (socket.error,
						requests.exceptions.ConnectionError):
					os.remove(new_filename)
					self.getFile(filename, link, silent)
				except KeyboardInterrupt:
					print("\nExiting.")
					os.remove(new_filename)
					raise KeyboardInterrupt
		else:
			return new_filename

	def tagFile(self, filename, metadata, art_url):
		if not self.file_done:
			return
		image = None
		if art_url is not None:
			self.getFile('artwork.jpg', art_url, True)
			try:
				with open('artwork.jpg', 'rb') as file:
					image = file.read()
			except:
				pass
		if filename.endswith('.mp3'):
			audio = MP3(filename, ID3=ID3)
			try:
				audio.add_tags()
			except:
				pass
			if image:
				audio.tags.add(
					APIC(
						encoding=3,
						mime='image/jpeg',
						type=3,
						desc=u'Cover',
						data=image
					)
				)
			audio.tags["TIT2"] = TIT2(encoding=3, text=(metadata.get('title', '')))
			try:
				audio.tags["TPE1"] = TPE1(encoding=3, text=metadata.get('artist', ''))
			except:
				pass
			audio.tags["TDRC"] = TDRC(encoding=3, text=(metadata.get('year', '')))
			audio.tags["TCON"] = TCON(encoding=3, text=(metadata.get('genre', ' ')))
			audio.save()
		elif filename.endswith('.flac'):
			audio = FLAC(filename)
			try:
				audio.add_tags()
			except:
				pass
			audio.tags['title'] = metadata['title']
			audio.tags['artist'] = metadata['artist']
			audio.tags['year'] = metadata['year']
			audio.tags['genre'] = metadata['genre']
			audio.tags.add(
				APIC(
					encoding=3,
					mime='image/jpeg',
					type=3,
					desc=u'Cover',
					data=image
				)
			)
			audio.save()
		elif filename.endswith('.m4a'):
			audio = MP4(filename)
			try:
				audio.add_tags()
			except:
				pass
			covr = []
			covr.append(MP4Cover(image, MP4Cover.FORMAT_JPEG))
			audio.tags['covr'] = covr
			audio.tags['title'] = metadata['title']
			audio.tags['artist'] = metadata['artist']
			#audio.tags['year'] = metadata['year']
			audio.tags['genre'] = metadata['genre']
			audio.save()
		if os.path.isfile('artwork.jpg'):
			os.remove('artwork.jpg')

	def getTopTracks(self):
		print("Downloading top {} tracks".format(self.args.top))
		url_params = {
			'limit': self.args.top if self.args.top <= 50 else 10,
			'genre': 'soundcloud:genres:' + self.args.genre,
			'kind': 'top',
			'client_id': browser_id
		}
		url = 'https://api-v2.soundcloud.com/charts'
		response = self.connectionHandler(url, payload=url_params)
		if response:
			tracks = json.loads(response.text)['collection']
			for index, track in enumerate(tracks):
				if self.checkTrackNumber(index):
					self.getSingleTrack(track['track'])
		return

	def getNewTracks(self):
		print("Downloading {} trending tracks".format(self.args.new))
		url_params = {
			'limit': self.args.new if self.args.new <= 50 else 10,
			'genre': 'soundcloud:genres:' + self.args.genre,
			'kind': 'trending',
			'client_id': browser_id
		}
		url = 'https://api-v2.soundcloud.com/charts'
		response = self.connectionHandler(url, payload=url_params)
		if response:
			tracks = json.loads(response.text)['collection']
			for index, track in enumerate(tracks):
				if self.checkTrackNumber(index):
					self.getSingleTrack(track['track'])
		return

	def Download(self):
		if self.url is None:
			if self.args.top:
				self.getTopTracks()
			elif self.args.new:
				self.getNewTracks()
			else:
				print("No URL entered.")
			return
		elif 'soundcloud' not in self.url:
			print("Invalid URL")
			return
		try:
			if os.path.isdir(self.dirname):
				os.chdir(str(self.dirname))
			else:
				print("Directory doesn't exist.")
				return
			print("Connecting ... ")
		except WindowsError:
			print("Invalid Directory")
			return
		data = self.Resolver('/resolve', self.url, True)
		if data is not None:
			if isinstance(data, resource.Resource):
				if data.kind == 'user':
					print("User profile found.")
					folder = self.validateName(data.username)
					if not os.path.isdir(folder):
						os.mkdir(folder)
					os.chdir(os.path.join(os.getcwd(), str(folder)))
					print("Saving in: " + os.getcwd())
					if self.args.all:
						self.getUploadedTracks(data)
						self.getLikedTracks()
					elif self.args.likes:
						self.getLikedTracks()
					else:
						self.getUploadedTracks(data)
				elif data.kind == 'track':
					if 'recommended'  in self.url: 
						no_tracks = self.args.limit if self.args.limit else 5
						print("Downloading " + str(no_tracks) + " related tracks")
						self.getRecommendedTracks(data, no_tracks)
					else:
						print("Single track found.")
						print("Saving in: " + os.getcwd())
						self.getSingleTrack(data)
				elif data.kind == 'playlist':
					print("Single playlist found.")
					folder = self.validateName(data.user['username'])
					if not os.path.isdir(folder):
						os.mkdir(folder)
					os.chdir(os.path.join(os.getcwd(), str(folder)))
					self.getPlaylists(data)
			elif isinstance(data, resource.ResourceList):
				if self.url.endswith('likes'):
					print("Downloading liked tracks.")
					user_url = self.url[:-6]
					user = self.Resolver('/resolve', user_url, True)
					folder = self.validateName(user.username)
				else:
					folder = self.validateName(data[0].user['username'])
				if not os.path.isdir(folder):
					os.mkdir(folder)
				os.chdir(os.path.join(os.getcwd(), str(folder)))
				print("Saving in: " + os.getcwd())
				if data[0].kind == 'playlist':
					print("%d playlists found." % (len(data)))
					self.getPlaylists(data)
				elif data[0].kind == 'track':
					for index, track in enumerate(data):
						if self.checkTrackNumber(index):
							self.getSingleTrack(track)
		else:
			print("Network error or Invalid URL.")
			sys.exit(0)