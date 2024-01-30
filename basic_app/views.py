from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Todo
from .serializers import TodoSerializer

@api_view(['GET', 'POST'])
def todos_ops(request):
    method = request.method
    if method == "GET":
        todos = Todo.objects.all()
        todo_ser = TodoSerializer(todos, many=True)
        serialized_data = todo_ser.data
        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK
        )
    elif method == "POST":
        data = request.data
        todo_ser = TodoSerializer(data=data)
        if todo_ser.is_valid():
            todo_ser.save()
            return Response(data={"message": "inserted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(todo_ser.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT', 'DELETE'])
def put_todos(request, id):
    method = request.method
    todo = Todo.objects.get(id=id)
    if method == "PUT":
        data = request.data
        todo_ser = TodoSerializer(todo, data=data)
        if todo_ser.is_valid():
            todo_ser.save()
            return Response(data=todo_ser.data, status=status.HTTP_200_OK)
        else:
            return Response(todo_ser.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        todo.delete()
        return Response(data={"message": "deleted successfully"}, status=status.HTTP_200_OK)