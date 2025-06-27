from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

DEAFULT_OWNER:str = "root"

class MetaData(BaseModel):
    info:str
    created:datetime = Field(default_factory=datetime.now)
    modified:datetime = Field(default_factory=datetime.now)
    permission:str = Field(default_factory=" ")
    owner:str = DEAFULT_OWNER


class DirNode(BaseModel):
    name: str
    nodeType: Literal["directory", "file"]
    entries: List[str]=Field(default_factory=list)
    metaData:MetaData 
    children:Optional[List[DirNode]] = Field(default_factory=list)
        
    def attachToNode(self, parentNode:DirNode):
        if parentNode.nodeType!="directory":
            raise Exception("Cannot attach children to type file node")

        if self.name not in parentNode.entries:
            parentNode.entries.append(self.name)
            parentNode.children.append(self)

    def deleteFromNode(self, parentNode:DirNode):
        if self.name not in parentNode.entries:
            raise Exception("child does not exist in the parent node")
        else:
            parentNode.entries.remove(self.name)
            parentNode.children[child for child in parentNode.children if child.name != self.name]

def LevelOrderTraversal(root:DirNode):
    pass
