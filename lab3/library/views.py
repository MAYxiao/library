from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection,transaction  
from django.shortcuts import render_to_response
from lab3.library.models import *  
import MySQLdb

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
        for i in name:
            for j in i:
                na = j
        cursor.close()
        dic = {'books':books,'name':na}
        return render_to_response('library/author_book.html',dic)
    else:
        return render_to_response('library/author_book.html', {'error': True})

def update(request):
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
    elif 'publisher' in request.GET and 'time' in request.GET and 'price' in request.GET and 'name' in request.GET and 'age' in request.GET and 'country' in request.GET and 'title' in request.GET:
        publisher = request.GET['publisher']
        time = request.GET['time']
        price = request.GET['price']
        name = request.GET['name']
        age = request.GET['age']
        country = request.GET['country']
        title = request.GET['title']
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
            aid = str(row[0]) 
        cursor.execute('update Book set AuthorID=\''+aid+'\',Publisher=\''+publisher+'\',PublishDate=\''+time+'\',Price=\''+price+'\' where TITLE = \''+title+'\'')
        transaction.commit_unless_managed()
        cursor.execute('select * from Book where TITLE = \''+title+'\'')
        bookinfo = cursor.fetchall();
        cursor.close()
        dic={'bookinfo':bookinfo,'userinfo':userinfo,'title':title}
        return render_to_response('library/abinfo.html',dic)
    else:
        return render_to_response('library/author_book.html', {'error': True})

def insert(request):
    if 'name' in request.GET and request.GET['name'] and 'isbn' not in request.GET:
        name = request.GET['name']
        cursor = connection.cursor()
        i = cursor.execute('select * from Author where Name=\''+name+'\'')
        if i!=0:
            flag = 1
        else:
            flag = 0
        transaction.commit_unless_managed()
        cursor.close()
        dic={'name':name,'flag':flag}
        return render_to_response('library/insert.html',dic)
    elif 'title' in request.GET and 'isbn' in request.GET and 'publisher' in request.GET and 'time' in request.GET and 'price' in request.GET and 'name' in request.GET:
        publisher = request.GET['publisher']
        time = request.GET['time']
        price = request.GET['price']
        name = request.GET['name']
        title = request.GET['title']
        isbn = request.GET['isbn']
        cursor = connection.cursor()
        i = cursor.execute('select * from Book where ISBN=\''+isbn+'\'')

        if 'age' in request.GET and request.GET['age'] and 'country' in request.GET and request.GET['country']:
            age = request.GET['age']
            country = request.GET['country']
            if i!=0:
                cursor.close()
                return render_to_response('library/insert.html/?title=\''+title+'\'&isbn=\''+isbn+'\'&publisher=\''+publisher+'\'&time=\''+time+'\'&price=\''+price+'\'&age=\''+age+'\'&country=\''+country+'\'', {'error': True})
            else:
                cursor.execute('insert into Author(Name,Age,Country) values (\''+name+'\',\''+age+'\',\''+country+'\')')
                transaction.commit_unless_managed()
                cursor.execute('select * from Author where Name = \''+name+'\'')
                userinfo = cursor.fetchall()
                for row in userinfo:
                    aid = str(row[0]) 
                cursor.execute('insert into Book(ISBN,TITLE,AuthorID,Publisher,PublishDate,Price) values (\''+isbn+'\',\''+title+'\',\''+aid+'\',\''+publisher+'\',\''+time+'\',\''+price+'\')')
                transaction.commit_unless_managed()
                cursor.execute('select * from Book where ISBN=\''+isbn+'\'')
                bookinfo = cursor.fetchall()
                cursor.close()
                dic={'bookinfo':bookinfo,'userinfo':userinfo,'title':title}
                return render_to_response('library/abinfo.html',dic)
        else:
            if i!=0:
                cursor.close()
                return render_to_response('library/insert.html/?title=\''+title+'\'&isbn=\''+isbn+'\'&publisher=\''+publisher+'\'&time=\''+time+'\'&price=\''+price+'\'', {'error': True})
            else:
                cursor.execute('select * from Author where Name = \''+name+'\'')
                userinfo = cursor.fetchall()
                for row in userinfo:
                    aid = str(row[0]) 
                cursor.execute('insert into Book(ISBN,TITLE,AuthorID,Publisher,PublishDate,Price) values (\''+isbn+'\',\''+title+'\',\''+aid+'\',\''+publisher+'\',\''+time+'\',\''+price+'\')')
                transaction.commit_unless_managed()
                cursor.execute('select * from Book where ISBN=\''+isbn+'\'')
                bookinfo = cursor.fetchall()
                cursor.close()
                dic={'bookinfo':bookinfo,'userinfo':userinfo,'title':title}
                return render_to_response('library/abinfo.html',dic)
    else:
        cursor.close()
        return render_to_response('library/insert.html', {'error': True})
        