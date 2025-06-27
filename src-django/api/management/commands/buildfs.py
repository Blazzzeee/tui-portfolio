from django.core.management.base import BaseCommand
from api.utils.routines import buildFileSystem 
from api.utils.dirtree import DirNode 

def print_tree(node: DirNode, indent=""):
    print(f"{indent}- {node.name}/" if node.nodeType == "directory" else f"{indent}- {node.name}")
    if node.nodeType == "directory" and node.children:
        for child in node.children:
            print_tree(child, indent + "  ")

class Command(BaseCommand):
    help = "Builds the virtual filesystem from GitHub and blog data"

    def handle(self, *args, **kwargs):
        file_root=buildFileSystem()
        self.stdout.write(self.style.SUCCESS("Filesystem built successfully."))
        print("\nFilesystem Tree Structure:\n")
        print_tree(file_root)
