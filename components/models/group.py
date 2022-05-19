from neomodel import StructuredNode, StringProperty

# Create your models here.

class Group(StructuredNode):
    groupCd = StringProperty(unique_index=True, required=True)
    groupName = StringProperty(default="")
    
    def __str__(self):
            return self.groupName

