from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection,transaction  
from django.shortcuts import render_to_response
from lab3.library.models import *  
import MySQLdb
  
def ClassroonAdd(request):  
    if 'name' in request.GET and request.GET['name'] and 'tutor' in request.GET and request.GET['tutor']:  
        name = request.GET['name']  
        tutor = request.GET['tutor']  
        cursor=connection.cursor()  
        sql='insert into Author (AuthorID,Country,Name,Age) values (\''+name+'\',\''+tutor+'\',\'a\',20)'  
        cursor.execute(sql)  
        transaction.commit_unless_managed()  
        cursor.close()  
          
        return render_to_response('library/Classroom_Add_results.html',  
            {'name': name})  
    else:  
        return render_to_response('library/Classroom_Add.html', {'error': True}) 