#!/usr/bin/env python3
import unittest
import os.path, os
from soundloader import Soundloader

class TestSoundloaderClass(unittest.TestCase):

	def setUp(self):
		"""
		I just need a comment here for consistency
		"""
		self.sl = Soundloader("b45b1aa10f1ac2941910a7f0d10f8e28", "tests/", True)

	def test_resolve(self):
		"""
		Effectivly tests _request, _fetch_json and _resolve at the same time
		"""
		json = self.sl._resolve("https://soundcloud.com/majorlazer/major-lazer-dj-snake-lean-on-feat-mo")
		self.assertEqual(json["id"], 193781466)

		print("Prepare expected error...")
		json = self.sl._resolve("https://soundcloud.com/majorlazer/major-LOLOLOLon-feat-mo")
		self.assertEqual(json, None)

	def test_download_single_track(self):
		"""
		Simple test of a single track download
		"""
		song_ = "https://soundcloud.com/majorlazer/major-lazer-dj-snake-lean-on-feat-mo"
		ret = self.sl.download_track(song_)
		self.assertTrue(ret)
		f1 = os.path.isfile(os.path.join(self.sl.save_folder, "Major Lazer & DJ Snake - Lean On (feat MØ).mp3"))
		self.assertTrue(f1)
		if f1: os.remove(os.path.join(self.sl.save_folder, "Major Lazer & DJ Snake - Lean On (feat MØ).mp3"))

	def test_download_set(self):
		"""
		Simple test of downloading a couple of songs from a set
		"""
		set_ = "https://soundcloud.com/majorlazer/sets/apocalypse-soon"
		ret = self.sl.download_set(set_, 2)
		f1 = os.path.isfile(os.path.join(self.sl.save_folder, "Major Lazer - Aerosol Can (feat Pharrell Williams).mp3"))
		f2 = os.path.isfile(os.path.join(self.sl.save_folder, "Major Lazer - Come On To Me (feat Sean Paul).mp3"))
		self.assertTrue(f1 and f2)
		self.assertTrue(ret)
		if f1 and f2:
			os.remove(os.path.join(self.sl.save_folder, "Major Lazer - Aerosol Can (feat Pharrell Williams).mp3"))
			os.remove(os.path.join(self.sl.save_folder, "Major Lazer - Come On To Me (feat Sean Paul).mp3"))

	# def test_download_likes(self): pass # not needed, all the same functions are used in the set function

	def test_get_user_id(self):
		"""
		Another simple test for getting a user id
		"""
		user = "majorlazer"
		id_ = self.sl.get_user_id(user)
		self.assertEqual(id_, str(12148579))

if __name__ == "__main__":
	unittest.main()