from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lists.models import List, UserList
# Create your views here.

def results(request):
    if request.method == 'POST':
        tag = request.POST['tag']
        location = request.POST['location']
        reputation = request.POST['reputation']
        pages = request.POST['pages']

        # You can now manipulate the form data.
        resultList ={}
        resultList = getResults(tag,location, reputation, pages)
        request.session['resultList'] = resultList

    if request.method == 'GET' and 'profileImage' in request.GET:
        profileImage = request.GET['profileImage']
        profileLink = request.GET['profileLink']
        displayName = request.GET['displayName']
        userReputation = request.GET['reputation']
        userLocation = request.GET['location']
        userTag = request.GET['tag']
        answerScore = request.GET['answerScore']
        answerCount = request.GET['answerCount']
        listName = request.GET['myFavourites']
        bronzeCount = request.GET['bronze']
        silverCount = request.GET['silver']
        goldCount = request.GET['gold']

        current_user = request.user
        lists = List.objects.filter(userName__username = current_user.username,listName = listName )

        if len(lists) == 0:
            newList = List(userName = current_user, listName = listName)
            newList.save()
        
        lists = List.objects.filter(userName__username = current_user.username,listName = listName )

        newUserList = UserList(listID = lists[0], userDisplayName = displayName, profileImage =profileImage, profileLink = profileLink, reputation = userReputation, location = userLocation, tagName = userTag, answerScore = answerScore, answerCount= answerCount, bronzeCount = bronzeCount, silverCount= silverCount, goldCount=goldCount )
        newUserList.save()

    tupleList = tuple(request.session['resultList'].items())
    paginator = Paginator(tupleList, 20) 
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    current_user = request.user

    lists = List.objects.filter(userName__username = current_user.username)

    print(lists)
    
    context ={
        'resultList': paged_results,
        'lists': lists
    }
    return render(request,'results.html', context)

    



import requests
import urllib.parse
params = {
        "site" : "stackoverflow",
        "key"  : "FjjuUlAs4GvIx234fokbXg(("
        }

def getResults(tagName, locationName, reputationScore, pages):
    resultsList ={}
    pages = int(pages)
    for x in range(1,pages+1):

        BASEURL = "https://api.stackexchange.com/2.2/users?pagesize=100&order=desc&sort=reputation&page=" +str(x)


        r = requests.get(BASEURL, params=params)

        data=r.json()

 
        for user in data['items']:
            newUser =()
            #check if location is in user and the location field enter was not empty
            if "location" in user and locationName != "":
#################################################################################################
                #checking if reputation score is not empty and tage name is not empty
                if reputationScore !="" and tagName !="":
                    #checks if location and reptuation match values
                    if locationName.lower() in user["location"].lower() and int(user["reputation"]) >= int(reputationScore):
                        #CHECK FOR TAG
                        newUser = checkUserTag(user, tagName)
#########################################################################################

                #checks that reputation score is not empty and tag name is
                elif reputationScore !="" and tagName =="":
                    #checks location value in user object and reputation score
                    if locationName.lower() in user["location"].lower() and int(user["reputation"]) >= int(reputationScore):
                        #adds user to result list
                        newUser = (user['display_name'],user['link'], user["location"],user['reputation'] ," "," "," ",user['profile_image'],user["badge_counts"]['bronze'],user["badge_counts"]['silver'],user["badge_counts"]['gold'])
##############################################################################################
                #checks to see if reputation score is empty and tag name isnt  
                elif reputationScore =="" and tagName != "":
                    #checks locationname is equal, then checks for user tags
                    if locationName.lower() in user["location"].lower():
                        #CHECK FOR TAG
                        newUser = checkUserTag(user, tagName)
                                #checks to see if reputation score is empty and tag name isnt  
                elif reputationScore =="" and tagName == "":
                    #checks locationname is equal, then checks for user tags
                    if locationName.lower() in user["location"].lower():
                        #CHECK FOR TAG
                        newUser = (user['display_name'],user['link'], user["location"]," " ," "," "," ",user['profile_image'],user["badge_counts"]['bronze'],user["badge_counts"]['silver'],user["badge_counts"]['gold'])
######################################################################################
            #if location is not specified
            elif locationName =="":
###########################################################################################
                #checking if reputation score is not empty and tage name is not empty
                if reputationScore !="" and tagName !="":
                    if int(user["reputation"]) >= int(reputationScore):
                        #CHECK FOR TAG
                        newUser = checkUserTag(user, tagName)
###########################################################################################
                #checks that reputation score is not empty and tag name is
                elif reputationScore !="" and tagName =="":
                    if int(user["reputation"]) >= int(reputationScore):
                    #adds user to result list
                        newUser = (user['display_name'],user['link'], "",user['reputation'] ," "," "," ",user['profile_image'],user["badge_counts"]['bronze'],user["badge_counts"]['silver'],user["badge_counts"]['gold'])
############################################################################################
                elif reputationScore =="" and tagName != "":
                        #CHECK FOR TAG
                        newUser = checkUserTag(user, tagName)
##################################################################################################
            #if location is not in user and the location is specified in search query, skip user
            elif "location" not in user and locationName != "":
                pass

            if len(newUser) > 0:
                resultsList[newUser[0]] =(newUser[1],newUser[2],newUser[3],newUser[4],newUser[5],newUser[6],newUser[7],newUser[8],newUser[9],newUser[10])
            
    return(resultsList)

def checkUserTag(user, tagName):
    newUser=()
    userID = user['user_id']
    BASEURL = "https://api.stackexchange.com/2.2/users/" +str(userID) +"/top-tags"

    j = requests.get(BASEURL, params=params)

    tagData = j.json()

    for tag in tagData['items']:
        if "location" in user and tagName == tag['tag_name']:
            newUser = (user['display_name'],user['link'], user["location"],user['reputation'] ,tag['tag_name'],tag['answer_score'],tag['answer_count'],user['profile_image'],user["badge_counts"]['bronze'],user["badge_counts"]['silver'],user["badge_counts"]['gold'])
        elif "location" not in user and tagName == tag['tag_name']:
            newUser = (user['display_name'],user['link']," ",user['reputation'] ,tag['tag_name'],tag['answer_score'],tag['answer_count'],user['profile_image'],user["badge_counts"]['bronze'],user["badge_counts"]['silver'],user["badge_counts"]['gold'])


    return(newUser)


def moreInfo(request):

        if request.method == 'GET':
            profileImage = request.GET['profileImage']
            displayName = request.GET['displayName']
            userReputation = request.GET['reputation']
            userTag = request.GET['tag']
            answerScore = request.GET['answerScore']
            answerCount = request.GET['answerCount']
            bronzeCount = request.GET['bronze']
            silverCount = request.GET['silver']
            goldCount = request.GET['gold']


            data = [profileImage, displayName, userReputation, userTag, answerScore, answerCount, bronzeCount,silverCount,goldCount]

            context={
                "userInformation": data
            }

            return render(request, "userInfo.html", context)
