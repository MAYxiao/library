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
          
        return render_to_response('library/Classroom_Add_results.html', {'name': name})  
    else:  
        return render_to_response('library/Classroom_Add.html', {'error': True})

def index(request):
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
        cursor = connection.cursor()
        cursor.execute('select * from Book left join Author on Book.AuthorID=Author.AuthorID where Author.Name = \''+name+'\'')
        books = cursor.fetchall()
        transaction.commit_unless_managed()
        cursor.close()
        dic = {'books': books,'name':name}
        return render_to_response('library/author_book.html', dic)
    else:
        return render_to_response('library/index.html', {'error': True})

def bookinfo(request):
    if 'booktitle' in request.GET and request.GET['booktitle']:
        booktitle = request.GET['booktitle']
        cursor = connection.cursor()
        cursor.execute('select * from Book where TITLE=\''+booktitle+'\'')
        bookinfo = cursor.fetchall()
        cursor.execute('select * from Author right join Book on Author.AuthorID=Book.AuthorID where Book.TITLE = \''+booktitle+'\'')
        userinfo = cursor.fetchall()
        transaction.commit_unless_managed()
        cursor.close()
        dic = {'bookinfo':bookinfo,'title':booktitle,'userinfo':userinfo}
        return render_to_response('library/abinfo.html',dic)
    else:
        return render_to_response('library/author_book.html', {'error': True})

def delete(request):
    if 'title' in request.GET and request.GET['title'] and 'aid' in request.GET and request.GET['aid']:
        booktitle = request.GET['title']
        aid = request.GET['aid']
        cursor = connection.cursor()
        cursor.execute('delete from Book where TITLE=\''+booktitle+'\'')
        transaction.commit_unless_managed()
        cursor.execute('select * from Book where AuthorID=\''+aid+'\'')
        books = cursor.fetchall();
        cursor.execute('select Name from Author where AuthorID=\''+aid+'\'')
        name = cursor.fetchall();
        cursor.close()
        dic = {'books':books,'name':name}
        return render_to_response('library/author_book.html',dic)
    else:
        return render_to_response('library/author_book.html', {'error': True})

def update(request):
    global isbn
    if 'isbn' in request.GET and request.GET['isbn'] and 'aid' in request.GET and request.GET['aid']:
        isbn = request.GET['isbn']
        aid = request.GET['aid']
        
        cursor = connection.cursor()
        cursor.execute('select * from Book where ISBN = \''+isbn+'\'')
        bookinfo = cursor.fetchall()
        cursor.execute('select * from Author where AuthorID = \''+aid+'\'')
        userinfo = cursor.fetchall()
        transaction.commit_unless_managed()
        cursor.close()
        dic = {'bookinfo':bookinfo,'userinfo':userinfo}
        return render_to_response('library/update.html',dic)
    elif 'publisher' in request.GET and 'time' in request.GET and 'price' in request.GET and 'name' in request.GET and 'age' in request.GET and 'country' in request.GET:
        publisher = request.GET['publisher']
        time = request.GET['time']
        price = request.GET['price']
        name = request.GET['name']
        age = request.GET['age']
        country = request.GET['country']
        cursor = connection.cursor()
        cursor.execute('select * from Author where Name = \''+name+'\'')
        userinfo = cursor.fetchall();
        if userinfo:
            cursor.execute('update Author set Name = \''+name+'\',Age=\''+age+'\',Country=\''+country+'\' where Name = \''+name+'\'')
            transaction.commit_unless_managed()
            cursor.execute('select * from Author where Name = \''+name+'\'')
            userinfo = cursor.fetchall()
        else:
            cursor.execute('insert into Author(Name,Age,Country) values (\''+name+'\',\''+age+'\',\''+country+'\')')
            transaction.commit_unless_managed()
            cursor.execute('select * from Author where Name = \''+name+'\'')
            userinfo = cursor.fetchall()
        for row in userinfo:
            aid = row[0]
        cursor.execute('update Book set AuthorID=\''+aid+'\',Publisher=\''+publisher+'\',PublisherDate=\''+time+'\',Price=\''+price+'\' where ISBN = \''+isbn+'\'')
        transaction.commit_unless_managed()
        cursor.execute('select * from Book where ISBN = \''+isbn+'\'')
        bookinfo = cursor.fetchall();
        dic={'bookinfo':bookinfo,'userinfo':userinfo}
        return render_to_response('library/abinfo.html',dic)
    else:
        return render_to_response('library/author_book.html', {'error': True})

def result(request):
    if 'bookinfo' in request.GET and request.GET['bookinfo'] and 'userinfo' in request.GET and request.GET['userinfo']:
        bookinfo = request.GET['bookinfo']
        userinfo = request.GET['userinfo']
        cursor = connection.cursor()
        cursor.execute('select * from Book where ISBN = \''+isbn+'\'')
        bookinfo = cursor.fetchall()
        cursor.execute('select * from Author where AuthorID = \''+aid+'\'')
        userinfo = cursor.fetchall()
        transaction.commit_unless_managed()
        cursor.close()
        dic = {'bookinfo':bookinfo,'userinfo':userinfo}
        return render_to_response('library/update.html',dic)
    else:
        return render_to_response('library/author_book.html', {'error': True})
