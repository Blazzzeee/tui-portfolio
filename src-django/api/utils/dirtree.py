from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class MetaData(BaseModel):
    size:int
    created:datetime
    modified:datetime
    permission:str
    owner:str


class DirNode(BaseModel):
    name: str
    nodeType: Literal["directory", "file"]
    entries: List[str]
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
            parentNode.children = [child for child in parentNode.children if child.name != self.name]
