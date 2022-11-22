# FeedTheMonster Level Generation

## Building a levelgen.csv
The levelgen file is a comma-separated value file where each row after the first defines a level in the game. A sample_levelgen.csv is provided as an example of a levelgen for an English-language game with 150 levels, utilizing all level types. This sample is also available in [spreadsheet form](https://docs.google.com/spreadsheets/u/3/d/1PyWYpfwg04fhrcnkSNFM7cSQTNj34XV3NS_iAMe8IfY).

Each line takes the form *targets, type, notes*.

The target characters that the learner will match on each level are specified in the levelgen, while the foil (incorrect) stones are filled in from target characters that have been taught so far.

### Targets syntax
**Every level must have exactly five targets**.

Targets are comma-separated, and the group of all five targets is enclosed as quotes.

On matchfirst levels, the character in the word that needs to be matched by the learner is enclosed in parenthesis. For instance, if the targets list includes `"(f)ox"`, the word fox will be presented as a prompt, but the sound file f.wav will be played and the learner will only need to drag the f stone to the monster, at which the puzzle will be completed.

On spell levels, an entire word is presented as a prompt, and the learner must match each letter in order. For instance, if the targets list includes `"fox"`, the word fox will be presented as a prompt, with the sound file fox.wav, and the learner will need to drag the f stone, then the o stone, then the x stone to complete the puzzle.

#### Complex Characters as Targets
If your language of Feed the Monster is designed to teach complex characters, such as the blended sound "th", these should be enclosed in brackets. For instance, if the targets list is `"a, b, t, h, [th]"`, the letter t will be presented (with the sound file t.wav) as the third prompt, the letter h will be presented (with the sound file h.wav) as the fourth prompt, and the blend "th" will be presented as the fifth prompt (with the sound th.wav). Complex characters will be present together on a stone - meaning that there will be a stone that says "th" and can be dragged up. **If multi-character blends are not enclosed with brackets, they will be treated as a word made up of individual letters.**

You can use complex characters in matchfirst and spell levels as well - a matchfirst target of `"([th])ose"` will prsent the word "those" as a prompt, play the th.wav sound file, and require the learner to drag up the th stone. On the other hand, a spell target of `"[th]ose"` will play the those.wav sound file, and require the learner to drag up the th stone, then the o stone, then the s stone, and then the e stone.

It is possible to include multiple complex characters in a word - for instance, a spell target of `"[sh][eep]"` will play the audio file sheep.wav, and require the learner to drag up the sh stone and then the eep stone.


### Type syntax
A one-word type description is used to define what type of level it is.

Level type | Meaning
----- | -----
match | An individual letter is presented as a prompt, the learner matches the letter
matchfirst | A word is presented as a prompt, the learner matches the first letter
spell | A word is presented as a prompt, the learner matches each letter of the word in order.

### Notes syntax
Notes are optional text at the end of each line that are not processed by the parselevelgen.py file

## Running parselevelgen.py
Before running the python script that parses a levelgen, be sure to edit lines 39, 40, and 41, which define the location of the levelgen to parse, the location of the template files to use, and the location of the directory to output generated levels. Once these locations have been set, no additional arguments are needed, so you can run
`python parselevelgen.py`

## Template folders
The folder input_154 contains a set of level template files that are used by the parselevelgen.py script to generate new levels. Their location must be defined in the parselevelgen.py script. The python script makes a copy of the template levels, ans then replaces the target/option values with values from the language-specific levelgen.

The templates are defined so that levels gradually go from two to three stones to choose from at the beginning to more choices at the end- if you want to change the number of choices present, editing the template xml files in the input_154 directory would allow you to define the "shape" of the levels, but not their content.
