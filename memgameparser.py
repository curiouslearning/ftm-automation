#!/usr/bin/python
import os
from sys import argv
import shutil

pairs = ["2_1","2_2","2_3","2_4","2_5","2_6","3_1","3_2","3_3","3_4","3_5","3_6","4_2","4_3","4_4","4_5","5_1","5_2","5_3","5_5","5_6","6_1"]

if (len(argv) <= 1):
	print "oh no, no base dir given"
else:
	print argv[1]

basecompdir = '/mnt/o/FTM/buildengine/Image Tiles/'
wordstocomp = []
for root, dirs, filenames in os.walk (basecompdir):
	for f in filenames:
		tempfnm = f
		curword = tempfnm[5:-4]
		wcpl = [curword,[],[],root + f]
		wordstocomp.append(wcpl)

oldunitybasegeneric = '/mnt/o/FTM/'
unityassbase = oldunitybasegeneric + argv[1] + "/unitywork/Feed The Monster/Assets"
artlookone = unityassbase + "/Art/MemoryGame/"

for root, dirs, filenames in os.walk (artlookone):
	for fn in filenames:
		for cw in wordstocomp:
			if (cw[0] in fn and "meta" not in fn and "flip" not in fn and "pattern" not in fn and "icon" not in fn):
				if (root == artlookone):
					wiloc = root + fn
				else:
					wiloc =  root + "/" + fn
				cw[1].append(wiloc)

soundlookone = unityassbase + "/Sounds/MiniGame/Memory/"
for root, dirs, filenames in os.walk (soundlookone):
	for fn in filenames:
		for cw in wordstocomp:
			if (cw[0] in fn and "meta" not in fn and "flip" not in fn.lower() and "match" not in fn.lower()):
				if (root == soundlookone):
					wiloc = root + fn
				else:
					wiloc =  root + "/" + fn
				cw[2].append(wiloc)

soundlooktwo = unityassbase + "/Resources/Sounds/Voice/Words/"
for root, dirs, filenames in os.walk (soundlooktwo):
	for fn in filenames:
		for cw in wordstocomp:
			if (cw[0] in fn and "meta" not in fn and "flip" not in fn.lower() and "match" not in fn.lower()):
				if (root == soundlooktwo):
					wiloc = root + fn
				else:
					wiloc =  root + "/" + fn
				cw[2].append(wiloc)

usablewords = []
for mw in wordstocomp:
	if (len(mw[1]) > 0 and len(mw[2]) > 0):

		usablewords.append(mw)

i = 0
if (len(usablewords) >= len(pairs)):
	print "copying memory game assets"
	pairassetbase = "/mnt/o/ftm/langpackdata/" + argv[1] + "/art/memg/"
	for pairroot in pairs:
		uw = usablewords[i]
		shutil.copyfile(uw[1][0],pairassetbase + "memg_" + pairroot + "_a.jpg")
		shutil.copyfile(uw[2][0],pairassetbase + "memg_" + pairroot + "_c.wav")
		shutil.copyfile(uw[3],pairassetbase + "memg_" + pairroot + "_b.jpg")
		i+=1
