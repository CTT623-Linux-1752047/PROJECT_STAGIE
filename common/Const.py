from datetime import date
from datetime import datetime

class Const: 
    CURLY_BRACKETS_OPEN = "{"
    CURLY_BRACKETS_CLOSE = "}"
    DATE_CD_DMYHMS = date.today().strftime("%d%m%Y%H%M%S")
    DATE_DMYHMS = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    SHEET_NAME_VARIABLE = "Variable"
    SHEET_NAME_VARIABLE_VALUE = "Variable Value"
    SHEET_NAME_TASK_TYPE ="Task Type"
    SHEET_NAME_TECHNIQUE = "Technique"
    SHEET_NAME_LEVEL = "Level"
    SHEET_NAME_STUDENT = "Student"
    SHEET_NAME_GROUP = "Group"
    SHEET_NAME_LOCALINSINFO = "LocalInsInfo"

    NAME_LEVEL = "Level"
    NAME_STUDENT = "Student"
    NAME_GROUP = "Group"
    NAME_LOCALINSINFO = "LocalInsInfo"
    NAME_VARIABLE = "Variable"
    NAME_VARIABLE_VALUE = "VariableValue"
    NAME_TASK_TYPE ="TaskType"
    NAME_TECHNIQUE = "Technique"

    RELATIONSHIP_VARIABLEVALUE_VARIABLEVALUE = "hasSubValue"
    RELATIONSHIP_VARIABLEVALUE_VARIABLE = "hasVariableType"
    RELATIONSHIP_TASKTYPE_TASKTYPE = "hasSubTaskType"
    RELATIONSHIP_TASKTYPE_VARIABLEVALUE = "hasVariableValue"
    RELATIONSHIP_TASKTYPE_TECHNIQUE = "hasPragmaticScope"
    RELATIONSHIP_TT_GLOBAL = "hasGlobalConcurrency"
    RELATIONSHIP_TT_INC = "hasPartialConcurrency"
    RELATIONSHIP_TT_EXT = "hasConcurrencyByExtension"
    RELATIONSHIP_STUDENT_GROUP = "arrangedIn"
    RELATIONSHIP_LOCALINSINFO_STUDENT = "relatedToStudent"
    RELATIONSHIP_LOCALINSINFO_LEVEL = "relatedToLevel"
    RELATIONSHIP_LOCALINSINFO_TECHNIQUE = "relatedToTech"

    SUB_TASK = "SubTask"