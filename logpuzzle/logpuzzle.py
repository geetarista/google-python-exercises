#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def word_key(s):
    return s.split('-')[-1]

def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order.

    Example:

    ./logpuzzle.py animal_code.google.com
    http://code.google.com/something/puzzle-animal-baaa.jpg
    http://code.google.com/something/puzzle-animal-baab.jpg
    ...
    """

    domain = re.search(r'_(.+)', filename).group(1)
    matches = set()
    f = open(filename)

    for line in f:
        match = re.search(r'GET (.+) HTTP', line)
        if match:
            if "puzzle" in match.group(1):
                matches.add("http://" + domain + match.group(1))

    f.close()

    return sorted(matches, key=word_key)


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.

    Example:

    ./logpuzzle.py --todir animaldir animal_code.google.com
    ls animaldir
    img0  img1  img2  img3  img4  img5  img6  img7  img8  img9  index.html
    """

    # See if dest_dir exists--if not, create it
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    # Build HTML
    html_parts = ["<html><body>"]

    for i, url in enumerate(img_urls):
        try:
            # Download image
            ufile = urllib.urlopen(url)
            img = ufile.read()
            f = open("./%s/img%d" % (dest_dir, i), 'wb')
            f.write(img)
            f.close()

            # Add image tag
            html_parts.append('<img src="img%d">' % i)
        except IOError:
            print 'problem reading url:', url

    html_parts.append("</body></html>")

    # Write HTML file
    f = open('./' + dest_dir + '/index.html','w')
    f.write(''.join(html_parts))
    f.close()


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)

if __name__ == '__main__':
    main()
