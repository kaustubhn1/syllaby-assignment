import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated

from book.models import Book
from user.models import Profile
from .models import BookCollaboratorMapper


logger = logging.getLogger(__name__)


class BookCollaboratorView(APIView):
    """
    View for book-collaborator related CRUD operations
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Grant collaborator access to a user for a book
        """
        payload = request.data
        collaborator_profile_id = payload['profile_id']
        book_id = payload['book_id']

        book = None
        profile = None

        try:
            book = Book.objects.get(id=book_id)

            # Only book author is authorized to grant collaboration access
            if book.author.id != request.user.profile.id:
                return Response({"message": "Only the book's author can grant collaborator access to the book."}, status=HTTP_401_UNAUTHORIZED)
            
            if book.author.id == collaborator_profile_id:
                return Response({"message": "Book author cannot have collaborator role!"}, status=HTTP_400_BAD_REQUEST)
            
        except Book.DoesNotExist:
            return Response({"message": "The book does not exist"}, status=HTTP_404_NOT_FOUND)
    
        try:
            profile = Profile.objects.get(id=collaborator_profile_id)
        except Profile.DoesNotExist:
            return Response({"message": "The profile does not exist"}, status=HTTP_404_NOT_FOUND)
        
        try:
            if not BookCollaboratorMapper.objects.filter(collaborator=profile, book=book, access_revoked=False).exists():
                BookCollaboratorMapper.objects.create(collaborator=profile, book=book)
                return Response({"message": "User granted access as a collaborator"}, status=HTTP_201_CREATED)
            else:
                return Response({"message": "User already a collaborator for the book!"}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return Response({"message": "Server error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id):
        """
        Revoke collaborator access to a user for a book
        """
        try:
            book_collaborator_mapping = BookCollaboratorMapper.objects.get(id=id)
            book_collaborator_mapping.access_revoked = True
            book_collaborator_mapping.save()

            return Response({"message": "Collaborator access revoked"}, status=HTTP_204_NO_CONTENT)
        except BookCollaboratorMapper.DoesNotExist:
            return Response({"message": "Collaborator access record not found"}, status=HTTP_404_NOT_FOUND)
