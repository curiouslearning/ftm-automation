#!/usr/bin/python
import os
import codecs
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import random
from sys import argv
import csv


def removeSpaces (lst):
	lst = [x.lstrip()for x in lst if x != ' ']
	lst = [x.strip() for x in lst if x != ' ']
	lst = [x.lower() for x in lst if x != ' ']
	return lst

def isGameplayText (string):
	if(string != 'BonusLetter'
	and string != 'FireWrongLetter'
	and string != 'MagnetLetter'
	and string != 'Shield'):
		return False
	else:
		return True


def makeFoil (levelletters, targetletter):
	foils = foilstones + levelletters + levelletters
	nf = targetletter
	while (nf == targetletter):
		nf = foils[random.randrange(len(foils))]

	return nf


########### MAIN ######
foilstones = []

indir = '/mnt/o/FTM/buildengine/level_generation/input_154/'
outdir = '/mnt/o/FTM/USENGLISH/levels_new/'
with open('/mnt/o/FTM/USENGLISH/subskillslevelgen.csv', 'rb') as csvfile:
	masterCSV = csv.reader(csvfile)
	next(masterCSV)
	rownum = 0
	for row in masterCSV:

		f = "level" + str(rownum) + ".xml"
		tree = ET.parse (os.path.join(indir,f))
		treeRoot = tree.getroot()
		group = int(treeRoot.get('LettersGroup'))
		print ("parsing " + f)
		leveltype = row[1]
		levelMainSkill = row[2]
		levelSubSkill = row[3]
		levelSubSkillAmount = row[4]
		#print(leveltype)
		if (leveltype == "match"):
			treeRoot.set('monsterInputType', "Letter")
		if (leveltype == "matchfirst"):
			treeRoot.set('monsterInputType', "LetterInWord")
		if (leveltype == "spell"):
			treeRoot.set('monsterInputType', "Word")

		treeRoot.set("mainskill",levelMainSkill)
		treeRoot.set("subskill",levelSubSkill)
		treeRoot.set("subskillAmt",levelSubSkillAmount)

		messylettersinlevel = row[0].split(",")
		lettersinlevel = [x.decode('utf8') for x in messylettersinlevel if x !=' ']
		lettersinlevel = removeSpaces(lettersinlevel)





		targets = []
		if (leveltype == "match"):
			for nl in lettersinlevel:
				nl = nl.strip('[]').lower()
				if (nl not in foilstones):
					foilstones.append(nl)
				targets.append(nl)

		if (leveltype == "matchfirst"):
			therest = []
			for nl in lettersinlevel:
				targ = nl[nl.find('(') + 1 : nl.find(')')]
				#print(targ)
				rl = nl[nl.find(')')+1:]
				therest.append(rl)
				targ = targ.strip('[]').lower()
				if (targ not in foilstones):
					foilstones.append(targ)
				targets.append(targ)
			print (therest)

		if (leveltype == "spell"):
			for nw in lettersinlevel:
				targ = []
				hw = ""
				lp = 0
				while (lp < len(nw) ):
					testlet = nw[lp]
					if (testlet == '['):
						lp+=1
						testlet = nw[lp]
						while (testlet != ']' and lp < len(nw)):
							hw += nw[lp]
							lp+=1
							testlet = nw[lp]
						targ.append(hw)
						hw = ""
					else:
						targ.append(testlet)
					lp += 1
				targets.append(targ)

		print(targets)


		puzzles = treeRoot[0]
		pnum = 0
		for puzzle in puzzles:
			puzzle.set("spawnIds","20,75,15,23,74,14,11,12,60")
			target = targets[pnum]
			req = "MonsterRequiredLetters"
			reqLets = puzzle.find(req)
			dragStones = puzzle.find("Stones")

			if (leveltype == "match" or leveltype == "matchfirst"):

				reqLet = reqLets.find('string')
				oldTarget = reqLet.text
				reqLet.text = target


				for child in dragStones.findall('string'):
					spawnList = [];
					if(not isGameplayText(child.text)):
						if(child.text == oldTarget):
							child.text = target
						else:
							child.text = makeFoil(targets,target)
			if (leveltype == "matchfirst"):
				allLet = "MonsterAllLetters"
				alllets = puzzle.find(allLet)
				e = ET.SubElement(alllets, 'string')
				e.text = "X"
				for ela in therest[pnum]:

					e = ET.SubElement(alllets, 'string')
					e.text = ela
			if(leveltype =="spell"):
				for child in list(reqLets):
					reqLets.remove(child)
				for tl in target:
					e = ET.SubElement(reqLets, 'string')
					e.text = tl

				random.shuffle(target)

				for child in list(dragStones):
					dragStones.remove(child)
				for tl in target:
					e = ET.SubElement(dragStones, 'string')
					e.text = tl
					e = ET.SubElement(dragStones, 'string')
					stonetext = tl
					while (stonetext in target):
							stonetext = foilstones[random.randrange(len(foilstones))]
					e.text =stonetext








			pnum += 1


		tree = ET.ElementTree(treeRoot)
		filename = outdir + f
		tree.write(open(filename, 'wb'), encoding = 'utf-8')
		tree = ""
		rownum += 1
csvfile.close()
