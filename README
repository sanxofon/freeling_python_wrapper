Freeling Python Wrapper & Quick Server

That's a long name for a simple couple of scripts.

1. analyzer.py - Freeling Python Wrapper (FPW)
	It creates a connection with the analizer executable in the /bin folder of the 3 & 4 versions of the great c++ package for natural language process, may be the best there is in spanish (in the wild). It runs the program and leaves it open. One can later send some phrase or word and it will return an array of all the words analyzed: tokenized, tagged, etc. See Freeling Usermanual to see all the pretty things it does.
	You can send as many phrases, long texts or even txt files, and the wrapper will keep the dictionaries loaded so the response is impresively fast.
	You can close the connection and make another one. You can configure the executing command (big security issue! for test prouporses only!), and you can edit the analyzer.cfg config file with any plain text editor. There is some info in the comments of the config file itself and, I repeat, read the Freeling Usermanual to learn the details (look for page 79).
	For the people who aren't familiar with natural language processing, you can begin by learning this:
		By default, if you make no changes to the config file and send a None as command, FPW will create a connection in spanish that if you send to it a word like: "perras", it wil return you the array: [ "perras", "perro", "NCFP000", "1"]. The first element will be the word you inputed, the second will be the root word without gender or number modifications, the third will be the EAGLES POS Tag of the word (in this case: Female Plural Noun) and the fourth is the ocurrence of that tag subject to context.
		The phrase: "Las perras que ladran a la luna están de vacaciones." will return an array like this:
		[
			["Las", "el", "DA0FP0", "0.970954", "lo", "PP3FPA00", "0.0289466", "la", "NCMP000", "9.94728e-005"],
			["perras", "perro", "NCFP000", "1"],
			["que", "que", "PR0CN000", "0.562517", "que", "CS", "0.437483"],
			["ladran", "ladrar", "VMIP3P0", "1"],
			["a", "a", "SPS00", "0.996023", "a", "NCFS000", "0.00397693"],
			["la", "el", "DA0FS0", "0.972269", "lo", "PP3FSA00", "0.0277039", "la", "NCMS000", "2.74025e-005"],
			["luna", "luna", "NCFS000", "1"],
			["están", "estar", "VAIP3P0", "1"],
			["de", "de", "SPS00", "0.999984", "de", "NCFS000", "1.61912e-005"],
			["vacaciones", "vacaciones", "NCFP000", "0.5", "vacación", "NCFP000", "0.5"],
			[".", ".", "Fp", "1"]
		]