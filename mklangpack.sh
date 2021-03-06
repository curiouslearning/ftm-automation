#!/bin/bash

lpbase="/mnt/o/ftm/lpd/ftm-languagepacks"
cd $lpbase

pwd

newdir=$1

if [ -z "$1" ]
  then
    echo "No argument supplied"
		exit 1
fi

if [ -z "$2" ]
	then
		baselook="unitywork"
	else
		baselook=$2
fi

echo "making "$newdir

mkdir -p $newdir
cd $newdir
newlpdata=$(pwd)
mkdir -p "charimg"
mkdir -p "levels"
mkdir -p "sounds/letters"
mkdir -p "sounds/words"
mkdir -p "sounds/feedbacks"
mkdir -p "sounds/other"
mkdir -p "art/feedbacks"
mkdir -p "art/titles"
mkdir -p "art/memg"

mydata="/mnt/o/ftm"

cd $mydata
if [ -d $newdir ]
then
	cd $newdir
	pwd

	echo "copying levels"
	cd $baselook"/Feed The Monster/Assets/Resources/Gameplay/Levels"
	cp *.xml $newlpdata"/levels"

	cd ../../
	echo "copying sounds"
	cd "Sounds/Voice"
	cp letters/*.wav $newlpdata"/sounds/letters"
	cp letters/*.WAV $newlpdata"/sounds/letters"
	cp words/*.wav $newlpdata"/sounds/words"
	cp words/*.WAV $newlpdata"/sounds/words"
	if [ -d "Syllables" ]
	then
		cp syllables/*.wav $newlpdata"/sounds/letters"
		cp syllables/*.wav $newlpdata"/sounds/words"
	fi
	cp Feedbacks/Positive/*.wav $newlpdata"/sounds/feedbacks"
	cp Instructions/*.wav $newlpdata"/sounds/other"
	cp Feedbacks/Positive/*.WAV $newlpdata"/sounds/feedbacks"
	cp Instructions/*.WAV $newlpdata"/sounds/other"

	cd ../../
	if [ -d "charimg" ]
	then
		echo "copying charimgs"
		cp charimg/*.png $newlpdata"/charimg"
	fi

	cd ../

	function copyimages {
		cp *amazing*.png $newlpdata"/art/feedbacks" 2>/dev/null || :
		cp *fantastic*.png $newlpdata"/art/feedbacks" 2>/dev/null || :
		cp *great*.png $newlpdata"/art/feedbacks" 2>/dev/null || :
		cp *well*.png $newlpdata"/art/feedbacks" 2>/dev/null || :
		cp *Amazing*.png $newlpdata"/art/feedbacks" 2>/dev/null || :
		cp *Fantastic*.png $newlpdata"/art/feedbacks" 2>/dev/null || :
		cp *Great*.png $newlpdata"/art/feedbacks" 2>/dev/null || :
		cp *Well*.png $newlpdata"/art/feedbacks" 2>/dev/null || :
		cp *treasure*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *Treasure*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *select*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *Select*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *letter*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *Letter*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *friend*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *Friend*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *parents*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *Parents*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp SEL_*.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *base.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *v03_logo.png $newlpdata"/art/titles" 2>/dev/null || :
		cp *$newdir*.png $newlpdata"/art/titles" 2>/dev/null || :
	}

	cd "Art/Splash"
	echo "copying images"
	copyimages
	cd ../
	cd "Titles"
	copyimages
	if [ -d "Instructions" ]
	then
		cd "Instructions"
		copyimages
		cd ../
	fi
	if [ -d "ParentsProgression" ]
	then
		cd "ParentsProgression"
		copyimages
		cd ../
	fi
	cd "Feedbacks/Positive"
	copyimages

	echo "parsing memory game assets"
	python /mnt/o/ftm/buildengine/memgameparser.py $newdir

	cd $newlpdata
	echo "-----"
	echo "checking missing files:"

	function checkmissing {
		if [ ! -f "$1" ]
		then
			echo "missing "$1 >> /mnt/o/ftm/buildengine/missing$newdir.txt
		fi
	}

	function checklist {
		if [ -f "/mnt/o/ftm/buildengine/missing$newdir.txt" ]
		then
			rm  "/mnt/o/ftm/buildengine/missing$newdir.txt"
		fi

		while IFS= read -r line
		do
		  checkmissing "$line"
		done < /mnt/o/ftm/buildengine/$1


	}
	cd art
	cd feedbacks
	checklist artfeedbacks.txt
	cd ../
	cd memg
	checklist artmemg.txt
	cd ../../
	cd sounds
	cd other
	checklist soundsother.txt



else
	echo "no existing unity branch for "$newdir
fi
