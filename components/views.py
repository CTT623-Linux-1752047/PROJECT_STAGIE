import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from components.models.technique import Technique
from components.models.student import Student
from components.models.group import Group
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def home(request):
    if request.user.is_authenticated:
        if request.method == "POST" : 
          
            searchCondition = request.POST.get("searchCondition")
            typeSearch = request.POST.get("typeSearch")
            
            result = False
            
            if typeSearch == "TE" :
                if searchCondition != "" :
                    lstGroupByTech = Technique.getGroupCodeByTechnique(searchCondition)
    
                    if len(lstGroupByTech) > 0 : 
                        lstDataBarChartEnCours = []
                        lstDataBarChartAcquis = []
                        lstDataBarChartMatrise = []
                        
                        for group in lstGroupByTech[0]: 
                            lstDataBarChartEnCours.append(Technique.cntStudentByTechniqueAndGroup(searchCondition,group,"L1"))
                            lstDataBarChartAcquis.append(Technique.cntStudentByTechniqueAndGroup(searchCondition,group,"L2"))
                            lstDataBarChartMatrise.append(Technique.cntStudentByTechniqueAndGroup(searchCondition,group,"L3"))
                            
                        lstGroupByTech.append(lstDataBarChartEnCours)
                        lstGroupByTech.append(lstDataBarChartAcquis)
                        lstGroupByTech.append(lstDataBarChartMatrise)
                        
                    techName = Technique.nodes.get(techniqueCd=searchCondition)
                    result =  {
                        "type" : "TE",
                        "code" : searchCondition,
                        "name" : techName.techniqueName,
                        "pieChart" : [Technique.cntTechFollowLevelByID(searchCondition,"L1"), # en cours
                                    Technique.cntTechFollowLevelByID(searchCondition, "L2"), # acquis
                                    Technique.cntTechFollowLevelByID(searchCondition, "L3")],  # maîtrise     
                        "barChart" : lstGroupByTech
                    }   
            
            if typeSearch == "ST" :
                if searchCondition != "": 
                    studentName = Student.nodes.get(studentCd=searchCondition)
                    datatable = []
                    for level in ["L1","L2","L3"]:
                        for item in Student.getTechOfStFollowLevelByID(searchCondition, level)[1]:
                            obj = {
                                "techName" : item,
                                "level" : level
                            }
                            datatable.append(obj)
                        
                    result =  {
                        "type" : "ST",
                        "code" : searchCondition,
                        "name" : studentName.fullNameStudent,
                        "pieChart" : [len(Student.getTechOfStFollowLevelByID(searchCondition, "L1")[0]), # en cours
                                    len(Student.getTechOfStFollowLevelByID(searchCondition, "L2")[0]), # acquis
                                    len(Student.getTechOfStFollowLevelByID(searchCondition, "L3")[0])], # maîtrise     
                        "datatable" : datatable
                    }   
                    
            if typeSearch == "GR" :
                if searchCondition != "": 
                    allStudentInGroup = Student.cntStudentByGroupe(searchCondition)
                    cntTechL1 = 0
                    cntTechL2 = 0
                    cntTechL3 = 0
                    lstTech = Technique.getTechByGroupe(searchCondition)
                    lstDataBarChartEnCours = []
                    lstDataBarChartAcquis = []
                    lstDataBarChartMatrise = [] 
                    for item in lstTech[0]:
                        techName = Technique.nodes.get(techniqueCd=item)
                        tmp1 = Technique.cntStudentByTechAndGroupAndLevel(item,searchCondition,"L1")
                        tmp2 = Technique.cntStudentByTechAndGroupAndLevel(item,searchCondition,"L2")
                        tmp3 = Technique.cntStudentByTechAndGroupAndLevel(item,searchCondition,"L3")
                        if tmp1 / allStudentInGroup < 0.8 : 
                            cntTechL1 = cntTechL1 + 1
                        if tmp2 / allStudentInGroup < 0.8 : 
                            cntTechL2 = cntTechL2 + 1
                        if tmp3 / allStudentInGroup < 0.8 : 
                            cntTechL3 = cntTechL3 + 1
                        
                        objL1 = {
                            "meta": techName.techniqueName + " - ", 
                            "value": tmp1
                        }
                        lstDataBarChartEnCours.append(objL1)
                        
                        objL2 = {
                            "meta": techName.techniqueName  + " - ", 
                            "value": tmp2
                        }
                        lstDataBarChartAcquis.append(objL2)
                        
                        objL3 = {
                            "meta": techName.techniqueName  + " - ", 
                            "value": tmp3
                        }
                        lstDataBarChartMatrise.append(objL3)
                           
                    lstTech.append(lstDataBarChartEnCours)
                    lstTech.append(lstDataBarChartAcquis)
                    lstTech.append(lstDataBarChartMatrise) 
                        
                    result =  {
                        "type" : "GR",
                        "code" : searchCondition,
                        "name" : "",
                        "pieChart" : [cntTechL1, # en cours
                                    cntTechL2, # acquis
                                    cntTechL3], # maîtrise     
                        "barChart" : lstTech
                    }
                
            if typeSearch == "STech": 
                result =  Technique.getTechByGroupe(request.POST.get("idGroupe")) 
                
            if typeSearch == "STable" :
                if request.POST.get("idGroupe"):
                    lstStudent = Student.getStudentByGroupe(request.POST.get("idGroupe"))
                    result = []
                    for item in lstStudent: 
                        tmp = [item[0], item[1]]
                        if request.POST.get("idTech"):
                            lstTech = request.POST.get("idTech").split(",")
                            for tech in lstTech:
                                record = Technique.getLevelByTechStudent(item[0], tech)
                                #tmp.append(record)
                                if record == False: 
                                    tmp.append("-")
                                if record == "L1": 
                                    tmp.append("<span class=\"badge badge-pill \" style=\"background-color: #ff0000; color: white\">En cours</span>")
                                if record == "L2":
                                    tmp.append("<span class=\"badge badge-pill \" style=\"background-color: #2bff00; color: white\">Acquis</span>")
                                if record == "L3":
                                    tmp.append("<span class=\"badge badge-pill \" style=\"background-color: #2451ff; color: white\">Maîtrise</span>")
                                
                        result.append(tmp)
                               
                result = result   
            return JsonResponse({"response": result}, status=200)
      
        return render(request, 'statistique/index.html', {  'lstTechniques' : len(Technique.nodes.all()),
                                                            'lstStudent' : len(Student.nodes.all()),
                                                            'lstGroup' : len(Group.nodes.all()),                              
                                                        })
    else :
        return render(request, "authentication/signin.html")

@csrf_exempt
def getData(request):
    try: 
        data = []
        
        if request.GET.get("type") == "TE" : 
            techniques = Technique.nodes.all()
            for technique in techniques :
                obj = {
                    "techniqueCd": technique.techniqueCd,
                    "techniqueName": technique.techniqueName,
                }
                data.append(obj)
        elif request.GET.get("type") == "ST" : 
            students = Student.nodes.all()
            for student in students: 
                obj = {
                    "studentCd": student.studentCd,
                    "fullNameStudent": student.fullNameStudent,
                }
                data.append(obj) 
        else : 
            groups = Group.nodes.all()
            for group in groups : 
                obj = {
                    "groupCd": group.groupCd,
                    "groupName": group.groupName,
                }
                data.append(obj)
                
        return JsonResponse({"data": data}, status=200)    
    except:
        response = {"error": "Error occurred"}

def getListTechByGroup(request):
    try: 
        result = []
        
        return result
    except: 
        return False

def signup(request):

    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()

        messages.success(request, "Your Account has been successfully created.")

        return redirect('signin')

    return render(request, "authentication/signup.html")

@csrf_exempt
def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signup')
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request) 
    messages.success(request, "Logged Out Successfully!")
    return redirect('home') 