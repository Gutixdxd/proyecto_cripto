from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, New_Doc_Form
from .models import User, Document
from rsa import newkeys, sign, verify

def newUser(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
                #Genera Llaves
            public_key, private_key = newkeys(1024)
            #Recupera usuario
            user = request.user
            #Asigna clave publica al usuario
            user.key = public_key
            #Retorna al usuario la clave privada para que 
            #la guarde y no se guarda en el sistema
            return render(request, 'template', {'private_key': private_key})
        else:
            form = RegistrationForm()
            return redirect("/")
    else:
        return redirect("/")

def login_request(request):
    """
    login_request maneja el inicio de sesión del usuario,
    verifica que el método sea post, luego tomando los datos del
    formulario busca al usuario en la base de datos,
    si existe entonces inicia sesión y redirecciona a "/",
    de otra forma arroja error en el formulario.
    """ 
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_request(request):
    """
    logout_request cierra la sesión del usuario
    y luego redirecciona a "/".
    """ 
    logout(request)
    return redirect("/")

def newFirma(request, PK, document_id):
    #Check user login
    if request.user.is_authenticated:
        if request.method == "POST":
            document = get_object_or_404(Document, id=document_id)
            text = document.text
            message = text.encode()
            try:
                #Puede pasar que se firma un documento con una clave incorrecta,
                #Y en teoria pasa por esta verificacion, no se si es correcto
                cripticSign = sign(message, PK, "SHA-1")
                document.sign = cripticSign
                document.save()
                return 
            except:
                return #Private Key invalida
            

    #Actualiza pagina con documento firmado
    return redirect("/")


def checkDoc(request, user_id, doc_id):
    user = get_object_or_404(User, id=user_id)
    doc = get_object_or_404(Document, id= doc_id)
    message = doc.text
    key = user.key
    sign = doc.sign
    #Desencripta la firma de un documento
    try:
        verify(message.encode(), sign, key)
        #Si la firma desencriptada corresponde, no tira error
        return True
    except:
        return False #firma invalida
    
def requestSign(request, user_id, doc_id):
    return #notifica al usuario que debe firmar cierto documento

def newDoc(request, text):
    #Usa un formulario para obtener texto
    doc = New_Doc_Form(request.post)
    doc.user = request.user
    doc.save()
    return #Ok