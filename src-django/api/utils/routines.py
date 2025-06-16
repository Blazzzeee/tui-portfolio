from datetime import datetime
from dirtree import MetaData,DirNode 

fileRoot=None

def buildFileSystem():
    global fileRoot 
    fileRoot = DirNode(name="home", nodeType="directory", metaData=MetaData(info="Root of the file system", modified=datetime.now(), permission=" "))
    buildBlogDir()
    buildProjectsDir()
    buildRootDir()


def buildBlogDir():
    dir = DirNode(name="blog", nodeType="directory", metaData=MetaData(info="Blog directory", modified=datetime.now, permission=" ")) 
    if fileRoot!=None:
        dir.attachToNode(fileRoot)
    attachBlogs()

def attachBlogs():
    #the user must build a blogs repo on Github , the script collects blogs resembling github commits and adds it to blog dir
    pass

def buildProjectsDir():
    #use a global mentioning repo names that are to be added
    #the routine scrapes special dir in github that contains all projects/{projectname} info
    pass

def buildRootDir():
    pass
