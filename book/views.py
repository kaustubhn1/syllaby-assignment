import logging

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated

from common.models import BookCollaboratorMapper
from .models import Book
from .serializers import BookSerializer


logger = logging.getLogger(__name__)


class BookView(APIView):
    """
    View for book related CRUD operations
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        """
        Return all books or get book by Id.
        """
        if not id:
            books = Book.objects.all()
            books_serialized = BookSerializer(books, many=True).data
            return Response(books_serialized, status=HTTP_200_OK)
        else:
            book = get_object_or_404(Book, id=id)
            book_serialized = BookSerializer(book).data
            return Response(book_serialized, status=HTTP_200_OK)
    
    def post(self, request):
        """
        Create a book record
        """

        payload = request.data

        user_profile = request.user.profile
        payload['author'] = user_profile.id

        book_serializer = BookSerializer(data=payload)

        if book_serializer.is_valid():
           book_serializer.save()
           return Response(book_serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(book_serializer.errors, status=HTTP_400_BAD_REQUEST)
        
    def put(self, request, id):
        """
        Update a book record
        """

        payload = request.data

        user_profile = request.user.profile
        payload['author'] = user_profile.id

        try:
            book = Book.objects.get(id=id)

            # Only allow book name updation if the requesting user is the author
            if payload['book_name'] != book.book_name and user_profile.id != book.author.id:
                return Response({"message": "Unauthorized request. Only author can edit the book name."}, status=HTTP_401_UNAUTHORIZED)
            
            # Check collaborator access
            if user_profile.id != book.author.id and not BookCollaboratorMapper.objects.filter(collaborator__id=user_profile.id, book=book, access_revoked=False).exists():
                return Response({"message": "Unauthorized request. User not granted collaborator access to this book!"}, status=HTTP_401_UNAUTHORIZED)
            
            book_serializer = BookSerializer(book, data=payload)

            if book_serializer.is_valid():
                book_serializer.save()
                return Response(book_serializer.data, status=HTTP_200_OK)
            else:
                return Response(book_serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(str(e))
            return Response({}, status=HTTP_500_INTERNAL_SERVER_ERROR)
