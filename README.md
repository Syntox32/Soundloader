#Soundloader
Download and take your favorite tracks with you, offline!

If you enjoy the work of the artists you listen to, please go support them in a way that you feel
is appropriate(e.g. purchase it).

Inspired by this <a href="https://github.com/013/Soundcloud-Downloader">repo</a>

##How do I use it?
If any number of arguments are given it will move on to the argument parser.

If the script is ran without giving it any arguments, it will go CLI mode and ask you to input a link to a single track.
````
If multiple actions are given it will be prioritized in this order:
  1.  likes  
  2.  sets  
  3.  single track    
```
```
usage: soundloader.py [-h] [-l] [-u USERNAME] [-s SET] [-t TRACK] [-c COUNT]  
                  [-f FOLDER] [-x]  
                  
example: python soundloader.py -t https://soundcloud.com/<user>/<awesome track>
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
	
	--https [optional]
			Use HTTPS when querying the API, slower than normal HTTP
```
## Requirements
You need any version of <strong>Python 3</strong> running on your computer. It <em>should</em> also work with <strong>Python 2.7</strong>
