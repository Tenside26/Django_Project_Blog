
from Blog_App.models import PostsModel, CommentsModel
from .serializers import PostsModelSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response


@csrf_exempt
@api_view(['GET', 'POST'])
def api_posts_list_view(request):

    if request.method == 'GET':
        posts = PostsModel.objects.all()
        serializer = PostsModelSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostsModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def api_post_detail_view(request, pk):

    try:
        post = PostsModel.objects.get(pk=pk)
    except PostsModel.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostsModelSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostsModelSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)
