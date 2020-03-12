import json
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from .serializers import *
from .models import *
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist
from decimal import *


class ProfessorsViewSet(viewsets.ModelViewSet):
    queryset = Professors.objects.all().order_by('profID')
    serializer_class = ProfessorsSerializer


@csrf_exempt
@require_http_methods(["GET"])
def GetProfessors(request):
    profs = Professors.objects.all()
    data = ProfessorsSerializer(profs, many=True).data
    return JsonResponse(data, safe=False)


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        if request.body is not None:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body['username']
            email = body['email']
            password = body['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return HttpResponse('The account: ' + username + ' has been successfully created', status=200)
        else:
            return HttpResponse('Invalid request', status=400)
    else:
        return HttpResponse('Invalid request', status=400)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        if request.body is not None:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body['username']
            password = body['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Succesfully logged in")
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username, password))
                return HttpResponse("Invalid login details given")
        else:
            return HttpResponse('Invalid')
    else:
        return HttpResponse('Invalid')

@csrf_exempt
def rate_professor(request):
    row_exists = False
    if request.method == 'POST':
        if request.body is not None:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            prof_field = body['profID']
            year_field = body['moduleYear']
            semseter_field = body['moduleSemester']
            profID1 = Professors.objects.filter(profID=prof_field)
            profID = profID1[0]
            module_field = body['moduleID']
            moduleID1 = ModuleCode.objects.filter(moduleID=module_field)
            moduleID = moduleID1[0]
            if str(module_field) == "CD1" and int(semseter_field) == 1 and str(year_field) == "2017" and (str(prof_field) == "JE1" or str(prof_field) == "VS1"):
                row_exists = True
                moduleInfo = ModuleYearSemester.objects.get(id=1)

            if str(module_field) == "CD1" and int(semseter_field) == 2 and str(year_field) == "2018" and str(prof_field) == "JE1":
                row_exists = True
                moduleInfo = ModuleYearSemester.objects.get(id=2)

            if str(module_field) == "PG1" and int(semseter_field) == 2 and str(year_field) == "2017" and str(prof_field) == "TT1":
                row_exists = True
                moduleInfo = ModuleYearSemester.objects.get(id=3)

            if str(module_field) == "PG1" and int(semseter_field) == 1 and str(year_field) == "2019" and str(prof_field) == "JE1":
                row_exists = True
                moduleInfo = ModuleYearSemester.objects.get(id=4)

            if row_exists:
                rating = body['rating']
                print("Adding new rating...")
                newRating = RateProfessor(profID=profID, moduleInfo=moduleInfo, rating=rating)
                newRating.save()
                return HttpResponse("Added record")
                return HttpResponse("Failed to add record - professor not recorded as teaching this module")
    return HttpResponse("Failed to add record")

@csrf_exempt
def logout_request(request):
    logout(request)
    print(request, "Logged out successfully!")
    return HttpResponse("Logged out successfully")


def list_professors(request):
    response = "----------------------------------------------------------------------------------------------------\n"
    response += "     Module                     Year      Semeseter              Professors\n"
    response += "----------------------------------------------------------------------------------------------------\n"
    if request.method == 'GET':
        if request.body is not None:
            for row in ModulesTaughtBy.objects.all():

                moduleInfo = row.moduleInfo
                padInt = 0
                padString = ""
                id = 0
                if str(moduleInfo.moduleID) == "CD1":
                    id = 1
                    padInt = 5
                if str(moduleInfo.moduleID) == "PG1":
                    id = 2
                for x in range(padInt):
                    padString += " "
                moduleCode = moduleInfo.moduleID
                moduleTitle1 = ModuleName.objects.filter(moduleID=id)
                moduleTitle = moduleTitle1
                year = moduleInfo.moduleYear
                semseter = moduleInfo.moduleSemester
                taughtBy = ""
                moduleProfessors = row.moduleProfessors
                rowString = str(row)
                trimRow = rowString[39:]
                trimRow2 = trimRow.replace('<ProfessorTitle:', '')
                excludeChars = '>]'
                for char in excludeChars:
                    trimRow2 = trimRow2.replace(char, "")
                response += str(moduleTitle[0]) + "  " + padString + str(year)  + "          " + str(semseter) + "      " + trimRow2 + "\n"

                print(row)

                print(moduleProfessors)
        return HttpResponse(response)
    return HttpResponse(response)


def view_professors_ratings(request):
    JE1total = 0
    JE1count = 0
    VS1total = 0
    VS1count = 0
    TT1total = 0
    TT1count = 0
    JE1rateString = ""
    VS1rateString = ""
    TT1rateString = ""
    response = ""
    if request.method == 'GET':
        if request.body is not None:
            for row in RateProfessor.objects.all():
                if str(row.profID) == 'JE1':
                    JE1total += row.rating
                    JE1count += 1
                if str(row.profID) == 'VS1':
                    VS1total += row.rating
                    VS1count += 1
                if str(row.profID) == 'TT1':
                    TT1total += row.rating
                    TT1count += 1
            JE1rating = JE1total / JE1count
            JE1decimalRating = Decimal(str(JE1rating)).quantize(Decimal('1.'), rounding=ROUND_UP)
            JE1intRating = int(JE1decimalRating)
            for x in range(JE1intRating):
                JE1rateString += "*"
            VS1rating = VS1total / VS1count
            VS1decimalRating = Decimal(str(VS1rating)).quantize(Decimal('1.'), rounding=ROUND_UP)
            VS1intRating = int(VS1decimalRating)
            for x in range(VS1intRating):
                VS1rateString += "*"
            TT1rating = TT1total / TT1count
            TT1decimalRating = Decimal(str(TT1rating)).quantize(Decimal('1.'), rounding=ROUND_UP)
            TT1intRating = int(TT1decimalRating)
            for x in range(TT1intRating):
                TT1rateString += "*"
            response += "The rating of Professor J. Excellent (JE1) is " + JE1rateString + "\n"
            response += "The rating of Professor V. Smart (VS1) is " + VS1rateString + "\n"
            response += "The rating of Professor T. Terrible (TT1) is " + TT1rateString + "\n"
            return HttpResponse(response)
        return HttpResponse("error")
    return HttpResponse("error")


@csrf_exempt
def get_ratings_for_professor(request):
    if request.method == 'POST':
        if request.body is not None:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            prof_field = body['profID']
            module_field = body['moduleID']
            count = 0
            total = 0
            for professor in RateProfessor.objects.filter(profID=prof_field):
                if str(professor.moduleInfo.moduleID) == str(module_field):
                    count += 1
                    total += professor.rating
            profRating = total/count
            decimalRating = Decimal(str(profRating)).quantize(Decimal('1.'), rounding=ROUND_UP)
            intRating = int(decimalRating)
            response = "The rating of "
            profTitle1 = ProfessorTitle.objects.filter(profID=prof_field)
            profTitle = str(profTitle1[0])
            response += profTitle
            id = 0
            if module_field == "CD1":
                id = 1
            if module_field == "PG1":
                id = 2
            moduleTitle1 = ModuleName.objects.filter(moduleID=id)
            moduleTitle = moduleTitle1[0]
            response += " in module "
            response += str(moduleTitle)
            response += " is "
            for x in range(intRating):
                response += "*"
            print(response)
            return HttpResponse(response)
    return HttpResponse('error')