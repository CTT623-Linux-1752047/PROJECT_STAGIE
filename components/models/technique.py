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