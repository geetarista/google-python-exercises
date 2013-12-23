#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""


def get_special_paths(dir):
    results = []
    filenames = os.listdir(dir)
    for filename in filenames:
        if re.match(r'.+\_\_\w+\_\_.+', filename):
            results.append(filename)

    return results

def copy_to(source, target):
    if not os.path.isdir(target):
        os.makedirs(target)

    paths = get_special_paths(source)
    for p in paths:
        shutil.copy(p, target + '/' + p)

def zip_to(source, target):
    paths = get_special_paths(source)
    cmd = "zip -j %s %s" % (target, ' '.join(paths))
    print "Command I'm going to do:", cmd
    err, out = commands.getstatusoutput(cmd)
    if err:
        print(out)
        sys.exit(1)

def print_results(results):
    for result in results:
        print(os.path.abspath(result))

def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.
    
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
        sys.exit(1)
    
    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]
    
    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]
    
    if len(args) == 0:
        print "error: must specify one or more dirs"
        sys.exit(1)
    
    if todir:
        return copy_to(args[0], todir)

    if tozip:
        return zip_to(args[0], tozip)

    print_results(get_special_paths(args[0]))

if __name__ == "__main__":
    main()
