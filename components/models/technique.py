from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo

# Create your models here.

class Technique(StructuredNode):
    techniqueCd = StringProperty(unique_index=True, required=True)
    techniqueName = StringProperty(default="")
    
    def __str__(self):
            return self.techniqueName

