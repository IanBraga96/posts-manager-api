from django.shortcuts import render

# Create your views here.
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import PostLike
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer, PostLikeSerializer, PostCommentSerializer
from .models import PostComment
from .utils import extract_mentions

BASE_URL = "https://dev.codeleap.co.uk/careers/"

class PostListCreateAPIView(APIView):
    def get(self, request):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                data = response.json()
                
                serializer = PostSerializer(
                    data['results'], 
                    many=True, 
                    context={'request': request}
                )
                
                return Response({
                    'results': serializer.data
                }, status=status.HTTP_200_OK)
                
            return Response(
                {"detail": "Failed to fetch posts from external API"},
                status=response.status_code,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                response = requests.post(BASE_URL, json=serializer.validated_data)
                if response.status_code in [201, 200]:
                    return Response(response.json(), status=response.status_code)
                return Response(
                    {"detail": "Failed to create post on external API"},
                    status=response.status_code,
                )
            except Exception as e:
                return Response(
                    {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    def get_url(self, pk):
        return f"{BASE_URL}{pk}/"

    def get(self, request, pk):
        try:
            response = requests.get(self.get_url(pk))
            if response.status_code == 200:
                serializer = PostSerializer(
                    response.json(),
                    context={'request': request}
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            return Response(
                {"detail": "Post not found or error fetching from external API"},
                status=response.status_code,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        serializer = PostUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                response = requests.patch(
                    self.get_url(pk), json=serializer.validated_data
                )
                if response.status_code in [200, 204]:
                    return Response(
                        response.json() if response.content else {},
                        status=response.status_code,
                    )
                return Response(
                    {"detail": "Failed to update post on external API"},
                    status=response.status_code,
                )
            except Exception as e:
                return Response(
                    {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            response = requests.delete(self.get_url(pk))
            if response.status_code in [200, 204]:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"detail": "Failed to delete post on external API"},
                status=response.status_code,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostLikeAPIView(APIView):
    def post(self, request, pk):
        try:
            username = request.data.get('username')
            if not username:
                return Response(
                    {'detail': 'Username is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            like, created = PostLike.objects.get_or_create(
                post_id=pk,
                username=username
            )

            if not created:
                like.delete()
                return Response(
                    {'detail': 'Like removed'},
                    status=status.HTTP_200_OK
                )

            serializer = PostLikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostCommentAPIView(APIView):
    def get(self, request, pk):
        try:
            comments = PostComment.objects.filter(post_id=pk)
            serializer = PostCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, pk):
        try:
            username = request.data.get('username')
            content = request.data.get('content')
            
            if not username or not content:
                return Response(
                    {'detail': 'Username and content are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            mentioned_users = extract_mentions(content)

            comment = PostComment.objects.create(
                post_id=pk,
                username=username,
                content=content,
                mentioned_users=mentioned_users
            )

            serializer = PostCommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            comment_id = request.data.get('comment_id')
            username = request.data.get('username')
            content = request.data.get('content')
            
            if not comment_id or not username or not content:
                return Response(
                    {'detail': 'Comment ID, username and content are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                comment = PostComment.objects.get(id=comment_id, post_id=pk)
            except PostComment.DoesNotExist:
                return Response(
                    {'detail': 'Comment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if comment.username != username:
                return Response(
                    {'detail': 'You can only edit your own comments'},
                    status=status.HTTP_403_FORBIDDEN
                )

            mentioned_users = extract_mentions(content)
            
            comment.content = content
            comment.mentioned_users = mentioned_users
            comment.save()

            serializer = PostCommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def delete(self, request, pk):
        try:
            comment_id = request.data.get('comment_id')
            username = request.data.get('username')
            
            if not comment_id or not username:
                return Response(
                    {'detail': 'Comment ID and username are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                comment = PostComment.objects.get(id=comment_id, post_id=pk)
            except PostComment.DoesNotExist:
                return Response(
                    {'detail': 'Comment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if comment.username != username:
                return Response(
                    {'detail': 'You can only delete your own comments'},
                    status=status.HTTP_403_FORBIDDEN
                )

            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
