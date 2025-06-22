from api.utils.dirtree import MetaData,DirNode 
import os
import subprocess
import shutil
import datetime

fileRoot=None

GITHUB_USERNAME = "Blazzzeee"
PROJECTS = ["websockets", "studybud"]
SPARSE_PATHS = ["portfolio/"] 
CLEANUP_ENABLED = False

def buildFileSystem():
    global fileRoot 
    fileRoot = DirNode(name="home", nodeType="directory", metaData=MetaData(info="Root of the file system", modified=datetime.now(), permission=" "))
    buildBlogDir()
    buildProjectsDir()
    buildRootDir()


def buildBlogDir():
    dir = DirNode(name="blog", nodeType="directory", metaData=MetaData(info="Blog directory", modified=datetime.now(), permission=" ")) 
    if fileRoot!=None:
        dir.attachToNode(fileRoot)
    attachBlogs()

def attachBlogs():
    #the user must build a blogs repo on Github , the script collects blogs resembling github commits and adds it to blog dir
    pass

def buildProjectsDir():
    #use a global mentioning repo names that are to be added
    #the routine scrapes special dir in github that contains all projects/{projectname} info
    dir = DirNode(name="projects", nodeType="directory", metaData=MetaData(info="Project Directory", modified=datetime.now(), created=datetime.now(), permission=" "))
    BASE_DIR= "tmp"
    os.makedirs(BASE_DIR, exist_ok=True)
    for project in PROJECTS:
        repo_url = f"https://github.com/{GITHUB_USERNAME}/{project}.git"
        project_path = os.path.join(BASE_DIR, project)
        #Clone subdir from remote repo {project}
        subprocess.run(["git", "clone", 
                        "--filter=blob:none",
                        "--sparse",
                        repo_url,
                        project_path
                        ])
        #Set sparse path
        subprocess.run(["git", "sparse-checkout", "set"]+ SPARSE_PATHS, cwd=project_path)

        print(f"Spare cloned {project} to {project_path}")


        if CLEANUP_ENABLED:
             print(f"Starting cleanup..")
             shutil.rmtree(BASE_DIR)
             print("Finished cleanup...")
def buildRootDir():
    pass
