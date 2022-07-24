from pickle import FALSE
from neomodel import StructuredNode, StringProperty, RelationshipTo, db

# Create your models here.

class TaskType(StructuredNode):
    taskTypeCd = StringProperty(unique_index=True, required=True)
    taskTypeName = StringProperty(default="")
    
    hasSubTaskType = RelationshipTo('TaskType', 'hasSubTaskType')
    
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
    
    def getVariableValueByTaskType(idTaskType): 
        try : 
            cypher = "MATCH (tt:TaskType)-[:hasVariableValue]->(vv:VariableValue) WHERE tt.taskTypeCd = \"" + idTaskType + "\" "
            cypher = cypher + "RETURN vv.variableType, vv.variableValue, vv.variableValueCd, ID(vv) "
            return db.cypher_query(cypher)[0]
        except : 
            return False

    def getTechniqueByTaskType(idTaskType): 
       try: 
           cypher = "MATCH (t:Technique)-[:hasPragmaticScope]->(tt:TaskType) WHERE tt.taskTypeCd = \"" + idTaskType + "\" "
           cypher = cypher + "RETURN t.techniqueCd, t.techniqueName, ID(t)"
           return db.cypher_query(cypher)[0]
       except: 
           return False
    
    def checkExistsElement(key1, key2, array): 
        for index, val in enumerate(array):
            if key1 == val[0] and key2 == val[1]:
                return index
        return False
    
    def getTaskTypeTechniqueParentByTaskType(idTaskType): 
        try: 
            # parent tasktype with technique <> null
            cypher1 = "MATCH (tt1:TaskType)-[:hasSubTaskType]->(tt2:TaskType)<-[:hasPragmaticScope]-(t:Technique) WHERE tt1.taskTypeCd = \"" + idTaskType + "\" "
            cypher1 = cypher1 + " RETURN tt2.taskTypeCd, tt2.taskTypeName, t.techniqueCd, t.techniqueName, ID(tt2), ID(t)"
            wRecord1 = db.cypher_query(cypher1)[0]
            
            # parent task type with technique == null
            cypher2 = "MATCH (tt1:TaskType)-[:hasSubTaskType]->(tt2:TaskType) WHERE tt1.taskTypeCd = \"" + idTaskType + "\" "
            cypher2 = cypher2 + " RETURN tt2.taskTypeCd, tt2.taskTypeName, ID(tt2)"
            wRecord2 = db.cypher_query(cypher2)[0]
            
            flgDuplicate = False
            
            for item2 in wRecord2 : 
                taskCd = item2[0]
                taskName = item2[1]
                for item1 in wRecord1 : 
                    if taskCd == item1[0] and taskName == item1[1] : 
                        flgDuplicate = True
                if not flgDuplicate : 
                    tmp = [item2[0], item2[1], "", "", item2[2]]
                    wRecord1.append(tmp)
                    flgDuplicate = False     
            
            return wRecord1
        except:
            return False
        
    
        
    def getTaskTypeTechniqueChildByTaskType(idTaskType): 
        try: 
            # child task type with technique <> null
            cypher1 ="MATCH (t:Technique)-[:hasPragmaticScope]->(tt1:TaskType)-[:hasSubTaskType]->(tt2:TaskType) WHERE tt2.taskTypeCd = \"" + idTaskType + "\" "
            cypher1 = cypher1 + " RETURN tt1.taskTypeCd, tt1.taskTypeName, t.techniqueCd, t.techniqueName, ID(tt1), ID(t)"
            wRecord1 = db.cypher_query(cypher1)[0]
            
            # child task type with technique == null
            cypher2 = "MATCH (tt1:TaskType)-[:hasSubTaskType]->(tt2:TaskType) WHERE tt2.taskTypeCd = \"" + idTaskType + "\" "
            cypher2 = cypher2 + " RETURN tt1.taskTypeCd, tt1.taskTypeName, ID(tt1)"
            wRecord2 = db.cypher_query(cypher2)[0]
           
            flgDuplicate = False
            
            for item2 in wRecord2 : 
                taskCd = item2[0]
                taskName = item2[1]
                for item1 in wRecord1 : 
                    if taskCd == item1[0] and taskName == item1[1] : 
                        flgDuplicate = True
                if not flgDuplicate : 
                    tmp = [item2[0], item2[1], "", "", item2[2]]
                    wRecord1.append(tmp)
                    flgDuplicate = False     
                    
            return wRecord1
            
        except:
            return False