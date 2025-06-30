import os
import shutil
import subprocess
from datetime import datetime

from api.utils.dirtree import DirNode, MetaData

file_root = None

GITHUB_USERNAME = "Blazzzeee"
PROJECTS = ["testing"]
SPARSE_PATHS = ["portfolio/"]
CLEANUP_ENABLED = True
PROJECT_FILES = ["about.txt", "demo.gif", "journey.txt", "tech.txt"]


def buildFileSystem():
    print(f"Starting file system hook")
    file_root = DirNode(
        name="home",
        nodeType="directory",
        metaData=MetaData(
            info="Root of the file system", modified=datetime.now(), permission=" "
        ),
    )
    buildBlogDir()
    buildProjectsDir(file_root)
    buildRootDir()
    return file_root


def buildBlogDir():
    dir = DirNode(
        name="blog",
        nodeType="directory",
        metaData=MetaData(
            info="Blog directory", modified=datetime.now(), permission=" "
        ),
    )
    if file_root != None:
        dir.attachToNode(file_root)
    attachBlogs()


def attachBlogs():
    # the user must build a blogs repo on Github , the script collects blogs resembling github commits and adds it to blog dir
    pass


def buildProjectsDir(file_root):
    # use global repo list
    # the routine scrapes special dir in github that contains all projects/{projectname} info
    dirProjects = DirNode(
        name="projects",
        nodeType="directory",
        metaData=MetaData(
            info="Project Directory",
            modified=datetime.now(),
            created=datetime.now(),
            permission=" ",
        ),
    )
    dirProjects.attachToNode(file_root)
    BASE_DIR = "tmp"
    os.makedirs(BASE_DIR, exist_ok=True)
    for project in PROJECTS:
        repo_url = f"https://github.com/{GITHUB_USERNAME}/{project}.git"
        project_path = os.path.join(BASE_DIR, project)
        # Clone subdir from remote repo {project}
        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--filter=blob:none",
                    "--sparse",
                    repo_url,
                    project_path,
                ],
                check=True,
                text=True,
            )

            subprocess.run(
                ["git", "sparse-checkout", "init", "--cone"],
                cwd=project_path,
                check=True,
                text=True,
            )
            # Set sparse path
            subprocess.run(
                ["git", "sparse-checkout", "set"] + SPARSE_PATHS,
                cwd=project_path,
                text=True,
            )
            print(f"Spasre cloned {project} to {project_path}")

        except subprocess.CalledProcessError as e:
            print(
                f"Error {e.returncode}: Could not clone {project} msg: {e.stdout} {e.stderr}"
            )

    print(f"Starting project hook...")
    for project in PROJECTS:

        dir = DirNode(
            name=project,
            nodeType="directory",
            metaData=MetaData(
                info=" ",
                modified=datetime.now(),
                created=datetime.now(),
                permission=" ",
            ),
        )
        dir.attachToNode(dirProjects)
        print(f"Added {project} to filesystem")

        for file_basename in PROJECT_FILES:
            try:
                # Read data from file , Create Node , attach node to filesystem
                file_name = os.path.join("tmp", project, SPARSE_PATHS[0], file_basename)
                if file_basename.endswith("gif"):
                    # TODO handle gifs
                    text = "gif file"
                else:
                    with open(file_name, mode="r", encoding="utf-8") as file:
                        text = file.read()
                    # Create a node containing file content
                fileNode = DirNode(
                    name=file_basename,
                    nodeType="file",
                    entries=[text],
                    children=None,
                    metaData=MetaData(info=" ", permission="empty"),
                )
                # Attach node or file to its project node
                fileNode.attachToNode(dir)
                print(f"Added {file_basename} to dir {project}")

            except FileNotFoundError as e:
                print(
                    f"Error: file {file_basename} not present in {project} skipping ..."
                )
            except Exception as e:
                print(f"Unknown error has occurred {e}")

    if CLEANUP_ENABLED:
        print(f"Starting cleanup..")
        shutil.rmtree(BASE_DIR)
        print("Finished cleanup...")


def buildRootDir():
    pass
