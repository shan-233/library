from django.shortcuts import render, redirect
from libraryapp import models
from django.contrib.auth import authenticate
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import datetime
import random
from utils import mypage
from utils import mypage2
from django.db.models import Q

def index(request):
    booksTop = models.bookModel.objects.all().order_by('-bhit')[:5]
    bookname = request.GET.get('book_name')
    if bookname == None:
        books = models.bookModel.objects.all().order_by('-id')
        # 拿到总数据量
        total_count = books.count()
            # 从url拿到page参数
        current_page = request.GET.get("page", None)
        page_obj = mypage.MyPage(current_page, total_count, url_prefix="index", max_show=2)
            # 对总数据进行切片，拿到页面显示需要的数据
        data = books[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, "index.html", {"books": data, "page_html": page_html,"booksTop": booksTop})
    else:
        books = models.bookModel.objects.all().filter(Q(name__contains=bookname))
        # 拿到总数据量
        total_count = books.count()
            # 从url拿到page参数
        current_page = request.GET.get("page", None)
        page_obj = mypage2.MyPage(current_page, total_count, url_prefix="index", max_show=2, book_name=bookname)
            # 对总数据进行切片，拿到页面显示需要的数据
        data = books[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, "index.html", {"books": data, "page_html": page_html,'book_name':bookname,"booksTop": booksTop})

def login(request):  #登入
    messages = ''  #初始時清除訊息
    if request.method == 'POST':  #如果是以POST方式才處理
        name = request.POST['username'].strip()  #取得輸入帳號
        password = request.POST['passwd']  #取得輸入密碼
        user1 = authenticate(username=name, password=password)  #驗證
        if user1 is not None:  #驗證通過
            if user1.is_active:  #帳號有效
                if user1.is_superuser:  #帳號有效
                    auth.login(request, user1)  #登入
                    return redirect('/adminmain/')  #開啟管理頁面
                else:  #帳號無效 
                    # request.sessions["username"]=name
                    auth.login(request, user1)
                    return redirect('/usermain/')  #開啟使用者頁面
            else:  #帳號無效
                message = '帳號尚未啟用！'
        else:  #驗證未通過
            message = '登入失敗！'
    return render(request, "login.html", locals())

def logout(request):  #登出
    auth.logout(request)
    return redirect('/index/')   

#管理者首頁
def adminmain(request,bookid=None):
    nowuser = request.user.username
    if bookid == None:  
        books = models.bookModel.objects.all().order_by('-id')
    else:
        book = models.bookModel.objects.get(id=bookid)
        if book.borrower == '':
            os.remove(os.path.join(settings.MEDIA_ROOT, book.burl))
            book.delete() 
            return redirect('/adminmain/')
        else:
            return redirect('/adminmain/')
    booksTop = models.bookModel.objects.all().order_by('-bhit')[:5]
    bookname = request.GET.get('book_name')
    if bookname == None:
        books = models.bookModel.objects.all().order_by('-id')
        total_count = books.count()
        current_page = request.GET.get("page", None)
        page_obj = mypage.MyPage(current_page, total_count, url_prefix="adminmain", max_show=2)
        data = books[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, "adminmain.html", {"books": data, "page_html": page_html,"booksTop": booksTop,"nowuser":nowuser})
    else:
        books = models.bookModel.objects.all().filter(Q(name__contains=bookname))
        total_count = books.count()
        current_page = request.GET.get("page", None)
        page_obj = mypage2.MyPage(current_page, total_count, url_prefix="adminmain", max_show=2, book_name=bookname)
        data = books[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, "adminmain.html", {"books": data, "page_html": page_html,'book_name':bookname,"booksTop": booksTop,"nowuser":nowuser})

#使用者首頁
def usermain(request):
    nowuser = request.user.username
    booksTop = models.bookModel.objects.all().order_by('-bhit')[:5]
    bookname = request.GET.get('book_name')
    if bookname == None:
        books = models.bookModel.objects.all().order_by('-id')
        total_count = books.count()
        current_page = request.GET.get("page", None)
        page_obj = mypage.MyPage(current_page, total_count, url_prefix="usermain", max_show=2)
        data = books[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, "usermain.html", {"books": data, "page_html": page_html,"booksTop": booksTop,"nowuser":nowuser})
    else:
        books = models.bookModel.objects.all().filter(Q(name__contains=bookname))
        total_count = books.count()
        current_page = request.GET.get("page", None)
        page_obj = mypage2.MyPage(current_page, total_count, url_prefix="usermain", max_show=2, book_name=bookname)
        data = books[page_obj.start:page_obj.end]
        page_html = page_obj.page_html()
        return render(request, "usermain.html", {"books": data, "page_html": page_html,'book_name':bookname,"booksTop": booksTop,"nowuser":nowuser})

#新增書籍
def adminadd(request):
    message = ''
    nowuser = request.user.username
    name = request.POST.get('book_name', '')  #取得輸入資料
    isbn = request.POST.get('book_isbn', '')
    author = request.POST.get('book_author', '')
    theme = request.POST.get('book_theme', '')
    publish = request.POST.get('book_publish', '')
    publishyear = request.POST.get('book_publishyear', '')
    image = request.FILES.get('book_burl', '')
    desc = request.POST.get('book_desc', '')
    readurl = request.POST.get('book_readurl', '')
    if name!='':  
        uploaded_file = request.FILES['book_burl']
        fs = FileSystemStorage()  #上傳檔案
        filename = fs.save(uploaded_file.name,uploaded_file)
        unit = models.bookModel.objects.create(name=name, isbn=isbn, author=author, theme=theme,  desc=desc, publish=publish, publishyear=publishyear, burl=filename, readurl=readurl)
        unit.save()
        return redirect('/adminmain/')
    return render(request, "adminadd.html", locals())
#書籍詳細頁面
def book(request,bookid):
    book = models.bookModel.objects.get(id=bookid)
    sametheme = models.bookModel.objects.all().filter(Q(theme__contains=book.theme))
    list1=list(sametheme)
    for i in range(0,len(list1)):
        if list1[i].id==bookid:
            list1.pop(i)
            break
    list2=random.sample(list1,2)
    return render(request, "book.html", locals())
#使用者書籍詳細頁面
def userbook(request,bookid,btype=None):
    book = models.bookModel.objects.get(id=bookid)
    nowuser = request.user.username
    sametheme = models.bookModel.objects.all().filter(Q(theme__contains=book.theme))
    list1=list(sametheme)
    for i in range(0,len(list1)):
        if list1[i].id==bookid:
            list1.pop(i)
            break
    list2=random.sample(list1,2)
    if btype == 'borrow':
        if book.state == False:
            date = datetime.date.today() + datetime.timedelta(days=7)
            book.redate = date
            book.borrower = request.user.username
            book.connection = request.user.email
            book.state = True
            book.save()
            return redirect(f'/userbook/{bookid}')
    if btype == 'returnbook':
        if request.user.username == book.borrower: 
            book.state = False
            book.bhit=book.bhit+1 
            book.redate =''
            book.borrower = ''
            book.connection = ''
            book.save()
            return redirect(f'/userbook/{bookid}') 
    return render(request, "userbook.html", locals())
#管理者書籍詳細頁面
def adminbook(request,bookid):
    book = models.bookModel.objects.get(id=bookid)
    nowuser = request.user.username
    sametheme = models.bookModel.objects.all().filter(Q(theme__contains=book.theme))
    list1=list(sametheme)
    for i in range(0,len(list1)):
        if list1[i].id==bookid:
            list1.pop(i)
            break
    list2=random.sample(list1,2)
    return render(request, "adminbook.html", locals())

#管理者維護書籍頁面
def adminfix(request, bookid=None,uptype=None):
    books = models.bookModel.objects.get(id=bookid)
    nowuser = request.user.username
    if uptype == 'update':
        books = models.bookModel.objects.get(id=bookid)
        books.name = request.POST.get('book_name', '')
        books.isbn = request.POST.get('book_isbn', '')
        books.author = request.POST.get('book_author', '')
        books.theme = request.POST.get('book_theme', '')
        books.publish = request.POST.get('book_publish', '')
        books.publishyear = request.POST.get('book_publishyear', '')
        books.desc = request.POST.get('book_desc', '')
        books.readurl = request.POST.get('book_readurl', '')
        books.save()     
        if request.FILES.get('book_burl', '') != '':
            books.burl = request.FILES.get('book_burl', '')
            books.save() 
            uploaded_file = request.FILES['book_burl']
            fs = FileSystemStorage()  #上傳檔案
            filename = fs.save(uploaded_file.name,uploaded_file) 
        return redirect('/adminmain/')  
    return render(request, "adminfix.html", locals())

def adminall(request):
    books = models.bookModel.objects.all().order_by('-id')
    nowuser = request.user.username
    return render(request, "adminall.html", locals())

def userstudy(request):
    nowuser = request.user.username
    books = models.bookModel.objects.all().filter(Q(borrower__exact=nowuser))
    return render(request, "userstudy.html", locals())

