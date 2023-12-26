from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, Plot
from .serializers import CustomUserSerializer, PlotSerializer,PlotOwnershipTransferSerializer
from .ethereum_contract import EthereumContractConnector

class CustomUserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class PlotListView(generics.ListCreateAPIView):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer
    
    def perform_create(self, serializer):
        # Retrieve the owner using the provided email
        owner_email = self.request.data.get('owner_email')
        try:
            owner = CustomUser.objects.get(email=owner_email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"No user with email '{owner_email}' found.")

        # Set the owner and create the plot
        serializer.save(owner=owner)

class PlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer


class TransferPlotOwnershipView(generics.UpdateAPIView):
    queryset = Plot.objects.all()
    serializer_class = PlotOwnershipTransferSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the provided existing_owner_email matches the current owner's email
        existing_owner_email = self.request.data.get('existing_owner_email')
        if existing_owner_email != instance.owner.email:
            return Response({'error': 'You do not have permission to transfer ownership of this plot.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the new owner's email from the validated data
        new_owner_email = serializer.validated_data['new_owner_email']

        try:
            # Get the new owner instance
            new_owner = CustomUser.objects.get(email=new_owner_email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'The specified new owner does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Perform the transfer by updating the owner field
        instance.owner = new_owner
        instance.save()

        return Response({'message': f'Ownership of Plot {instance.plot_number} transferred to {new_owner.email}.'}, status=status.HTTP_200_OK)
