from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import Template,Context
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import cursor
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import mediapipe as mp
import base64
import numpy as np
import cv2
from django.http import JsonResponse

def cifrarmensaje(msj,key):
	lm=msj.split(" ")
	cmc=""
	lmc=[]
	for i in lm:
		pal=cifrarpalabra(i,key)
		lmc.append(pal)
	for j in lmc:
		cmc=cmc+str(j)+" "    
	return cmc

def cifrarpalabra(m,k):
	lpc=[]
	lp=[]
	n,e=k
	cpc=""
	for i in m:
		x=buscarpos(i)
		lp.append(x)
	for j in lp:
		c=(j**e)%n
		lpc.append(c)
	for k in lpc:
		cpc=cpc+str(k)+" "
	return cpc	
	

def buscarpos(x):
	alf="abcdefghijklmnñopqrstuvwxyz.@ABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890"
	c=0
	for i in alf:
		if x==i:
			return c
		else:
			c=c+1	

def descifrarmensaje(msj,key):
	msj=msj.upper()
	lm=msj.split("  ")
	cmc=""
	lmc=[]
	for i in lm:
		pal=descifrarnumero(i,key)
		lmc.append(pal)
	for j in lmc:
		cmc=cmc+str(j)+" "
	return cmc

def descifrarnumero(m,k):
	lnc=[]
	ln=[]
	n,d=k
	cnc=""
	men=m.split(" ")
	for i in men:
		x=int(i)
		ln.append(x)
	for j in ln:
		m=(j**d)%n
		lnc.append(m)
	for k in lnc:
		l=buscarlet(k)
		cnc=cnc+str(l)
	return cnc

def buscarlet(x):
	alf="abcdefghijklmnñopqrstuvwxyz.@ABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890"
	c=0
	for i in alf:
		if x==c:
			return i
		else:
			c=c+1	
def index(request):
    doc_externo=open("plantilla\index.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def perfil(request):
    key_private=[143,113]
    descifrado=""
    descifradoE=""
    descifradoP=""
    clas=""
    name=request.session.get('name',"")
    print(str(name)+" largo: "+str(len(name)))
    email=request.session.get('email',"")
    passw=request.session.get('passw',"")
    clas=request.session.get('clas',"")
    
    if clas==None:
        clas=""
    print(clas)
    request.session['puntaje']="0"
    try:
        print("se intento")
        descifrado=descifrarmensaje(str(name),key_private)
        descifradoE=descifrarmensaje(str(email),key_private)
        descifradoP=descifrarmensaje(str(passw),key_private)
    except:
        descifrado=""
        descifradoE="?"
        descifradoP=""
    print(descifradoP)
    print(descifradoE)
    print(descifrado)
    doc_externo=open("plantilla\perfil.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context({"name":descifrado,"email":descifradoE,"pass":descifradoP, "clas":clas})
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
    key_public=[143,17]
    print("AAAAAA")
    username=""
    password=""

    username=request.GET["username"]
    password=request.GET["password"]
    cifrado=str(cifrarmensaje(username,key_public))
    cifrado=cifrado[0:(len(cifrado)-2)]
    cifradoA=str(cifrarmensaje(password,key_public))
    cifradoA=cifradoA[0:(len(cifradoA)-2)]
    print(cifrado)
    print(cifradoA)
    print()
    id_usu=""
    name=""
    clas=""
    passw=""
    email=""
    print(username, password)
    miconexion = mysql.connector.connect(user="b2b9d95a9c8f35",password="55f5f243",host="us-cdbr-east-04.cleardb.com",database="heroku_ebc478919d2c6e9")
    cursor = miconexion.cursor()
    q = "select * from usuarios where usu = '"+cifrado+"' and contraseña = '"+cifradoA+"'"
    cursor.execute(q)
    rs=cursor.fetchone()
    try:
        id_usu=rs[0]
        name=rs[1]
        email=rs[2]
        passw=rs[3]
        clas=rs[4]
        
    except:
        id_usu="0"
        name=""
        email=""
        passw=""
        clas=""
    request.session['id_usu']=id_usu
    request.session['name']=name
    request.session['email']=email
    request.session['clas']=clas
    request.session['passw']=passw
    request.session.modified = True

    print("session: id:"+str(request.session['id_usu']))
    miconexion.close()
    print(username, password,id_usu,clas,"\n")
    
    linkR="/perfil/"
    
    return redirect(linkR, permanent=True)
def crearCuenta(request):
    doc_externo=open("plantilla\crearCuenta.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def crearCuentaN(request):
    key_public=[143,17]
    username=request.GET["username"]
    password=request.GET["password"]
    email=request.GET["email"]
    cifrado=str(cifrarmensaje(username,key_public))
    cifrado=cifrado[0:(len(cifrado)-2)]
    cifradoE=str(cifrarmensaje(email,key_public))
    cifradoE=cifradoE[0:(len(cifradoE)-2)]
    cifradoA=str(cifrarmensaje(password,key_public))
    cifradoA=cifradoA[0:(len(cifradoA)-2)]
    print(username, password,email)
    miconexion = mysql.connector.connect(user="b2b9d95a9c8f35",password="55f5f243",host="us-cdbr-east-04.cleardb.com",database="heroku_ebc478919d2c6e9")
    cursor = miconexion.cursor()
    q = "INSERT INTO usuarios (usu,correo,contraseña,promedio) VALUES ('"+cifrado+"','"+cifradoE+"','"+cifradoA+"', '0')"
    cursor.execute(q)
    miconexion.commit()
    miconexion.close()
    return redirect("/iniciarCuenta", permanent=True)
def NSelector(request):
    request.session['puntaje']="0"
    doc_externo=open("plantilla/normal-select.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def WSelector(request):
    request.session['puntaje']="0"
    doc_externo=open("plantilla\words-select.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def JUGaR(request):
    request.session['puntaje']="0"
    doc_externo=open("plantilla\jugar.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def normal(request):
    request.session['puntaje']="0"
    doc_externo=open("plantilla/normal.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def words(request):
    request.session['puntaje']="0"
    doc_externo=open("plantilla\words.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context()
    documento=plt.render(ctx)
    return HttpResponse(documento)
def registrarPN(request,puntaje):
    miconexion = mysql.connector.connect(user="b2b9d95a9c8f35",password="55f5f243",host="us-cdbr-east-04.cleardb.com",database="heroku_ebc478919d2c6e9")
    cursor = miconexion.cursor()
    fecha=datetime.today().strftime('%Y-%m-%d %H:%M')
    link=""
    try:
        q = "SELECT * FROM usuarios where id_usu = '"+str(request.session.get('id_usu','0'))+"'"
        cursor.execute(q)
        rs=cursor.fetchone()
        promedio=int(rs[5])
        promedio=(promedio+int(puntaje))/2
        q = "INSERT INTO puntaje (puntaje,mododejuego,fecha,id_usu) VALUES ('"+puntaje+"','Normal','"+str(fecha)+"','"+str(request.session.get('id_usu','0'))+"')"
        cursor.execute(q)
        miconexion.commit()
        clasificacion="campeon"
        if(promedio<90):
            clasificacion="oro"
        if(promedio<60):
            clasificacion="plata"
        if(promedio<30):
            clasificacion="bronce"
        q = "UPDATE usuarios SET clasificacion = '"+clasificacion+"'  WHERE id_usu = '"+str(request.session.get('id_usu','0'))+"';"
        cursor.execute(q)
        miconexion.commit()
        q = "UPDATE usuarios SET promedio = '"+str(promedio)+"'  WHERE id_usu = '"+str(request.session.get('id_usu','0'))+"';"
        cursor.execute(q)
        miconexion.commit()
        
        request.session['clas']=str(clasificacion)
        request.session.modified = True
        link="/historial"
    except:
        print("Es invitado")
        link="/jugar"
    miconexion.close()
    return redirect(link, permanent=True)
def registrarPW(request,puntaje):
    miconexion = mysql.connector.connect(user="b2b9d95a9c8f35",password="55f5f243",host="us-cdbr-east-04.cleardb.com",database="heroku_ebc478919d2c6e9")
    cursor = miconexion.cursor()
    fecha=datetime.today().strftime('%Y-%m-%d %H:%M')
    link=""
    try:
        q = "SELECT * FROM usuarios where id_usu = '"+str(request.session.get('id_usu','0'))+"'"
        cursor.execute(q)
        rs=cursor.fetchone()
        promedio=int(rs[5])
        promedio=(promedio+int(puntaje))/2
        q = "INSERT INTO puntaje (puntaje,mododejuego,fecha,id_usu) VALUES ('"+puntaje+"','WORDS','"+str(fecha)+"','"+str(request.session.get('id_usu','0'))+"')"
        cursor.execute(q)
        miconexion.commit()
        clasificacion="campeon"
        if(promedio<90):
            clasificacion="oro"
        if(promedio<60):
            clasificacion="plata"
        if(promedio<30):
            clasificacion="bronce"
        q = "UPDATE usuarios SET clasificacion = '"+clasificacion+"'  WHERE id_usu = '"+str(request.session.get('id_usu','0'))+"';"
        cursor.execute(q)
        miconexion.commit()
        q = "UPDATE usuarios SET promedio = '"+str(promedio)+"'  WHERE id_usu = '"+str(request.session.get('id_usu','0'))+"';"
        cursor.execute(q)
        miconexion.commit()
        request.session['clas']=str(clasificacion)
        request.session.modified = True

        link="/historial"
    except:
        print("Es invitado")
        link="/jugar"
    miconexion.close()
    return redirect(link, permanent=True)
def modificarDatos(request):
    key_private=[143,113]
    descifrado=""
    descifradoE=""
    descifradoP=""
    name=request.session.get('name','')
    email=request.session.get('email','')
    passw=request.session.get('passw','')
    clas=request.session.get('clas','')
    descifrado=descifrarmensaje(str(name),key_private)
    descifrado=descifrado[0:(len(descifrado)-1)]
    descifradoE=descifrarmensaje(str(email),key_private)
    descifradoE=descifradoE[0:(len(descifradoE)-1)]
    descifradoP=descifrarmensaje(str(passw),key_private)
    descifradoP=descifradoP[0:(len(descifradoP)-1)]
    doc_externo=open("plantilla\modificarCuenta.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context({"name":descifrado,"email":descifradoE,"pass":descifradoP})
    documento=plt.render(ctx)
    return HttpResponse(documento)
def modificarCuenta(request):
    print(">:|")
    key_public=[143,17]
    username=request.GET["username"]
    password=request.GET["password"]
    email=request.GET["email"]
    idu=request.session["id_usu"]
    print("---2---")
    cifrado=str(cifrarmensaje(username,key_public))
    cifrado=cifrado[0:(len(cifrado)-2)]
    cifradoE=str(cifrarmensaje(email,key_public))
    cifradoE=cifradoE[0:(len(cifradoE)-2)]
    cifradoA=str(cifrarmensaje(password,key_public))
    cifradoA=cifradoA[0:(len(cifradoA)-2)]
    request.session['name']=cifrado
    request.session['email']=cifradoE
    request.session['passw']=cifradoA
    request.session.modified = True
    print(cifrado+"-", cifradoA,cifradoE)
    miconexion = mysql.connector.connect(user="b2b9d95a9c8f35",password="55f5f243",host="us-cdbr-east-04.cleardb.com",database="heroku_ebc478919d2c6e9")
    cursor = miconexion.cursor()
    q = "UPDATE usuarios SET usu = '"+cifrado+"' , contraseña = '"+cifradoA+"' , correo = '"+cifradoE+"'  WHERE id_usu = '"+str(idu)+"';"
    cursor.execute(q)
    miconexion.commit()
    miconexion.close()
    return redirect("/perfil", permanent=True)
def CerrarSesion(request):
    request.session.flush()
    request.session.modified = True
    print("cerrar sesion2")
    return redirect("/iniciarCuenta", permanent=True)
def Historial(request):
    miconexion = mysql.connector.connect(user="b2b9d95a9c8f35",password="55f5f243",host="us-cdbr-east-04.cleardb.com",database="heroku_ebc478919d2c6e9")
    cursor = miconexion.cursor()
    idu=request.session.get('id_usu',"0")
    q = "select * from puntaje where id_usu = '"+str(idu)+"' order by id_punt desc limit 4"
    cursor.execute(q)
    rs=cursor.fetchall()
    dato1="No haz jugado"
    dato2="No haz jugado"
    dato3="No haz jugado"
    dato4="No haz jugado"
    modo1="No haz jugado"
    modo2="No haz jugado"
    modo3="No haz jugado"
    modo4="No haz jugado"
    fecha1="No haz jugado"
    fecha2="No haz jugado"
    fecha3="No haz jugado"
    fecha4="No haz jugado"
    try:
        dato1=rs[0][1]
        modo1=rs[0][2]
        fecha1=rs[0][3]
        try:
            dato2=rs[1][1]
            modo2=rs[1][2]
            fecha2=rs[1][3]
            try:
                dato3=rs[2][1]
                modo3=rs[2][2]
                fecha3=rs[2][3]
                try:
                    dato4=rs[3][1]
                    modo4=rs[3][2]
                    fecha4=rs[3][3]
                except:
                    print("")
            except:
                print("")
        except:
            print("")
    except:
        print("")
    miconexion.close()
    doc_externo=open("plantilla\historial.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context({"dato1":dato1,"dato2":dato2,"dato3":dato3,"dato4":dato4,"modo1":modo1,"modo2":modo2,"modo3":modo3,"modo4":modo4,"fecha1":fecha1,"fecha2":fecha2,"fecha3":fecha3,"fecha4":fecha4,})
    documento=plt.render(ctx)
    return HttpResponse(documento)

def configurar(request):
    letrasGuardadas = ""
    estado = ""
    
    PINKY_TIP_LEFT = ["|","1","Tab","q","CapsLock","a","Shift","<","z","Control","Meta"]
    RING_FINGER_TIP_LEFT = ["2","w","s","x","Alt"]
    MIDDLE_FINGER_TIP_LEFT = ["3","e","d","c"]
    INDEX_FINGER_TIP_LEFT = ["4","5","r","t","f","g","v","b"]
    THUMB_TIP_LEFT = [" "]

    PINKY_TIP_RIGHT = ["Backspace","¿","'","0","Enter","+","Dead","p","}","{","ñ","Shift","-","Control","ContextMenu"]
    RING_FINGER_TIP_RIGHT= ["0","o","l","."]
    MIDDLE_FINGER_TIP_RIGHT= ["8","i","k",",","AltGraph"]
    INDEX_FINGER_TIP_RIGHT= ["6","7","y","u","h","j","n","m"]
    THUMB_TIP_RIGHT= [" "]

    teclas = ["|","1","Tab","q","CapsLock","a","Shift","<","z","Control","Meta","2","w","s","x","Alt","3","e","d","c","4","5","r","t","f","g","v","b","Backspace","¿","'","0","Enter","+","Dead","p","}","{","ñ","Shift","-","Control","ContextMenu","0","o","l",".","8","i","k",",","AltGraph","6","7","y","u","h","j","n","m"]

    def redondear (x,y,z):
        print(x)
        print(y)
        return str(x-0.1225*-z)+","+str(x+0.1225*-z)+","+str(y-0.1225*-z)+","+str(y+0.1225*-z)

    mp_hands = mp.solutions.hands
    imagen = request.POST.get("imagen")
    letra = request.POST.get("letra")

    if imagen == None:
        print("No hay imagen")
        estado = "no se recupero ninguna imagen"
    else:
        print(letra)
        imagen = imagen.replace("data:image/png;base64,","")
        b = bytes(imagen,'utf-8')
        image_64_decode = base64.decodebytes(b) 
        nparr = np.fromstring(image_64_decode, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        with mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.5) as hands:
        
            height, width, _ = img_np.shape
            img = cv2.flip(img_np, 1)

            # Convert the BGR image to RGB before processing.
            results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            if results.multi_hand_landmarks is not None:
                try:
                    coordsx = []
                    coordsy = []
                    coordsz = []
                    if letra in PINKY_TIP_LEFT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].z)
                        coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in RING_FINGER_TIP_LEFT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].z)
                        coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in MIDDLE_FINGER_TIP_LEFT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z)
                        coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in INDEX_FINGER_TIP_LEFT:
                        print("soy el dedo index left")
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z)
                        coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in THUMB_TIP_LEFT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].z)
                        coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in PINKY_TIP_RIGHT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].z)
                        if len(coordsx) == 2:
                            coords = redondear(coordsx[1],coordsy[1],coordsz[1])
                        else:
                            coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in RING_FINGER_TIP_RIGHT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].z)
                        if len(coordsx) == 2:
                            coords = redondear(coordsx[1],coordsy[1],coordsz[1])
                        else:
                            coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in MIDDLE_FINGER_TIP_RIGHT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z)
                        if len(coordsx) == 2:
                            coords = redondear(coordsx[1],coordsy[1],coordsz[1])
                        else:
                            coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in INDEX_FINGER_TIP_RIGHT:
                        print("soy el dedo index right")
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z)
                        if len(coordsx) == 2:
                            coords = redondear(coordsx[1],coordsy[1],coordsz[1])
                        else:
                            coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    elif letra in THUMB_TIP_RIGHT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
                            coordsz.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].z)
                        if len(coordsx) == 2:
                            coords = redondear(coordsx[1],coordsy[1],coordsz[1])
                        else:
                            coords = redondear(coordsx[0],coordsy[0],coordsz[0])
                        print(coords)
                    request.session[letra] = coords
                    estado = "tecla guardada con exito"
                except Exception as e:
                    print(e," Algo paso pero si se detecto la mano")
                    estado = "ocurrio un error :("
            else:
                print("No se detecto tu manos uwuwnt")
                estado = "No se detecta la mano"

    for i in teclas:
        if i in request.session:
            letrasGuardadas += i+","
    
    print("letras guardadas: ",letrasGuardadas," :letrasGuradadas")

    if request.is_ajax and request.method == "POST":
        
        print("entre al ajx")
        return JsonResponse({"msg": letrasGuardadas,"estado": estado})
    
    doc_externo=open("plantilla\configurar.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context({})
    documento=plt.render(ctx)
    return HttpResponse(documento)


@csrf_exempt
def jugarNormal(request):

    PINKY_TIP_LEFT = ["|","1","Tab","q","CapsLock","a","Shift","<","z","Control","Meta"]
    RING_FINGER_TIP_LEFT = ["2","w","s","x","Alt"]
    MIDDLE_FINGER_TIP_LEFT = ["3","e","d","c"]
    INDEX_FINGER_TIP_LEFT = ["4","5","r","t","f","g","v","b"]
    THUMB_TIP_LEFT = [" "]

    PINKY_TIP_RIGHT = ["Backspace","¿","'","0","Enter","+","Dead","p","}","{","ñ","Shift","-","Control","ContextMenu"]
    RING_FINGER_TIP_RIGHT= ["0","o","l","."]
    MIDDLE_FINGER_TIP_RIGHT= ["8","i","k",",","AltGraph"]
    INDEX_FINGER_TIP_RIGHT= ["6","7","y","u","h","j","n","m"]
    THUMB_TIP_RIGHT= [" "]

    mp_hands = mp.solutions.hands
    imagen = request.POST.get("imagen")
    letra = request.POST.get("letra")
    errores = 0

    def comprobar(x,y):
        rango = request.session[letra].split(sep=",")
        print(rango,"es el rango")
        print(x)
        print(y)
        if x >= float(rango[0]) and x <= float(rango[1]) and y >= float(rango[2]) and y <= float(rango[3]):
            print("tecleaste bien B)")
            return 0
        else: return 1

    if imagen == None:
        print("No hay imagen")
        estado = "no se recupero ninguna imagen"
    else:
        print(letra, "en el juego")
        imagen = imagen.replace("data:image/png;base64,","")
        b = bytes(imagen,'utf-8')
        image_64_decode = base64.decodebytes(b) 
        nparr = np.fromstring(image_64_decode, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        with mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.5) as hands:
        
            height, width, _ = img_np.shape
            img = cv2.flip(img_np, 1)

            # Convert the BGR image to RGB before processing.
            results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            if results.multi_hand_landmarks is not None:
                try:
                    coordsx = []
                    coordsy = []

                    if letra in PINKY_TIP_LEFT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y)
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in RING_FINGER_TIP_LEFT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y)
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in MIDDLE_FINGER_TIP_LEFT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in INDEX_FINGER_TIP_LEFT:
                        print("soy el dedo index left")
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in THUMB_TIP_LEFT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in PINKY_TIP_RIGHT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y)
                        if len(coordsx) == 2:
                            errores = comprobar(coordsx[1],coordsy[1])
                        else:
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in RING_FINGER_TIP_RIGHT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y)
                        if len(coordsx) == 2:
                            errores = comprobar(coordsx[1],coordsy[1])
                        else:
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in MIDDLE_FINGER_TIP_RIGHT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)
                        if len(coordsx) == 2:
                            errores = comprobar(coordsx[1],coordsy[1])
                        else:
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in INDEX_FINGER_TIP_RIGHT:
                        print("soy el dedo index right")
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
                        if len(coordsx) == 2:
                            errores = comprobar(coordsx[1],coordsy[1])
                        else:
                            errores = comprobar(coordsx[0],coordsy[0])
                    elif letra in THUMB_TIP_RIGHT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            coordsx.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x)
                            coordsy.append(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
                        if len(coordsx) == 2:
                            errores = comprobar(coordsx[1],coordsy[1])
                        else:
                            errores = comprobar(coordsx[0],coordsy[0])
                    estado = "si se detecto la mano"
                except Exception as e:
                    print(e," Algo paso pero si se detecto la mano")
                    estado = "ocurrio un error :("
            else:
                print("No se detecto tu manos uwuwnt")
                estado = "No se detecta la mano"

    if request.is_ajax and request.method == "POST":
        
        print("entre al ajx")
        print(errores," es el error")
        return JsonResponse({"errores": errores ,"estado": estado})

    doc_externo=open("plantilla/normal-cam.html")
    plt=Template(doc_externo.read())
    doc_externo.close()
    ctx=Context({})
    documento=plt.render(ctx)
    return HttpResponse(documento)
