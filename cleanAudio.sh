pwd

echo "removing spaces"

##find -name "* *" -type f | rename 's/ /_/g'

echo "changing file types"

for i in *.mp3 ; do
    ffmpeg -y -i "$i" $(basename "${i/.mp3}").wav
		rm "$i"
done


echo "renaming files"
##rename 's/_Letter//' -v *.wav

rename 's/_sounds//' -v *.wav
rename 's/_sound//' -v *.wav

rename 's/_words//' -v *.wav

rename 's/\_word//' -v *.wav
rename 's/_pair//' -v *.wav
rename 's/_Syllable//' -v *.wav
rename 's/_syllable//' -v *.wav
rename 's/_feedback//' -v *.wav
rename 's/.wav.wav/.wav/' -f -v *.wav
