from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import User, Document
from rsa import newkeys, encrypt, decrypt

def newUser(request):
    #Genera Llaves
    public_key, private_key = newkeys(1024)
    #Recupera usuario
    user = request.user
    #Asigna clave publica al usuario
    user.key = public_key
    #Retorna al usuario la clave privada para que 
    #la guarde y no se guarda en el sistema
    return private_key

def newFirma(request, PK, document_id):
    #Check user login

    document = get_object_or_404(Document, id=document_id)
    user = request.user
    sign = user.username
    cripticSign = encrypt(sign, PK)
    document.sign = cripticSign
    #Falta validar que la clave publica lo desencripta

    #Actualiza pagina con documento firmado
    return render()


def checkDoc(request, user_id, doc_id):
    user = get_object_or_404(User, id=user_id)
    doc = get_object_or_404(Document, id= doc_id)

    key = user.key
    sign = doc.sign
    #Desencripta la firma de un documento
    result = decrypt(sign, key)
    #Si la firma desencriptada corresponde esta bien
    if (result == user.username):
        return True
    else:
        return False
    
def requestSign(request, user_id, doc_id):
    return #notifica al usuario que debe firmar cierto documento

def newDoc(request, text):
    #Usa un formulario para obtener texto
    doc = NewDocForm(request.post)
    doc.user = request.user
    doc.save()
    return #Ok