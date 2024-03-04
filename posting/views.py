from rest_framework.views import APIView
from .models import Posting
from .serializers import PostingSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsPostingOwner
from rest_framework.permissions import IsAuthenticated


class ListPostings(APIView):
    serializer_class = PostingSerializer

    def get(self, request, *args, **kwargs):
        postings = Posting.objects.all()
        serializer = PostingSerializer(postings, many=True)
        return Response(serializer.data)


class CreatePostings(APIView):
    serializer_class = PostingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPostingOwner]

    def post(self, request, *args, **kwargs):
        # Check if the employer_id from the endpoint matches with the one from the request
        if int(request.data['employer_id']) != kwargs.get('employer_id'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        posting = PostingSerializer(data=request.data)
        # Check permission
        self.check_object_permissions(request, posting)
        # Create posting
        if posting.is_valid():
            posting.save()
            return Response(posting.data)
        else:
            return Response(posting.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeletePostings(APIView):
    serializer_class = PostingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPostingOwner]

    def put(self, request, *args, **kwargs):
        # Check if the posting that needs to be updated exists
        employer_id = kwargs.get('employer_id')
        posting_id = kwargs.get('posting_id')
        try:
            posting = (Posting.objects
                       .filter(employer_id=employer_id)
                       .get(posting_id=posting_id))
            # Check if the employer_id from the endpoint matches with the one from the request and the posting that
            # will be updated
            if int(request.data['employer_id']) != employer_id:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # Check permission
            self.check_object_permissions(request, posting)
            # Update the posting
            updated_posting = PostingSerializer(posting, data=request.data)
            if updated_posting.is_valid():
                updated_posting.save()
                return Response(updated_posting.data)
            else:
                return Response(updated_posting.errors, status=status.HTTP_400_BAD_REQUEST)
        except Posting.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Check if the posting that will be deleted exists
        try:
            posting = (Posting.objects
                       .filter(employer_id=kwargs.get('employer_id'))
                       .get(posting_id=kwargs.get('posting_id')))
            # Check permissions
            self.check_object_permissions(request, posting)
            # Delete posting
            posting.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Posting.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
