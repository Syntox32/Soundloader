# Soundloader
Download and take your favorite tracks with you, offline!

If you enjoy the work of the artists you listen to, please go support them in a way that you feel
is appropriate(e.g. purchase it).

Inspired by this <a href="https://github.com/013/Soundcloud-Downloader">repo</a>

## Installation

##### Option one (recommended)
If you have pip working and installed, it's pretty straight forward.

```
pip install git+https://github.com/Syntox32/Soundloader
```

##### Option two

Download the project in some way (.zip or git), `cd` to the directory and run.

```
python setup.py install
```
---

You can now run the script by typing this in the console of your choice.
```
soundloader.py
```

Run this for help.

```
soundloader.py --help
```

## Example usage

Downloading 20 likes:

```
soundloader.py --likes --username <username> --count 20
```
---

Downloading a single track:
```
soundloader.py --track https://soundcloud.com/<user>/<awesome_track>
```
---

Downloading a track to a folder:
```
soundloader.py --folder C:\Music\Folder --track https://soundcloud.com/<user>/<awesome_track>
```
---

Downloading a set of tracks, and create the download directory if it doesn't exist with `-x`
```
soundloader.py --folder C:\Music\Folder -x --set https://soundcloud.com/<username>/sets/<set_name>
```

## Arguments

Starting the script without passing it any arguments, it will launch in an *interactive mode*.

```
usage: soundloader.py [-h] [-l] [-u USERNAME] [-s SET] [-t TRACK] [-c COUNT]
				[-f FOLDER] [-x] [-o] [--https]
```

```
arguments:
	-h, --help            
			Show this help message and exit
			
	-l, --likes           
			Download likes from any account, requires a given username
			
	-s, --set SET     
			Link to a set to download
			
	-t, --track TRACK
			Link to a track to download
			
	-u, --username USERNAME [required if '--likes' is used]
			Used when retrieving likes, if the 'likes' argument 
			is given this must also, else the script will throw an error.
			
	-c, --count COUNT [optional]
			How many tracks are to be downloaded, if none is
			given it will download all available
			
	-f, --folder FOLDER [optional]
			Where to download the track(s), if none is 
			given the directory will be the current directory
			
	-x, --create-directory [optional]
			Create folder if none exists

	-o, --overwrite [optional]
			Overwrite already existing songs
	
	--https [optional]
			Use HTTPS when querying the API, slower than normal HTTP
```

If the script is ran without giving it any arguments, it will go CLI mode and ask you to input a link to a single track.
````
If multiple actions are given it will be prioritized in this order:
  1.  likes  
  2.  sets  
  3.  single track    
```

## Requirements
You need any version of <strong>Python 3.x</strong> running on your computer. It <em>should</em> also work with <strong>Python 2.7.x</strong>
