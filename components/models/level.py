from neomodel import StructuredNode, StringProperty, RelationshipTo, db

# Create your models here.

class Level(StructuredNode):
    levelCd = StringProperty(unique_index=True, required=True)
    levelName = StringProperty(default="")
   
    def __str__(self):
            return self.techniqueName
        
    def getTechniqueByTaskType():
        cypher = "MATCH p=(tt:TaskType)<-[:hasPragmaticScope]-(t:Technique) RETURN tt.taskTypeCd, tt.taskTypeName, t.techniqueCd, t.techniqueName"
        wRecord = db.cypher_query(cypher)[0]
        result = []
        for record in wRecord: 
            obj = {
                "taskTypeCd" : record[0],
                "taskTypeName" : record[1],
                "techniqueCd" : record[2],
                "techniqueName" : record[3]
            }
            result.append(obj)
        return result

   
        