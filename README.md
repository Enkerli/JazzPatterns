# JazzPatterns
> Converting melodic patterns into performance

The original list of melodic patterns comes from [A Pattern History of Jazz](https://jazzomat.hfm-weimar.de/pattern_history/) from the [Dig That Lick project](http://dig-that-lick.eecs.qmul.ac.uk) within the [Jazzomat Research Project](https://jazzomat.hfm-weimar.de). The [data used](https://jazzomat.hfm-weimar.de/download/download.html) is available under the [Open Database License (ODbL) v1.0](https://opendatacommons.org/licenses/odbl/1.0/) from [Open Data Commons](https://opendatacommons.org).

The list of patterns is available in a CSV file with:
* The pattern as a series of intervals (in semitones)
* An ID from the original database
* The number of instances of the pattern contained within the corpus
The list is ordered in decreasing order of "popularity" within the corpus.

This repo contains the script used to convert each pattern into a MIDI file which includes some data for expression on each note (velocity and CC02, breath control).
The MIDI files produced by the script are also in the repo. Individual MIDI files are named with the index number of the pattern, a database ID, and the number of instances present in the corpus. A file combining all the patterns in a single track is also included.

The original intention for this work is to curate a list of “Jazz Licks” to practice on a MIDI controller or acoustic instrument, in order to “build vocabulary”.

A recording of an automated performance of those initial patterns is [released on Vimeo](https://vimeo.com/896031262) under a [CC BY-SA 4.0 license](http://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1).

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://vimeo.com/896031262">Jazz Patterns</a> by <span property="cc:attributionName">Alex Enkerli</span> is licensed under <a href="http://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution-ShareAlike 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a></p>
