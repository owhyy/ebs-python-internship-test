from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_util.decorators import serialize_decorator

from apps.blog.models import Category, Blog, Comment
from apps.blog.serializers import CategorySerializer, BlogSerializer, CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BlogListView(GenericAPIView):
    serializer_class = BlogSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        blogs = Blog.objects.all()

        return Response(BlogSerializer(blogs, many=True).data)


class BlogItemView(GenericAPIView):
    serializer_class = BlogSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, pk):
        blog = get_object_or_404(Blog.objects.filter(pk=pk))

        return Response(BlogSerializer(blog).data)


class CreateBlogView(GenericAPIView):
    serializer_class = BlogSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(BlogSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        blog = Blog.objects.create(
            title=validated_data['title'],
            slug=validated_data['slug'],
            enabled=validated_data['enabled'],
            body=validated_data['body'],
            category=validated_data['category'],
        )
        blog.save()

        return Response(BlogSerializer(blog).data)


class CreateCommentView(GenericAPIView):
    serializer_class = CommentSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(CommentSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        comment = Comment.objects.create(
            blog=validated_data['blog'],
            text=validated_data['text'],
        )
        comment.save()

        return Response(CommentSerializer(comment).data)
