#!/usr/bin/env python3

"""
	Take Soundcloud with you offline!

	If you enjoy the work of the artists you listen to, please go support them in a way that you feel
	is appropriate(e.g. purchase it).

	If the script is ran without giving it any arguments, it will go CLI mode and ask you
	to input a link to a single track.

	If any number of arguments are given it will move on to the argument parser.

	If multiple actions are given it will be prioritized in this order:
		1. likes
		2. sets
		3. single track

	usage: soundloader.py [-h] [-l] [-u USERNAME] [-s SET] [-t TRACK] [-c COUNT]
	                  [-f FOLDER] [-x]

	arguments:
		-h, --help
				Show this help message and exit

		-l, --likes
				Download the likes, requires a given username

		-s, --set SET
				Link to a set to download

		-t, --track TRACK
				Link to a track to download

		-u, --username USERNAME [required if '--likes' is used]
				Used when retrieving likes, if the likes argument
				is given this must also, else the script will throw an error.

		-c, --count COUNT [optional]
				How many tracks are to be downloaded, if none is
				given it will download all available

		-f, --folder FOLDER [optional]
				Where to download the track(s), if none is
				given the directory will be the current directory

		-x, --create-directory [optional]
				Create folder if none exists
"""

import sys, os, os.path, argparse

# https://code.google.com/p/stagger/
# from stagger.id3 import *

import json, re
from urllib.request import urlopen
from string import ascii_lowercase, ascii_uppercase

class Soundloader(object):
	def __init__(self, clientid=None, save_folder=None, create_folder=None):
		"""
		Initialize a soundloader class with a client ID or API key
		"""
		self.client_id = clientid

		if save_folder:
			self.save_folder = self._get_download_folder(save_folder, create_folder)
		else:
			self.save_folder = None

		self.RESOLVE_URL = "https://api.soundcloud.com/resolve.json?url=%s&client_id=%s"
		self.LIKES_URL = "https://api-v2.soundcloud.com/users/%s/track_likes?client_id=%s&limit=%s"
		self.SONG_URL = "https://api.soundcloud.com/i1/tracks/%s/streams?client_id=%s"
		self.VALID_CHARS = ascii_lowercase + ascii_uppercase + "æøåÆØÅ" + " &_-0123456789()"

	def download_track(self, song_url):
		"""
		Download a single track
		"""
		data = self._resolve(song_url)
		if data is None or "id" not in data:
			print("Could not retrieve track data.")
			return False
		track_id = data["id"]
		fname = self._get_trackname(data)
		self._download_id(track_id, fname)
		return True

	def download_set(self, set_url, count=0):
		"""
		Download a set of tracks
		"""
		data = self._get_set(set_url)
		if data is None:
			print("Could not retrieve set data.")
			print("Are you sure this playlist is public?")
			return False
		set_len = len(data)
		if count > 0:
			set_len = count
		for i in range(0, set_len):
			track_id = data[i]["id"]
			fname = self._get_trackname(data[i])
			self._download_id(track_id, fname)
		return True

	def download_likes(self, username, count=0):
		"""
		Download n number of likes from a given username
		"""
		userid = self.get_user_id(username)
		likes = self._get_likes(userid, count)
		if likes is None:
			print("Could not retrieve data.")
			return False
		num_likes = len(likes)
		if count > 0:
			num_likes = count
		for i in range(0, num_likes):
			if likes[i]["track"] is None:
				continue
			track_id = likes[i]["track"]["id"]
			fname = self._get_trackname(likes[i]["track"])
			self._download_id(track_id, fname)
		return True

	def get_user_id(self, username):
		"""
		Return the user ID of a given username
		"""
		resp = self._resolve("https://soundcloud.com/%s" % username)
		return str(resp["id"])

	def _download_id(self, track_id, filename):
		"""
		Download and save a track by the given track ID and filename
		"""
		json = self._fetch_json(self.SONG_URL % (str(track_id), self.client_id))
		if not "http_mp3_128_url" in json:
			print("No http stream for track with ID: %s" % str(track_id))
			return False
		dl_link = json["http_mp3_128_url"]
		print("Downloading track id: %s" % str(track_id))
		track_data = self._request(dl_link).read()
		if track_data is None:
			print("Could not download track with ID: %s" % str(track_id))
			return False
		self._save_track(filename, track_data)
		print("Track download completed.")
		return True

	def _resolve(self, url):
		"""
		Return a list of JSON data for the given URL
		"""
		return self._fetch_json(self.RESOLVE_URL % (url, self.client_id))

	def _get_likes(self, user_id, limits):
		"""
		Return the list of likes for the given user ID
		"""
		j =  self._fetch_json(self.LIKES_URL % (str(user_id), self.client_id, str(limits)))
		if j is None:
			return None
		return j["collection"]

	def _get_set(self, set_url):
		"""
		Return a list of all tracks in a set
		"""
		j = self._fetch_json(self.RESOLVE_URL % (str(set_url), self.client_id))
		if j is None:
			return None
		return j["tracks"]

	def _get_trackname(self, track_json):
		"""
		Return operating system friendly filename with the artist and track name
		"""
		title = track_json["title"]
		username = track_json["user"]["username"]
		if "-" not in title:
			title = username + " - " + title
		return self._safe_filename(title)

	def _save_track(self, filename, data):
		"""
		Save track data to file
		"""
		try:
			if self.save_folder:
				filename = os.path.join(self.save_folder, filename)
			with open(filename, "wb+") as f:
				f.write(data)
		except IOError as e:
			print("IOError:", e)

	def _safe_filename(self, path):
		"""
		Return operating system friendly filename
		"""
		filename = "".join(ch for ch in path if ch in self.VALID_CHARS)
		return filename + ".mp3"

	def _encode_str(self, string):
		"""
		Return a utf-8 encoded string
		"""
		return str(string).encode("utf-8")

	def _fetch_json(self, url):
		"""
		Return JSON data for a given URL
		"""
		try:
			req = self._request(url)
			if req is None:
				return None
			data = req.read().decode("utf-8")
			return json.loads(data)
		except Exception as e:
			print("Error:", e)
		return None

	def _request(self, url):
		"""
		Return a request for a given URL, or print the appropriate error message
		"""
		err = None
		try:
			req = urlopen(url)
			return req
		except Exception as e:
			err = str(e)
			if "404" in err: err = "[ERR 404]: I have no clue what you are trying to do.."
			elif "401" in err: err = "[ERR 401]: You were not authorized, wtf."
			elif ["502", "503"] in err: err = "[ERR 502/503]: It probably wasn't your fault, kid."
		finally:
			if err is not None:
				print(err)
		return None

	def _get_download_folder(self, directory, create):
		"""
		Return the path of a valid download directory
		"""
		if create:
			full_path = os.path.abspath(directory)
			if not os.path.isdir(directory):
				print("Creating directory:\n  %s" % full_path)
				os.mkdir(full_path)
			else:
				print("%s already exists, continuing.." % directory)
			return full_path
		else:
			isdir = os.path.isdir(directory)
			if not isdir:
				print("The given folder is not a valid directory:", directory)
				sys.exit(0)
			else:
				full_path = os.path.abspath(directory)
				print("Saving to directory:\n  %s" % full_path)
				return full_path

def main():
	"""
	Take Soundcloud with you offline!
	"""
	apikey = "b45b1aa10f1ac2941910a7f0d10f8e28"

	if len(sys.argv) == 1:
		track = input("Input a link to the track you wish to download:\n")
		sl = Soundloader(apikey)
		sl.download_track(track)
		sys.exit(0)

	parser = argparse.ArgumentParser(description="Take Soundcloud with you offline")
	parser.add_argument("-l", "--likes", action="store_true", help="Download the likes, requires a given username")
	parser.add_argument("-u", "--username", help="Used when retrieving likes")
	parser.add_argument("-s", "--set", help="Link to a set to download")
	parser.add_argument("-t", "--track", help="Link to a track to download")
	parser.add_argument("-c", "--count", type=int, help="How many tracks are to be downloaded")
	parser.add_argument("-f", "--folder", help="Where to download the track(s)")
	parser.add_argument("-x", "--create-directory", action="store_true", help="Create folder if none exists")
	args = parser.parse_args()

	sl = Soundloader(apikey, args.folder, args.create_directory)

	if args.likes:
		print("Downloading likes..")
		if args.username is None:
			parser.print_help()
			sys.exit(0)
		print("Downloading likes for '%s'.." % args.username)
		if args.count is not None:
			sl.download_likes(args.username, args.count)
		else:
			sl.download_likes(args.username)
		print("Done!")
	elif args.set:
		print("Downloading set..")
		if args.count is not None:
			sl.download_set(args.set, args.count)
		else:
			sl.download_set(args.set)
		print("Done!")
	elif args.track:
		print("Downloading track '%s'" % args.track)
		sl.download_track(args.track)
		print("Done!")
	else:
		print("Well, you have to type in something!\n")
		parser.print_help()
		sys.exit(0)

if __name__ == "__main__":
	main()
