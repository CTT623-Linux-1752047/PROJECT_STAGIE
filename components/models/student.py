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