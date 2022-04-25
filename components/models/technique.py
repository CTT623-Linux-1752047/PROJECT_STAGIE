from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo

from components.models import Variable

# Create your models here.

class Technique(StructuredNode):
    techniqueCd = StringProperty(unique_index=True, required=True)
    techniqueName = StringProperty()
    

    # Relationship hasSubValue :
    variableValue = RelationshipTo('VarialeValue', 'HAS_SUB_VALUE')

    # Relationship hasVariableType
    variableType = RelationshipTo(Variable,'HAS_VARIABLE_TYPE')
    