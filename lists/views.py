from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import List, UserList

def savedLists(request):

    current_user = request.user

    lists = List.objects.filter(userName__username = current_user.username)


    paginator = Paginator(lists, 10) 
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    context = {
        'lists': paged_results
    }


    return render(request,'savedLists.html', context)

def userList(request, list_id):

    individualList = UserList.objects.filter(listID = list_id)

    request.session['currentList'] =list_id


    paginator = Paginator(individualList, 10) 
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    context={

        'individualList':paged_results
    }

    return render(request,'userList.html',context)

def removeList(request, list_id):
    
    List.objects.filter(listID=list_id).delete()

    current_user = request.user
    lists = List.objects.filter(userName__username = current_user.username)

    paginator = Paginator(lists, 10) 
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    context = {
        'lists': paged_results
    }
    

    return render(request,'savedLists.html', context)

def removeUserList(request, list_id):
 

    UserList.objects.filter(listID = request.session['currentList'],id = list_id).delete()

    individualList = UserList.objects.filter(listID = request.session['currentList'])

    paginator = Paginator(individualList, 10) 
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    context={

        'individualList':paged_results
    }

    context={

            'individualList':individualList
        }

    return render(request,'userList.html',context)