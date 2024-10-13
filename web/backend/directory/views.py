from django.shortcuts import render
import os
from django.http import JsonResponse

# Retrieve the list of files in the directory
from rest_framework.decorators import APIView

from directory.serializers import FileSerializer

def list_files(directory_path):
    files = os.listdir(directory_path)
    file_list = []

    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            file_list.append({
                'name': file,
                'path': file_path
            })
        elif os.path.isdir(file_path):
            file_list.extend(list_files(file_path))
    
    return file_list

class ListFilesView(APIView):

    def get(self, request, format=None):
        # print(f'Request: {request.headers}')
        directory = request.query_params.get('directory', None)

        if directory is None:
            return JsonResponse({'error': 'No directory provided'}, status=400)
        
        directory_path = os.path.join(os.getcwd(), directory)

        try:
            file_list = list_files(directory_path)
            serialized_files = FileSerializer(file_list, many=True).data

            json = JsonResponse({'files': serialized_files})
            json['Access-Control-Allow-Origin'] = '*'
            return json
        except FileNotFoundError:
            return JsonResponse({'error': 'Directory not found'}, status=404)

