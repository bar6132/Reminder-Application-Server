from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from .serializers import NotesSerializer

@csrf_exempt
@api_view(['GET', 'POST'])
def note_list(request, pk=None):
    if pk is None:
        if request.method == 'GET':
            try:
                all_notes = Note.objects.all()
                serializer = NotesSerializer(all_notes, many=True).data
                response_data = {
                    'message': 'Notes retrieved successfully',
                    'data': serializer
                }
                print(serializer)
                return Response(response_data, status=status.HTTP_200_OK)
            except Note.DoesNotExist:
                error_data = {
                    'message': 'Notes not found'
                }
                return Response(error_data, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'POST':
            serializer = NotesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE','PATCH'])
def note_detail(request, pk):
    if request.method == 'GET':
        try:
            note = Note.objects.get(pk=pk)
            serializer = NotesSerializer(note)
            print(serializer.data)
            return Response(serializer.data)
        except Note.DoesNotExist:
            error_data = {
                'message': 'Note not found'
            }
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NotesSerializer(note, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        if pk is not None:
            try:
                note = Note.objects.get(pk=pk)
                note.status = 'completed'
                note.save()
                serializer = NotesSerializer(note)
                return Response(serializer.data)
            except Note.DoesNotExist:
                return Response({'error': 'Message not found.'}, status=404)
        else:
            return Response({'error': 'Message ID (pk) is required for marking as completed.'}, status=400)

    elif request.method == 'DELETE':
        try:
            note = Note.objects.get(pk=pk)
            print(note)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


