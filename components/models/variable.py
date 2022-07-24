from neomodel import StructuredNode, StringProperty

# Create your models here.

class Variable(StructuredNode):
    variableCd = StringProperty(unique_index=True, required=True)
    variableDescription = StringProperty(default="")
    
    def __str__(self):
            return self.variableDescription

