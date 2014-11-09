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

class FileSystem(object):
    def __init__(self, path):
        self.stat = os.stat(path)
        self.path = path
        
    def __str__(self):
        return self.path
    def __repr__(self):
        return self.path
    # TODO: turn these stat results into stat objects so we can do things like 
    # FileSystem.size().toMB or toGB, or toKB etc
    def size(self):
        return self.stat.st_size
    
    def ctime(self):
        return self.stat.st_ctime
    
    def mtime(self):
        return self.stat.st_mtime
    
    def atime(self):
        return self.stat.st_atime
        
    def is_olderthan(self):
        pass
    
    def is_newerthan(self):
        pass
    
    def is_smallerthan(self):
        pass
    
    def move(self, dst):
        shutil.move(self.path, dst)
    
    def copy(self, dst):
        shutil.copy2(self.path, dst)
        
    def delete(self):
        os.remove(self.path)
    


class FileSystemList(object):
    def __init__(self):
        self.list = []
        
    def append(self, fsobj):
        self.list.append(fsobj)
        
    def move(self, dst):
        for i in self.list:
            i.move(i.path, dst)
            
    def copy(self, dst):
        for i in self.list:
            i.copy(i.path, dst)

    def delete(self):
        for i in self.list:
            i.delete()
    
    def get_size(self):
        size = 0
        for i in self.list:
            size += i.size()
        return size
            
    def filter(self): # Todo: probably only useful for the FileSystemList class 
        pass
        
def findstr(string, path):
    """
    Find a string in a file.
    """''
    matches = []
    for root, dirs, files in os.walk(path):
        for fname in files:
            f = open(os.path.join(root, fname), 'r')
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
    matches = FileSystemList()
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
                matches.append(FileSystem(filename))
                
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
    findstr('document','c:/users/jay/desktop/python-shelltools/')
            
