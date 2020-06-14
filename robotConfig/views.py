from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import glob
from pathlib import Path
import json


# Validation function for Json
comparison = ['$eq', '$gt', '$lt', '$gte', '$lte', '$ne']
logic = ['$and', '$or', '$not']

def checkComponents(data):
    """
    Receives a Json with different Modules. Each module has conditions which should be properly formed according to the
    Grammar.
    The function loops over all the Modules and check (i.e. usng checkJson) that each <condition> is properly formed
    :param data: data is a Json object converted into a Python dictionary.
                 e.g. {
                          <moduleName1>: <conditions>,
                          <moduleName2>: <conditions>,
                          ...
                        }
    :return: True if it is validated as correctly formed grammar
    """
    for components in data.keys():
        if checkJson(data[components]) == False:
            return False
    return True


def checkJson(data):
    """
    Receives a condition (previously called by checkComponents) and evaluates if the Grammar is correct.

    The Grammar is correct if:

    1. The condition is boolean (true/false)
    2. It is a dictionary and
       2.1 There is only one element (i.e. len(data)==1)
           2.1.1 The element is a comparison (i.e. $le, $eq, etc) and has two children OR
           2.1.2 The element is a logic AND
                2.1.2.1 If the element is == $not AND it has a single child AND that child is correctly formed
                        (recurrent call to checkJson with the child element) OR
                2.1.2.2 If the element is $or OR $and AND it has two children AND both children are correctly formed
                        (recurrent call to checkJson with both children elements)

    :param data: A condition of a corresponding Module
    :return: True if it is validated as a correctly formed grammar
    """

    # If it is a boolean then it is correct
    if type(data) == bool:
        return True
    # Check if it is a dictionary
    if type(data) == dict:
        # If there is a single element it has to be either a comparison or a logic
        if len(data) == 1:
            singleElement = list(data.keys())[0]
            # If it is a comparison it is a leaf -> it has to have 2 elements
            if singleElement in comparison:
                # It has to have 2 components
                return len(data[singleElement]) == 2
            # Check if it is a logic
            elif singleElement in logic:
                # Logic has to have 2 elements if it is $and / $or -> call recursively
                # Logic has to have 1 element if it is a $not -> call recursively
                if singleElement in ['$and', '$or'] and len(data[singleElement]) == 2:
                    return checkJson(data[singleElement][0]) & checkJson(data[singleElement][1])
                if singleElement == '$not' and len(data[singleElement]) == 1:
                    return checkJson(data[singleElement])

    print(data)
    return False


# Views
# -----


def index(request):
    """
    Index endpoint (homepage) of app robotConfig
    It searches all the robotFiles in the database (i.e. filesystem in /robotConfig/database)
    It returns the list to populate the dropdown menu
    It renders the html template robotConfig/index.html

    :param request: HTTP request
    :return: Render the HTML and sent to the client
    """
    robotList = sorted([Path(f).stem for f in glob.glob('./robotConfig/database/*.json')])
    context = {'robotList': robotList, 'jsonRoboTxt':'', 'robotId':None, 'statusRobot':"-----"}
    return render(request,'robotConfig/index.html',context)


def showRobot(request, robot_id):
    """
    Once a robot is selected by dropdown menu (or by directly accessing the endpoint /robotConfig/#robotID# the
    configuration file is loaded.
    The file is checked to exist first, and then that is a Json. A status error is reported if there is a problem

    :param request: HTTP request
    :param robot_id: the id of the robot to load and to allow editing and saving
    :return: Render of the HTML with the loading Status and the robot configuration file into the text area
    """

    robotList = sorted([Path(f).stem for f in glob.glob('./robotConfig/database/*.json')])
    pathName = "./robotConfig/database/" + robot_id + ".json"
    outJson = ''
    statusTxt = 'Ready to Edit'
    try:
        f = open(pathName)
        data = json.load(f)
        outJson = json.dumps(data, indent =4, sort_keys = True)
        f.close()
    except FileNotFoundError:
        statusTxt = "Error: The robotId does not exist"
    except ValueError:
        statusTxt = "Error : Configuration file is not properly formatted"
        f.close()
    context = {'robotList': robotList, 'jsonRoboTxt': outJson, "robotId":robot_id, 'statusRobot': statusTxt}
    return render(request, 'robotConfig/index.html', context)


def updateRobot(request, robot_id):
    """
    The client submitted a change in the robot configuration. If the configuration is grammarly correct it will be saved
    as a json in robotConfig/database
    If the robot does not exist the client will be redirectly to the home page
    If the configuration is not a json an error indicating is not json will be displayed
    If the configuration is a json but the grammar is incorrect a message will be displayed

    :param request: HTTP request (POST) it should have the robot configuration in request.POST['txtArea']
    :param robot_id: The robot id being edited
    :return: A render of the HTMl with the Status (error, or file saved).
    """
    pathName = "./robotConfig/database/" + robot_id + ".json"
    robotList = sorted([Path(f).stem for f in glob.glob('./robotConfig/database/*.json')])
    outJson = ''
    if robot_id not in robotList:
        url_redirect = '/robotConfig'
        return redirect(url_redirect)

    else:
        statusTxt = "Saved"
        if request.method == "POST":
            txt = request.POST['txtArea'].strip()
            outJson = txt
            try:
                # Attempt to convert it to json
                received_json_data = json.loads(txt)
                if checkComponents(received_json_data):
                    with open(pathName,'w') as f:
                        json.dump(received_json_data,f)
                else:
                    statusTxt = "Error: Grammar error in the query"
            except ValueError:
                statusTxt = "Error : Configuration file is not properly formatted"
            except FileNotFoundError:
                statusTxt = "Error: The robotId does not exist"


    context = {'robotList': robotList, 'jsonRoboTxt': outJson, "robotId":robot_id, 'statusRobot': statusTxt}
    return render(request, 'robotConfig/index.html', context)
