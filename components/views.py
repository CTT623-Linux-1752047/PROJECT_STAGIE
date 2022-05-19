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
          
            searchCondition1 = request.POST.get("searchCondition1")
            searchCondition2 = request.POST.get("searchCondition2")
            searchCondition3 = request.POST.get("searchCondition3")
            
            result = False
            
            if searchCondition1 != "" :
                lstGroupByTech = Technique.getGroupCodeByTechnique(searchCondition1)
                if len(lstGroupByTech) > 0 : 
                    lstDataBarChartEnCours = []
                    lstDataBarChartAcquis = []
                    lstDataBarChartMatrise = []
                    
                    for group in lstGroupByTech[0]: 
                        lstDataBarChartEnCours.append(Technique.cntStudentByTechniqueAndGroup(searchCondition1,group,"L1"))
                        lstDataBarChartAcquis.append(Technique.cntStudentByTechniqueAndGroup(searchCondition1,group,"L2"))
                        lstDataBarChartMatrise.append(Technique.cntStudentByTechniqueAndGroup(searchCondition1,group,"L3"))
                        
                    lstGroupByTech.append(lstDataBarChartEnCours)
                    lstGroupByTech.append(lstDataBarChartAcquis)
                    lstGroupByTech.append(lstDataBarChartMatrise)
                
                result =  {
                    "techCode" : searchCondition1,
                    "pieChart" : [Technique.cntTechFollowLevelByID(searchCondition1,"L1"), # en cours
                                  Technique.cntTechFollowLevelByID(searchCondition1, "L2"), # acquis
                                  Technique.cntTechFollowLevelByID(searchCondition1, "L3")],  # maîtrise     
                    "barChart" : lstGroupByTech
                }   
            return JsonResponse({"response": result}, status=200)
        try:
            techniques = Technique.nodes.all()
            lstTech = []
            for technique in techniques :
                obj = {
                    "techniqueCd": technique.techniqueCd,
                    "techniqueName": technique.techniqueName,
                }
                lstTech.append(obj)
                
            groups = Group.nodes.all()
            lstGroup = []
            for group in groups : 
                obj = {
                    "groupCd": group.groupCd,
                    "groupName": group.groupName,
                }
                lstGroup.append(obj)
            
            students = Student.nodes.all()
            lstStudent = []
            for student in students: 
                obj = {
                    "studentCd": student.studentCd,
                    "fullNameStudent": student.fullNameStudent,
                }
                lstStudent.append(obj)
                
            relationshipTech = {
                "hasConcurrencyByExtension" : Technique.countRelationship("hasConcurrencyByExtension"),
                "hasPartialConcurrency" : Technique.countRelationship("hasPartialConcurrency"),
                "hasGlobalConcurrency" : Technique.countRelationship("hasGlobalConcurrency"),}
            relationStudent = {
                "enCours" : Student.countStudentByLevel("L1"),
                "Acquis" : Student.countStudentByLevel("L2"),
                "Maitrise" : Student.countStudentByLevel("L3"),
            }
        except:
            response = {"error": "Error occurred"}
      
        return render(request, 'statistique/index.html', {
                                                            'lstTechniques': lstTech, 
                                                            'lstStudent' : lstStudent, 
                                                            'lstGroup': lstGroup,
                                                            'relationshipTech' :  relationshipTech,
                                                            'relationshipStudent' : relationStudent
                                                        })
    else :
        return render(request, "authentication/signin.html")

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