import requests
import json

def login():
    username = input("username: ")
    password = input("password: ")
    details = {"username": username, "password": password}
    resp = requests.post('http://127.0.0.1:8000/Professors/login/', json=details)
    if resp.text == "Invalid login details given":
        print(resp.text)
        return False
    else:
        print(resp.json)
        print(resp.text)
        return True

def logout():
    resp = requests.get('http://127.0.0.1:8000/Professors/logout/')
    if resp.status_code!=200:
        print(resp.json)
    else:
        print(resp.json)
        print(resp.text)

def register():
        username = input("username: ")
        email = input("email: ")
        password = input("password: ")
        details = {"username": username, "email": email, "password": password}
        resp = requests.post('http://127.0.0.1:8000/Professors/register/', json=details)
        if resp.status_code != 200:
            print(str(resp.status_code))
            print('error')
        else:
            print(resp.json)
            print(resp.text)

def profIDs():
    resp = requests.get('http://127.0.0.1:8000/Professors/professor/')
    if resp.status_code!=200:
        print(resp.json)
    else:
        for profIDs in resp.json():
            print('{}'.format(profIDs['profID']))

def rateProf():
    profID = input("Professor ID: ")
    moduleID = input('Module ID: ')
    year = input("Year: ")
    semseter = input("Semester: ")
    rating = int(input("rating: "))
    userRating = {"profID": profID, "moduleID": moduleID, "moduleYear": year, "moduleSemester": semseter, "rating": rating}
    resp = requests.post('http://127.0.0.1:8000/Professors/rate/', json=userRating)
    if resp.status_code!=200:
        print(resp.json)
    else:
        print(resp.json)
        print(resp.text)

def averageRating():
    profID = input("Professor ID: ")
    moduleID = input("module ID: ")
    send = {"profID": profID, "moduleID": moduleID}
    resp = requests.post('http://127.0.0.1:8000/Professors/average/', json=send)
    if resp.status_code!=200:
        print(resp.json)
    else:
        print(resp.json)
        print(resp.text)

def listProfessors():
    resp = requests.get('http://127.0.0.1:8000/Professors/list/')
    if resp.status_code!=200:
        print(resp.json)
    else:
        print(resp.json)
        print(resp.text)

def viewProfRatings():
    resp = requests.get('http://127.0.0.1:8000/Professors/view/')
    if resp.status_code!=200:
        print(resp.json)
    else:
        print(resp.json)
        print(resp.text)

def clientLoop():
    while True:
        userInput = input("Enter request: ")
        if userInput == "logout":
            logout()
            break;
        if userInput == "professorid":
            profIDs()
        if userInput == "rate":
            rateProf()
        if userInput == "average":
            averageRating()
        if userInput == "list":
            listProfessors()
        if userInput == "view":
            viewProfRatings()

def loginLoop():
    while True:
        userInput = input("Please login, register or exit... ")
        if userInput == "register":
            register()
            if login() is True:
                clientLoop()
            elif login() is False:
                print("Failed to login")
                continue;
        if userInput == "login":
            if login() is True:
                clientLoop()
            elif login() is False:
                print("Failed to login")
                continue;
        if userInput == "exit":
            break;
loginLoop()
