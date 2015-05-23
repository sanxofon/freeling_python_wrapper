<h3>Freeling Python Simple Wrapper & Quick Server (FPSW&QS)</h3>
<i>That's a long name for a simple couple of scripts.</i>
<br><br>
<b>1. analyzer.py - Freeling Python Simple Wrapper (FPSW)</b>
<br>
	  It creates a connection with the analizer executable in the /bin folder of the 3 & 4 versions of the great c++ package for natural language process, may be the best there is in spanish (in the wild). It runs the program and leaves it open. One can later send some phrase or word and it will return an array of all the words analyzed: tokenized, tagged, etc. See Freeling Usermanual to see all the pretty things it does.
<br>
	  You can send as many phrases, long texts or even txt files, and the wrapper will keep the dictionaries loaded so the response is impresively fast.
<br>
	  You can close the connection and make another one. You can configure the executing command (big security issue! for test prouporses only!), and you can edit the analyzer.cfg config file with any plain text editor. There is some info in the comments of the config file itself and, I repeat, read the Freeling Usermanual to learn the details (look for page 79).
<br>
	  For the people who aren't familiar with natural language processing, you can begin by learning this:
<br>
		By default, if you make no changes to the config file and send a None as command, FPSW will create a connection in spanish that if you send to it a word like: <i>perras</i>, it wil return you the array: <i>[ "perras", "perro", "NCFP000", "1"]</i>. The first element will be the word you inputed, the second will be the root word without gender or number modifications, the third will be the EAGLES POS Tag of the word (in this case: Female Plural Noun) and the fourth is the ocurrence of that tag subject to context.
<br>
    The phrase: <i>Las perras que ladran a la luna están de vacaciones.</i> will return an array like this:
<pre>
[
	["Las", "el", "DA0FP0", "0.970954"],
	["perras", "perro", "NCFP000", "1"],
	["que", "que", "CS", "0.437483"],
	["ladran", "ladrar", "VMIP3P0", "1"],
	["a", "a", "SPS00", "0.996023"],
	["la", "el", "DA0FS0", "0.972269"],
	["luna", "luna", "NCFS000", "1"],
	["están", "estar", "VAIP3P0", "1"],
	["de", "de", "SPS00", "0.999984"],
	["vacaciones", "vacaciones", "NCFP000", "0.5"],
	[".", ".", "Fp", "1"]
]
</pre>
<b>2. server.py - Quick Server (QS)</b>
<br>
This will make a quick BaseHTTPServer in <i>localhost:8000</i> that if recieves <i>?q=Las perras que ladran a la luna están de vacaciones.</i> it will give you that array mentioned before as a JSON.
<br>
You can run it like this:
<pre>
>> python server.py
</pre>
That's quick!
<br><br>
<b>Dependencies</b>
<br>
1. Freeling 3.1/4dev
<br>
 &nbsp; &nbsp; It works with both <i>windows</i> (win7 tested) or <i>linux</i> (debian jessie tested) versions of the freeling binary package.
<br>
2. Python 2.7
<br>
 &nbsp; &nbsp; <i>Haven't tested in py3</i>
<br><br>
<b>Known trouble downloading freeling</b>
<br>
If you have python installed and you download freeling 3.1 to c:\freeling31 folder, this script will run without much modification, but the freeling package is a big and complicated download. Use curl, wget or something to try to download it until it succeeds. You could use something like this to download the windows x64 binary package (it will try many time until it succeeds, i'm afraid):
<pre>
wget -v -t 0 http://devel.cpl.upc.edu/freeling/downloads/33
</pre>
<br>
<b>Why?</b>
<br>
I wrote this because in fkn windows 7 the compiled analyzer.exe that comes with the binary version of the freeling 3.1 package doesn't keep the conection open in server mode, so you have to load the dictionaries (a couple of seconds) for every query. That's a lot of time if you multipy by thousands of querys done by a simple script. For instance you could create a root word search by doing a fulltext copy of a text with all the words rooted, so the search for <i>perras</i> in an analyzed repository will return (may be as a second level rank value?) all <i>perro</i> related results. You could also do only so for nouns, adjectives and verbs. Neat!
<br>
I <i>analyzed</i> 30,000 descriptions of a repository objects in one day with this simple script and some simple php code. Most of the time was spent in making a good regex that cleans the input from unwanted non utf-8 and such characters but keeping as many as posible valid characters (even in russian) of the original string. That was a test and retest work. I am a dumb lazy person.
<br><br>
<b>For testing prouporses only!</b>
<br>
If you wan't to run a freeling analyzer server for real production use you could use the java wrapper the comes in the freeling package and mount it as a webapp in tomcat or something like that. You should not use the linux analizer pre compiled executable in server mode. It's very unstable. But in your pc or temporarly you could use this! 
<br><br>
<i>This is free for all, send pull requests and bla, bla, bla...</i>
