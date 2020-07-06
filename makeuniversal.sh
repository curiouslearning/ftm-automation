#!/bin/bash


#SET THIS INFO BEFORE RUNNING
keystorefile="/PATH/TO/FILE.keystore"
keystorealias="ALIAS"
keystorepw="P4SSWORD"

#check for input aab argument
if [ -z "$1" ]
  then
    echo "no input aab location supplied as argument"
		echo "usage:"
		echo "./makeuniversal.sh /path/to/input.aab"
		exit 1
fi
#check for bundletool
if [ ! -f "bundletool-all-0.10.3.jar" ]
	then
		echo "need to run in same directory as bundletool-all-0.10.3.jar"
		exit 1
fi

#parsing language name
inputfile=$1
inputname="$(basename $inputfile)"
prefix='FeedTheMonster'
suffix='.aab'
partial=${inputname/#$prefix}
langname=${partial/%$suffix}
echo "parsing "$langname

#parsing version code
versionnum="$(java -jar bundletool-all-0.10.3.jar dump manifest --bundle=$inputfile --xpath=/manifest/@android:versionCode)"
echo "android version code "$versionnum

#running bundletool
echo "generating apk, this will take a minute"
java -jar bundletool-all-0.10.3.jar build-apks --bundle=$inputfile --output=o.apks --ks=$keystorefile --ks-pass=pass:$keystorepw --ks-key-alias=$keystorealias --key-pass=pass:$keystorepw --mode=universal

#extracting apk
mv o.apks o.zip
unzip o.zip -d outputzip
cd outputzip
mv universal.apk "../ftm_"$langname"_v"$versionnum"_universal.apk"
echo "output: ftm_"$langname"_v"$versionnum"_universal.apk"
cd ../

#cleaning up files
rm o.zip
rm -r outputzip
