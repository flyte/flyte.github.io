Title: Ministry of Recycled Sound
Tags: python

[TOC]

An advert for the latest Ministry of Sound album came on TV the other day. As usual, they played samples of some of the tunes you'll get on the album - one of which was [Darude - Sandstorm](http://youtu.be/PSYxT9GM0fQ). It occurred to me that all of the Ministry of Sound albums I can remember watching adverts for contained this one track. This made me wonder how many other songs kept getting put on the MoS albums repeatedly.

What I wanted to see was a list of tracks sorted by how many times they had appeared on a Ministry of Sound album. I had a hunch that Sandstorm would be at the top.

## Fetch the database

[FreeDB](http://www.freedb.org/) is a license-free database for use in looking up track listings for CDs. We start by [downloading the whole database](http://www.freedb.org/en/download__database.10.html) (roughly 800MB bzipped file) and extracting its contents to the filesystem:

    :::bash
    tar xjvf freedb-complete-20140101.tar.bz2

Producing the following file structure:

    .
    ├── blues
    │   ├── 0008a512
    │   ├── 000a8112
    │   ├── 000a9612
    <snip>
    ├── classical
    │   ├── 00073614
    │   ├── 00088112
    │   ├── 00092526
    <snip>
    ├── country
    etc.

Each file (`000a9612`, `00073614` etc.) represents a single CD and they're organised into genre directories. The files contain, among other things, the track listing of the CD.

## Search for Ministry of Sound CDs

Since there are over three million CDs listed in FreeDB, the files needed paring down a little.

    :::bash
    grep -ir "ministry of sound" . | perl -n -e '/(^.+?):/ && print $1."\n"' | uniq > ministry.txt

This grep command searches recursively and case-insensitively for the exact string "ministry of sound". It will normally output something like

    ./blues/4512b117:DTITLE=Various Artists / Ministry of Sound: Sessions Ten

but all we care about is the file name (4512b117) so we use perl regex to capture and print it with a newline appended. This will produce duplicate file names, so we pipe it to uniq and finally output to a file called ministry.txt. This command took a long time to complete, but would have been a whole lot slower had we have done it using Python.

Now we have a list of Ministry of Sound CDs, we copy the files into their own directory since we don't care what genre they're listed as.

    :::bash
    mkdir ministry
    cat ministry.txt | xargs -I {} cp {} ministry/

We now have all of the CD files in one directory so we can move on to using Python to figure out the answer to our question.

## Parse the CD files

The first issue we need to solve is that some of the track names are too long to fit on a single line in the CD file.

    TTITLE13=David Morales and Larent Garnier / Ministry of Sound Dance Pa
    TTITLE13=rty Fragment

We create a function which parses each line of the CD file and creates a dictionary of the keys and values. If a key is already in the dictionary, it will concatenate the value onto it.

    :::python
    def parse_cd(filename, replacements={}):
        """
        Takes the path to a FreeDB CD file and parses all
        key/value pairs into a dictionary.
        """
        lines = {}
        with open(filename, "r") as f:
            for line in f.readlines():
                # Remove newline chars
                line = line.rstrip()
                # Ignore any comments or lines without an equals in
                if "=" not in line or line.startswith("#"):
                    continue

                # Extract the keys and values, forcing the values to be
                # lower case
                eq_index = line.index("=")
                key = line[:eq_index]
                value = line[eq_index+1:].lower()

                # Take a dictionary of strings to search and replace eg.
                # {" (original mix)": "", " - ": " / "}
                for old, new in replacements.items():
                    value = value.replace(old, new)

                # Check for the existence of a partial line in the
                # dictionary first and then append the rest of the
                # value if it exists.
                if key in lines:
                    lines[key] += value
                else:
                    lines[key] = value
        return lines


Within this function we also replace certain characters and strings. Some of the delimiters are inconsistent in FreeDB, so we make an effort to replace them all with `/`. We also remove any occurrences of ` (original mix)` since these are indeed the original tracks.

    :::python
    REPLACEMENTS = {
        " (original mix)": "",
        " - ": " / ",
        "-" : " / ",
        " / ": "/"
    }

We create a `REPLACEMENTS` constant to put at the top of our script and pass it to the `parse_cd` function at runtime.

## Count up the tracks

We now have all the tools we need to count up the tracks.

    :::python
    if __name__ == "__main__":
        tracks_count = {}

        for filename in os.listdir(DB_DIR):
            # Parse the CD
            cd = parse_cd(os.path.join(DB_DIR, filename), REPLACEMENTS)
            # Extract the tracks
            tracks = [cd[x] for x in cd.keys() if x.startswith("TTITLE")]

            for track in tracks:
                # If the track has appeared already, increment its counter
                # otherwise add it and start it off at 1.
                if track in tracks_count:
                     tracks_count[track] += 1
                else:
                    tracks_count[track] = 1

        # Finally, sort the tracks_count dictionary by amount of appearances
        for track_count in sorted(tracks_count.items(), key=lambda x: x[1]):
            print "%s: %s" % track_count

We create a `tracks_count` dictionary to store the amount of appearances of each track. Next, we list the directory which contains all of the CD files and parse the files. We grab the tracks (the key always starts with `TTITLE`)  and either increment an existing entry in tracks_count or set it to `1` if it is its first appearance on a CD. Finally, we sort the `tracks_count` dictionary incrementally so that the most common track appears last on our console output and then print the whole lot.

## The Results

    ~/workspace/ministry $ python ministry.py | tail -n 30
    iio/rapture: 9
    atb/9pm (till i come): 9
    deepest blue/give it away: 9
    armand van helden/mymymy: 10
    tomcraft/loneliness: 10
    underworld/born slippy: 10
    shakedown/at night: 10
    supermode/tell me why: 10
    double 99/rip groove: 10
    yves larock/rise up: 10
    jakatta/american dream: 10
    alter ego/rocker: 10
    jaydee/plastic dreams: 10
    switch/a bit patchy: 10
    kings of tomorrow/finally: 10
    junior jack/stupidisco: 11
    static revenger/happy people: 11
    strike/u sure do: 11
    paul johnson/get get down: 11
    fedde le grand/put your hands up for detroit: 12
    ministry of sound / the annual 2005 disc #2: 12
    public domain/operation blade: 12
    dee dee/forever: 13
    eric prydz/call on me: 14
    chill out session / disc 2: 14
    storm/time to burn: 16
    paffendorf/be cool: 16
    mylo/drop the pressure: 16
    roger sanchez/another chance: 21
    darude/sandstorm: 25

The top 30 most common tracks used on Ministry of Sound CD releases. Look who's sitting pretty with 25 appearances!

I must admit, I thought these tracks would show up more regularly, considering the amount of CD files we were searching through (1,229), but I'm happy that at least my prediction was correct. Next time you see an advert for a MoS album keep an ear out for [Darude - Sandstorm](http://youtu.be/PSYxT9GM0fQ)!


## The full script

    :::python
    import os
    import json


    DB_DIR = "ministry"
    REPLACEMENTS = {
        " (original mix)": "",
        " - ": " / ",
        "-" : " / ",
        " / ": "/"
    }


    def parse_cd(filename, replacements=None):
        """
        Takes the path to a FreeDB CD file and parses all
        key/value pairs into a dictionary.
        """
        if replacements is None:
            replacements = {}
        lines = {}
        with open(filename, "r") as f:
            for line in f.readlines():
                # Remove newline chars
                line = line.rstrip()
                # Ignore any comments or lines without an equals in
                if "=" not in line or line.startswith("#"):
                    continue

                # Extract the keys and values, forcing the values to be
                # lower case
                eq_index = line.index("=")
                key = line[:eq_index]
                value = line[eq_index+1:].lower()

                # Take a dictionary of strings to search and replace eg.
                # {" (original mix)": "", " - ": " / "}
                for old, new in replacements.items():
                    value = value.replace(old, new)

                # Check for the existence of a partial line in the
                # dictionary first and then append the rest of the
                # value if it exists.
                if key in lines:
                    lines[key] += value
                else:
                    lines[key] = value
        return lines


    if __name__ == "__main__":
        tracks_count = {}

        for filename in os.listdir(DB_DIR):
            # Parse the CD
            cd = parse_cd(os.path.join(DB_DIR, filename), REPLACEMENTS)
            # Extract the tracks
            tracks = [
                cd[x] for x in cd.keys() if x.startswith("TTITLE")]

            for track in tracks:
                # If the track has appeared already, increment its counter
                # otherwise add it and start it off at 1.
                if track in tracks_count:
                    tracks_count[track] += 1
                else:
                    tracks_count[track] = 1

        # Finally, sort the tracks_count dictionary by
        # amount of appearances
        for track_count in sorted(
                tracks_count.items(), key=lambda x: x[1]):
            print "%s: %s" % track_count
