#!/usr/bin/env python


'''
shelltools aims to bring some of the basic file and directory tools found
in most shells to python. Copying, moving, searching etc.

This module will define the user-facing api.
'''
import fnmatch
import os
import shutil
import datetime


def findstr(string, path):
    """
    Find a string in a file.
    """''
    matches = []
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.endswith('.py'):
                f = open(os.path.join(root, fname), 'r')
            else:
                continue
            content = f.readline()
            while content != '':
                if string in content:
                    matches.append((fname, root))
                    print "%s\t%s" % (fname, root)
                    break
                else:
                    content = f.readline()
            f.close()


def find(locations, filters, recursive=False):
    """
    A general file search function
    By default, returns all files in given locations and ignores subfolders.
    Returns: A list of filepaths.
    """
    all_files = []
    matches = []
    for location in locations:
        contents = []
        if recursive == True:
            for root, dirs, files in os.walk(location):
                for fname in files:
                    contents.append(os.path.join(root, fname))
        else:
            try:
                for fname in os.listdir(location):
                    contents.append(os.path.join(location, fname))
            except WindowsError as e:
                print e
        all_files.extend(contents)
        
    for filename in all_files:
        for pattern in filters:
            if fnmatch.fnmatch(os.path.basename(filename), pattern):
                #print "Found match: %s" % filename
                matches.append(filename)
                
    return matches


def delete(filename):
    """
    Delete a file.
    """
    try:
        os.remove(filename)
    except WindowsError as e:
        print "Could not delete file"
        print e                    


def remtree(root):
    """
    Remove a directory tree.
    """
    try:
        shutil.rmtree(os.path.abspath(root))
    except OSError:
        print 'File Tree at %s could not be deleted.' % root
  
    
def merge(src, dest):
    """
    Copy directory tree from src to dest.
    Create new directories as needed
    If matching directory exists, only copy new files.
    """
    #Walk each directory in source. If same directory does not exist in dest, create it.
    skips = []
    for root, subs, files in os.walk(src):
        for sub in subs:
            fullpath = os.path.join(root, sub)
            relative = fullpath.replace(src, '')
            relative = relative.lstrip(os.sep)
            destpath = os.path.join(dest, relative)
            if not os.path.exists(destpath):
                os.makedirs(destpath)
        #copy each file that does not exist.
        for fname in files:
            sourcepath = os.path.join(root, fname)
            relative = sourcepath.replace(src, '')
            relative = relative.lstrip(os.sep)
            destfile = os.path.join(dest, relative)
            destpath = os.path.dirname(destfile)
            
            if not os.path.exists(destpath):
                os.makedirs(destpath)
            if not os.path.exists(destfile):    
                try:
                    shutil.move(sourcepath, destfile)
                except WindowsError:
                    print "Could Not move file. It is being used\
by another process.\n%s" % sourcepath
            else:
                skips.append(sourcepath)
    if len(skips) > 0:
        print "Cannot Copy files. They may already exist.\n%s" % skips


def get_size(path):
    """
    Returns the size, in bytes, of the file or directory specified by path
    """
    size = 0
    if os.path.isfile(path):
        try:
            size += os.path.getsize(path)
        except OSError:
            pass
        
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for fname in files:
                f = os.path.join(root, fname)
                try:
                    size += os.path.getsize(f)
                except OSError:
                    continue
    return size
 
    
def delolder(path, ndays):
    """
    Delete all files/folders older than the specified number of days.
    """
    if not os.path.exists(path): return 0
    # analyze path, get total size of all files
    total_count = 0
    deleted_count = 0
    size = 0
    today = datetime.date.today()
    delta = datetime.timedelta(ndays)
    # see if contents are larger than the limit, or older than the specified date
    # delete oldest folders/files one at a time
    files = os.listdir(path)
    for fname in files:
        fpath = os.path.join(path, fname)
        stats = os.stat(fpath)
        fdate = datetime.date.fromtimestamp(stats.st_mtime)
        if os.path.isfile(fpath):
            
            if today - fdate > delta:
                try:
                    print "deleting:", fpath
                    os.remove(fpath)
                    size += stats.st_size
                    deleted_count += 1
                    
                except OSError as e:
                    print e
                
                total_count += 1
    
    if deleted_count == 0:
        print "No files deleted."

        
if __name__ == '__main__':
    pass
            
