from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import Template,Context
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import cursor
def index(request):
    doc_externo=open("plantilla\index.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def perfil(request,id_usu):
    miconexion = mysql.connector.connect(user="root",password="root",host="localhost",database="mekima")
    cursor = miconexion.cursor()
    q = "select * from usuarios where id_usu = "+id_usu+""
    print(id_usu)
    cursor.execute(q)
    rs=cursor.fetchone()
    clas=""
    try:
        name=rs[1]
        email=rs[2]
        passw=rs[3]
        clas=rs[4]
        if (clas==None):
            clas=""
    except:
        name=""
        email=""
        passw=""
    doc_externo=open("plantilla\perfil.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context({"name":name,"email":email,"pass":passw, "clas":clas})
    documento=plt.render(ctx)
    return HttpResponse(documento)
def iniciarCuenta(request):
    doc_externo=open("plantilla\iniciarCuenta.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def iniciarSesion(request):
    username=""
    password=""
    username=request.GET["username"]
    password=request.GET["password"]
    id_usu=""
    print(username, password)
    miconexion = mysql.connector.connect(user="root",password="root",host="localhost",database="mekima")
    cursor = miconexion.cursor()
    q = "select * from usuarios where usu = '"+username+"'"
    cursor.execute(q)
    rs=cursor.fetchone()
    try:
        id_usu=rs[0]
    except:
        id_usu="0"
    print(username, password,id_usu)
    linkR="/perfil/"+str(id_usu)+" "
    if(id_usu==None):
        linkR="/iniciarCuenta"
    return redirect(linkR, permanent=True)
def crearCuenta(request):
    doc_externo=open("plantilla\crearCuenta.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def crearCuentaN(request):
    username=request.GET["username"]
    password=request.GET["password"]
    email=request.GET["email"]
    print(username, password,email)
    miconexion = mysql.connector.connect(user="root",password="root",host="localhost",database="mekima")
    cursor = miconexion.cursor()
    q = "INSERT INTO usuarios (usu,correo,contraseña) VALUES ('"+username+"','"+email+"','"+password+"')"
    cursor.execute(q)
    miconexion.commit()
    return redirect("/iniciarCuenta", permanent=True)
