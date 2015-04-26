#Soundloader
This is a script created for taking your Soundcloud tracks and playlists offline.

If you enjoy the work of the artists you listen to, please go support them in a way that you feel
is appropriate(e.g. purchase it).

##How do I use it?
If the script is ran without giving it any arguments, it will go CLI mode and ask you to input a link to a single track.  
If any number of arguments are given it will move on to the argument parser.    

````
If multiple actions are given it will be prioritized in this order:
  1.  likes  
  2.  sets  
  3.  single track    
```
```
usage: soundloader.py [-h] [-l] [-u USERNAME] [-s SET] [-t TRACK] [-c COUNT]  
                  [-f FOLDER] [-x]  
```
```
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
