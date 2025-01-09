from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
	
from firebase_admin import db

class LandingAPI(APIView):
	    
    name = 'Landing API'

    # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'cotizaciones'

    def get(self, request):

         # Referencia a la colección
         ref = db.reference(f'{self.collection_name}')
		    
         # get: Obtiene todos los elementos de la colección
         data = ref.get()

         # Devuelve un arreglo JSON
         return Response(data, status=status.HTTP_200_OK)
    def post(self, request):
	        
         # Referencia a la colección
         ref = db.reference(f'{self.collection_name}')
	        
         # push: Guarda el objeto en la colección
         new_resource = ref.push(request.data)
	        
         # Devuelve el id del objeto guardado
         return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED) 
