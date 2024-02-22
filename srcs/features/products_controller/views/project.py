from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from features.products_controller.serializers.project import ProjectSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"

    model = Project
    template_name = "products_controller/projects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["product_list"] = BaseProduct.objects.all().filter(project__name=self.object.name)
        except Project.DoesNotExist:
            ...
        return context


# https://blog.logrocket.com/django-rest-framework-create-api/
# https://github.com/denisorehovsky/django-rest-polymorphic


class ProjectListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all the todo items for given requested user
        """
        todos = Project.objects.filter(owner=request.user.id)
        serializer = ProjectSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the Project with given todo data
        """
        data = {"task": request.data.get("task"), "completed": request.data.get("completed"), "user": request.user.id}
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user_id):
        """
        Helper method to get the object with given pk, and user_id
        """
        try:
            return Project.objects.get(id=pk, owner=user_id)
        except Project.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieves the Project with given pk
        """
        todo_instance = self.get_object(pk, request.user.id)
        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        Updates the todo item with given pk if exists
        """
        todo_instance = self.get_object(pk, request.user.id)
        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        data = {"task": request.data.get("task"), "completed": request.data.get("completed"), "user": request.user.id}
        serializer = ProjectSerializer(instance=todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Deletes the todo item with given pk if exists
        """
        todo_instance = self.get_object(pk, request.user.id)
        if not todo_instance:
            return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        todo_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
