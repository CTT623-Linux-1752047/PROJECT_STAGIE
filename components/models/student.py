from neomodel import StructuredNode, StringProperty, db 

# Create your models here.

class Student(StructuredNode):
    studentCd = StringProperty(unique_index=True, required=True)
    fullNameStudent = StringProperty(default="")
    
    def __str__(self):
            return self.fullNameStudent

    def countStudentByLevel(level):
        cypher = "MATCH p=(st:Student)<-[r1:relatedToStudent]-(lII:LocalInsInfo)-[r2:relatedToLevel]->(l:Level) WHERE l.levelCd = \"" + level + "\" return count(r2)"
        return db.cypher_query(cypher)[0][0][0]
    
    def getTechOfStFollowLevelByID(idStudent, idLevel): 
        cypher = "MATCH p=(l:Level)<-[:relatedToLevel]-(lii:LocalInsInfo)-[:relatedToTech]->(t:Technique) "
        cypher = cypher + " WHERE l.levelCd = \"" + idLevel + "\" "
        cypher = cypher + " AND (lii)-[:relatedToStudent]->(:Student{studentCd:\"" + idStudent + "\"}) RETURN t"
        lstTechCd = []
        lstTechName = []
        wRecord = db.cypher_query(cypher)[0]
        for item in wRecord: 
            if item[0]['groupCd'] not in lstTechCd :
                lstTechCd.append(item[0]['techniqueCd'])
                if not item[0]['techniqueName']: 
                    lstTechName.append(item[0]['techniqueCd'])
                else :
                    lstTechName.append(item[0]['techniqueName'])
        result = []
        result.append(lstTechCd)
        result.append(lstTechName)   
        return result
    
    def cntStudentByGroupe(idGroupe):
        cypher = "MATCH (st:Student)-[:arrangedIn]->(gr:Group) "
        cypher = cypher + " WHERE gr.groupCd = \"" + idGroupe + "\" RETURN COUNT(st)"
        return db.cypher_query(cypher)[0][0][0]
    
    def getStudentByGroupe(idGroup): 
        try : 
            cypher = "MATCH (lii:LocalInsInfo)-[:relatedToStudent]->(st:Student)-[:arrangedIn]->(gr:Group{groupCd:\"" + idGroup + "\" }) "
            cypher = cypher + " RETURN st.studentCd, st.fullNameStudent"
            result = [] 
            for item in db.cypher_query(cypher)[0]: 
                if item not in result : 
                    result.append(item)
            return result
        except: 
            return False