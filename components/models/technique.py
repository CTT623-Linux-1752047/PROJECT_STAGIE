from multiprocessing import Condition
from neomodel import StructuredNode, StringProperty, RelationshipTo, db

# Create your models here.

class Technique(StructuredNode):
    techniqueCd = StringProperty(unique_index=True, required=True)
    techniqueName = StringProperty(default="")
    
    hasConcurrencyByExtension = RelationshipTo('Technique', 'hasConcurrencyByExtension')
    hasPartialConcurrency = RelationshipTo('Technique', 'hasPartialConcurrency')
    hasGlobalConcurrency = RelationshipTo('Technique', 'hasGlobalConcurrency')
    
    def __str__(self):
            return self.techniqueName

    def countRelationship(relationship):
        cypher = "MATCH p=()-[r:" + relationship + "]->() RETURN count(p)"
        return db.cypher_query(cypher)[0][0][0]

    def cntTechFollowLevelByID(idTech, idLevel): 
        cypher = "MATCH (l:Level)<-[:relatedToLevel]-(lii:LocalInsInfo)-[:relatedToTech]->(t:Technique) "
        cypher = cypher + " WHERE l.levelCd=\"" + idLevel + "\" AND t.techniqueCd=\"" + idTech + "\" return count(lii) "
        return db.cypher_query(cypher)[0][0][0]

    def getGroupCodeByTechnique(idTech):
        cypher = "MATCH (gr:Group)<-[:arrangedIn]-(:Student)<-[:relatedToStudent]-(:LocalInsInfo)-[:relatedToTech]->(t:Technique) "
        cypher = cypher + "WHERE t.techniqueCd =\"" + idTech + "\" RETURN gr"
        wRecord = db.cypher_query(cypher)[0]
        lstGroupCd = []
        lstGroupName = []
        for item in wRecord: 
            if item[0]['groupCd'] not in lstGroupCd :
                lstGroupCd.append(item[0]['groupCd'])
                if not item[0]['groupName']: 
                    lstGroupName.append(item[0]['groupCd'])
                else :
                    lstGroupName.append(item[0]['groupName'])
        result = []
        result.append(lstGroupCd)
        result.append(lstGroupName)   
        return result
    
    def cntStudentByTechniqueAndGroup(idTech, idGroup, idLevel):
        cypher = "MATCH (gr:Group)<-[:arrangedIn]-(st:Student)<-[:relatedToStudent]-(lii:LocalInsInfo)-[r1:relatedToLevel]->(l:Level) "
        cypher = cypher + " WHERE l.levelCd =\"" + idLevel + "\" "
        cypher = cypher + " AND (lii)-[:relatedToTech]->(:Technique{techniqueCd:\"" + idTech + "\"}) "
        cypher = cypher + " AND gr.groupCd = \"" + idGroup + "\"  RETURN COUNT(st)"
        return db.cypher_query(cypher)[0][0][0]
    
    def getTechByGroupe(idGroupe):
        cypher = "MATCH (t:Technique)<-[:relatedToTech]-(lii:LocalInsInfo)-[:relatedToStudent]->(st:Student)-[:arrangedIn]->(gr:Group) "
        cypher = cypher + "WHERE gr.groupCd = \"" + idGroupe + "\" RETURN t "
        wRecord = db.cypher_query(cypher)[0]
        lstTechniqueCd = []
        lstTechniqueName = []
        for item in wRecord: 
            if item[0]['techniqueCd'] not in lstTechniqueCd :
                lstTechniqueCd.append(item[0]['techniqueCd'])
                if not item[0]['techniqueName']: 
                    lstTechniqueName.append(item[0]['techniqueCd'])
                else :
                    lstTechniqueName.append(item[0]['techniqueName'])
        result = []
        result.append(lstTechniqueCd)
        result.append(lstTechniqueName)   
        return result
        
    def cntStudentByTechAndGroupAndLevel(idTech, idGroup, idLevel): 
        cypher = "MATCH p=(:Level{levelCd:\"" + idLevel + "\"})<-[]-(lii:LocalInsInfo)-[]->(:Technique{techniqueCd:\"" + idTech + "\"}) "
        cypher = cypher + "WHERE (lii)-[]->(:Student)-[]->(:Group{groupCd:\"" + idGroup + "\"}) RETURN COUNT(lii)"
        return db.cypher_query(cypher)[0][0][0]
    
    def getTaskTypeByTech(idTech):
        try: 
            cypher = " MATCH (t:Technique)-[:hasPragmaticScope]->(tt:TaskType) WHERE t.techniqueCd = \"" + idTech + "\" "
            cypher = cypher + "RETURN tt.taskTypeCd, tt.taskTypeName, ID(t), ID(tt)"
            return db.cypher_query(cypher)[0]
        except : 
            return False
       
    def getLevelByTechStudent(idStudent, idTech): 
        try: 
            cypher = "MATCH (st:Student)<-[:relatedToStudent]-(lii:LocalInsInfo)-[r1:relatedToLevel]->(l:Level) "
            cypher = cypher + " WHERE (lii)-[:relatedToTech]->(:Technique{techniqueCd:\"" + idTech + "\"}) "
            cypher = cypher + " AND st.studentCd = \"" + idStudent + "\"  RETURN l.levelCd	"
            
            return db.cypher_query(cypher)[0][0][0]
        except:
            return False 
    def getSubTechByRelation(idTech, idRelation):
        try: 
            if(idRelation == "C1"):
                relation = "hasGlobalConcurrency" 
                fieldReturn = "t2.techniqueCd, t2.techniqueName, ID(t2)"
                condition = " WHERE t1.techniqueCd = \"" + idTech + "\""
            elif(idRelation == "C2") :
                relation = "hasPartialConcurrency" 
                fieldReturn = "t2.techniqueCd, t2.techniqueName, ID(t2)"
                condition = " WHERE t1.techniqueCd = \"" + idTech + "\""
            else : 
                relation = "hasConcurrencyByExtension" 
                fieldReturn = "t1.techniqueCd, t1.techniqueName, ID(t1)"
                condition = " WHERE t2.techniqueCd = \"" + idTech + "\""
            
            cypher = "MATCH (t1:Technique)-[:" + relation + "]->(t2:Technique) " + condition + " RETURN " + fieldReturn
        
            return db.cypher_query(cypher)[0]
        except : 
            return False