#!/usr/bin/python
import os
import codecs
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import random
from sys import argv
import csv
import itertools



finalouttext = ""
with open('/mnt/o/FTM/buildengine/hc.csv', 'rb') as csvfile:

	indir = '/mnt/o/FTM/langpackdata/HINDI/levels/'
	for root, dirs, filenames in os.walk (indir):
		for f in filenames:
			tmpfnm = f

			lvlnum = tmpfnm.strip("levxm.")
			if int(lvlnum) < 10:
				finalouttext += "0" + str(lvlnum)
			else:
				finalouttext += str(lvlnum)
			finalouttext += ", "
			tree = ET.parse (os.path.join(root,f))
			treeRoot = tree.getroot()
			group = int(treeRoot.get('LettersGroup'))
			phid = int(treeRoot.get('HideCallout'))
			finalouttext += "group " + str(group) + ", "
			if phid == -1:
				finalouttext += "prompt stays visible, "
			else:
				finalouttext += "prompt hidden after " + str(phid) + " seconds, "
			mtype = treeRoot.get('monsterInputType')

			segments = treeRoot[0]
			count = 0
			for subTree in segments:
				count = count +1
				req = "MonsterRequiredLetters"
				reqLets = subTree.find(req)
				reqLet = reqLets.find('string')
				letnum = int(reqLet.text)
				row = next(itertools.islice(csv.reader(csvfile), letnum))

				acar = row[1]

				finalouttext += acar + " "
			finalouttext += "\n"
	fout = open("hindi_structure.csv","w");
	fout.write(finalouttext)
	fout.close()
