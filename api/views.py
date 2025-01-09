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



class LandingAPIDetail(APIView):

     name = 'Landing Detail API'

     collection_name = 'cotizaciones'
     
     def get(self, request, pk):
        
        ref = db.reference(f'{self.collection_name}/{pk}')

        data = ref.get()

        if data:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Documento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

     def put(self, request, pk):
         # Validar que request.data contenga los campos necesarios
        required_fields = ["correo", "modelo", "nombre"]
        missing_fields = [field for field in required_fields if field not in request.data]
            
        if missing_fields:
            return Response(
                {'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Referencia al documento específico
        ref = db.reference(f'{self.collection_name}/{pk}')

        # Verificar si el documento existe
        existing_data = ref.get()
        if not existing_data:
            return Response(
                {'error': 'Documento no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Actualizar el documento
        ref.update(request.data)

        return Response(
            {'message': 'Documento actualizado correctamente'},
            status=status.HTTP_200_OK
        )

     def delete(self, request, pk):
         # Referencia al documento específico
        ref = db.reference(f'{self.collection_name}/{pk}')
            
        # Verificar si el documento existe
        existing_data = ref.get()
        if not existing_data:
            return Response(
                {'error': 'Documento no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Eliminar el documento
        ref.delete()

        return Response(
            {'message': 'Documento eliminado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )
