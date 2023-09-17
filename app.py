from flask import Flask, render_template, redirect, request, url_for, flash, jsonify, session
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Userdb, Frienddb, Messagedb

import datetime

def rety(sdate):
    return int(str(sdate).split('-')[0])

def retb(k):
    if str(k)=='10':
        return 'Computer Science & Engineering'
    elif str(k)=='00':
        return 'Civil Engineering'
    elif str(k) == '13':
        return 'Information Technology'
    elif str(k) == '20':
        return 'Electrical Engineering'
    elif str(k) == '31':
        return 'Electrical & Communication Engineering'
    elif str(k) == '40':
        return 'Mechanical Engineering'
    elif str(k) == '50':
        return 'Chemical Engineering'


# For the user database
engine = create_engine('sqlite:///userdb.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# For the friends database
fengine = create_engine('sqlite:///friendsdb.db', connect_args={'check_same_thread': False})
Base.metadata.bind = fengine
FSession = sessionmaker(bind=fengine)

# For the messages database
mengine = create_engine('sqlite:///messagesdb.db', connect_args={'check_same_thread': False})
Base.metadata.bind = mengine
MSession = sessionmaker(bind=mengine)


app = Flask(__name__,template_folder='./templates')
app.debug = True
app.secret_key = os.urandom(12)



@app.route('/')
def index():
    return render_template('index.html')


#signup

@app.route('/signup/',methods=['POST','GET'])
def signup():

    sess=DBSession()

    if request.method=='POST':

        cdate = str(datetime.datetime.now()).split(' ')[0]

        bdate=request.form['dob']

        cy=rety(cdate)

        by=rety(bdate)

        calage=cy-by

        uy=cy%100-int(str(request.form['rno'])[0:2])

        bcode=str(request.form['rno'])[5:7]

        if request.form['sex']=='female':
            prflpic='images/defaultuserf.png'
        else:
            prflpic = 'images/defaultuser.png'


        newuser = Userdb(rno=request.form['rno'],name=request.form['name'],sex=request.form['sex'],DOB=bdate,DOJ=cdate,age=calage,year=uy,email=request.form['email'], username=request.form['username'], password=request.form['password'],branch=retb(bcode),prflpic=prflpic)

        qdata=sess.query(Userdb).filter_by(rno=newuser.rno).first()

        if qdata is not None:
            flash("false")
            return redirect(url_for('index'))

        else:
            sess.add(newuser)

            sess.commit()

            flash("true")
            return redirect(url_for('index'))
    else:

        return redirect(url_for('index'))

#Login

@app.route('/login/',methods=['POST','GET'])
def login():
    sess = DBSession()
    if request.method=='POST':
        qdata=sess.query(Userdb).filter_by(username=request.form['username'],password=request.form['password']).first()
        if qdata is not None:
            session['logged_in'] = True
            flash("loggedin")
            return redirect(url_for('home',rno=qdata.rno))

        else:
            session['logged_in'] = False

            flash("failed")
            return redirect(url_for('index'))
    else:

        return redirect(url_for('index'))


#profile

@app.route('/<int:rno>/home/')
def home(rno):
    if session.get('logged_in'):
        sess = DBSession()
        qdata=sess.query(Userdb).filter_by(rno=rno).one()
        fsess = FSession()
        fdata = fsess.query(Frienddb).all()
        return render_template('home.html',data=qdata,fdata=fdata)
    else:
        return redirect(url_for('index'))

#logout

@app.route('/logout/')
def logout():
    session['logged_in']=False
    return redirect(url_for('index'))

#forget
@app.route('/forget/')
def forget():
    return render_template('forget.html')

@app.route('/<int:rno>/profile/')
def profile(rno):
    if session.get('logged_in'):
        sess = DBSession()
        qdata = sess.query(Userdb).filter_by(rno=rno).one()
        adata = sess.query(Userdb).all()
        fsess = FSession()
        fdata = fsess.query(Frienddb).all()
        fd=[]
        for a in adata:
            for f in fdata:
                    if (a.rno==f.frsend and f.frget==rno and f.accept==1) or (a.rno==f.frget  and f.frsend==rno and f.accept==1):
                        fd.append(a)
        print("hii")
        return render_template('profile.html', data=qdata,fd=fd,cf=len(fd))
    else:
        return redirect(url_for('index'))

@app.route('/<int:rno>/notification/')
def notification(rno):
    if session.get('logged_in'):
        sess = DBSession()
        qdata = sess.query(Userdb).filter_by(rno=rno).one()
        fsess = FSession()
        fdata = fsess.query(Frienddb).all()
        return render_template('notification.html', data=qdata,fdata=fdata)
    else:
        return redirect(url_for('index'))

@app.route('/<int:rno>/<int:orno>/message/')
def message(rno,orno):

    if session.get('logged_in'):

        mu=0
        sess = DBSession()
        msess = MSession()
        qdata = sess.query(Userdb).filter_by(rno=rno).one()

        fsess = FSession()
        adata = sess.query(Userdb).all()
        fdata = fsess.query(Frienddb).all()
        fd = []
        for a in adata:
            for f in fdata:
                if (a.rno == f.frsend and f.frget == rno and f.accept == 1) or (a.rno == f.frget and f.frsend == rno and f.accept == 1):
                    fd.append(a)
                if orno==a.rno:
                    mu=a


        if len(fd)>0 and orno==0:
            mu=fd[0]
            if mu.rno < rno:
                mid = str(rno) + str(mu.rno)
            else:
                mid = str(mu.rno) + str(rno)
            mdata = msess.query(Messagedb).filter_by(mid=mid).all()
        else:
            if rno < orno:
                mid = str(orno) + str(rno)
            else:
                mid = str(rno) + str(orno)
            mdata = msess.query(Messagedb).filter_by(mid=mid).all()
        nmh=0
        if len(fd)==0:
            nmh=1

        return render_template('messages.html', data=qdata,fd=fd,mu=mu,nmh=nmh,mlen=len(fd),mdata=mdata)

    else:

        return redirect(url_for('index'))


@app.route('/<int:rno>/<int:orno>/msend/',methods=['POST','GET'])
def msend(rno,orno):
    a=0
    print(a)
    a += 1

    if session.get('logged_in'):
        print(a)
        a += 1
        if request.method=='POST':
            print(a)
            a += 1
            msess=MSession()
            print(a)
            a += 1
            if rno<orno:
                mid=str(orno)+str(rno)
            else:
                mid=str(rno)+str(orno)
            print(a)
            a += 1
            sendm=request.form['msgd']
            print(a)
            a += 1
            sendd = str(datetime.datetime.now())
            print(a)
            a += 1
            print(a)
            a+=1
            newm=Messagedb(mid=mid,msend=rno,mget=orno,sendm=sendm,sendd=sendd,getv=0)
            print(a)
            a += 1
            msess.add(newm)
            print(a)
            a += 1
            msess.commit()
            print(a)
            a += 1
            return redirect(url_for('message',rno=rno,orno=orno))
        else:
            return redirect(url_for('message', rno=rno, orno=orno))

    else:
        return redirect(url_for('index'))




@app.route('/<int:rno>/findfriends/')
def findfriends(rno):
    if session.get('logged_in'):
        sess = DBSession()
        qdata = sess.query(Userdb).filter_by(rno=rno).one()
        alldata=sess.query(Userdb).all()
        fsess = FSession()
        fsdata = fsess.query(Frienddb).filter_by(frsend=rno).all()
        fgdata= fsess.query(Frienddb).filter_by(frget=rno).all()
        fd={}
        nfs=1
        nfg=1
        for i in fsdata:
            if i.accept==0:
                fd[i.frget]=1
                nfs=0
            else:
                fd[i.frget]=0
        for i in fgdata:
            if i.accept==0:
                fd[i.frsend]=2
                nfg=0
            else:
                fd[i.frsend]=0
        for i in fd:
            print(i, fd[i])
        return render_template('findfriends.html', data=qdata,alldata=alldata,fd=fd,nfg=nfg,nfs=nfs)

    else:

        return redirect(url_for('index'))

@app.route('/<int:rno>/<int:orno>/oprofile/')
def oprofile(rno,orno):
    if session.get('logged_in'):
        sess = DBSession()
        qdata = sess.query(Userdb).filter_by(rno=rno).one()
        odata=sess.query(Userdb).filter_by(rno=orno).one()
        fsess = FSession()
        adata = sess.query(Userdb).all()
        fdata = fsess.query(Frienddb).all()
        fd = []
        for a in adata:
            for f in fdata:
                if (a.rno == f.frsend and f.frget == orno and f.accept == 1) or (a.rno == f.frget and f.frsend == orno and f.accept == 1):
                    fd.append(a)
        f=0
        f = fsess.query(Frienddb).filter_by(frsend=rno, frget=orno).first()
        if f==None:
            f = fsess.query(Frienddb).filter_by(frsend=orno, frget=rno).first()
        if f==None:
            f=0
        elif f.frget==orno and f.accept==0:
            f=1
        elif f.frsend==orno and f.accept==0:
            f=2
        elif f.accept==1:
            f=3
        print(f)
        return render_template('oprofile.html', data=qdata,odata=odata,f=f,fd=fd,cf=len(fd))
    else:
        return redirect(url_for('index'))

@app.route('/<int:rno>/<int:orno>/accept/')
def faccept(rno,orno):
    if session.get('logged_in'):
        fsess = FSession()
        rd = fsess.query(Frienddb).filter_by(frsend=orno, frget=rno).first()
        rd.accept=1
        fsess.add(rd)
        fsess.commit()
        return redirect(url_for('findfriends', rno=rno))
    else:
        return redirect(url_for('index'))

@app.route('/<int:rno>/<int:orno>/send/')
def fsend(rno, orno):
    if session.get('logged_in'):
        fsess = FSession()
        sendd = str(datetime.datetime.now()).split(' ')[0]
        newfr=Frienddb(frsend=rno,frget=orno,sendd=sendd,accept=0)
        fsess.add(newfr)
        fsess.commit()
        return redirect(url_for('findfriends', rno=rno))
    else:
        return redirect(url_for('index'))


@app.route('/<int:rno>/<int:orno>/<string:task>/')
def delr(rno,orno,task):
    print(rno,orno,task)
    if session.get('logged_in'):
        fsess = FSession()
        if task=="delr":
            dr=fsess.query(Frienddb).filter_by(frsend=rno,frget=orno).first()
        elif task=="rejr":
            dr = fsess.query(Frienddb).filter_by(frsend=orno, frget=rno).first()
        elif task=="unf":
            dr = fsess.query(Frienddb).filter_by(frsend=rno, frget=orno).first()
            if dr==None:
                dr = fsess.query(Frienddb).filter_by(frsend=orno, frget=rno).first()
        fsess.delete(dr)
        fsess.commit()
        return redirect(url_for('findfriends', rno=rno))
    else:
        return redirect(url_for('index'))

@app.route('/<int:rno>/search/',methods=['POST','GET'])
def search(rno):
    if session.get('logged_in') and request.method=='POST':
        searchd=request.form['searchd']
        sess=DBSession()
        qdata = sess.query(Userdb).filter_by(rno=rno).first()
        alldata=sess.query(Userdb).all()
        fsess = FSession()
        fsdata = fsess.query(Frienddb).filter_by(frsend=rno).all()
        fgdata = fsess.query(Frienddb).filter_by(frget=rno).all()
        fd = {}
        for i in fsdata:
            if i.accept == 0:
                fd[i.frget] = 1

            else:
                fd[i.frget] = 0
        for i in fgdata:
            if i.accept == 0:
                fd[i.frsend] = 2

            else:
                fd[i.frsend] = 0
        searchdata=[]
        for dd in alldata:
            if dd.rno==searchd or dd.name==searchd or dd.sex==searchd or dd.age==searchd or dd.year==searchd or dd.branch==searchd or dd.email==searchd or dd.username==searchd:
                searchdata.append(dd)

        return render_template('searchresult.html', data=qdata,fd=fd,searchdata=searchdata,searchd=searchd,cs=len(searchdata))
    else:
        return redirect(url_for('index'))



@app.route('/dispall/')
def dispall():
    sess=DBSession()
    alldata=sess.query(Userdb).all()
    s=str()

    for i in alldata:
        s+='<div style="border:2px solid red">'+'<h1>'+str(i.name)+'</h1>'+'<h1>'+str(i.rno)+'</h1>'+'<h1>'+str(i.sex)+'</h1>'+'<h1>'+str(i.age)+'</h1>'+'<h1>'+str(i.year)+'</h1>'+'<h1>'+str(i.branch)+'</h1>'+'<h1>'+str(i.DOB)+'</h1>'+'<h1>'+str(i.DOJ)+'</h1>'+'<h1>'+str(i.email)+'</h1>'+'<h1>'+str(i.username)+'</h1>'+'<h1>'+str(i.password)+'</h1>'+'<h1>'+str(i.aboutu)+'</h1>'+'<h1>'+str(i.prflpic)+'</h1>'+'<img src="{{ url_for("static",filename="'+str(i.prflpic)+'")}}" height="100px" width="100px"/>'+'</div>'

    return s


if __name__ == '__main__':
    app.run()
