from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, Plot
from .serializers import CustomUserSerializer, PlotSerializer,PlotOwnershipTransferSerializer
from .ethereum_contract import EthereumContractConnector

class CustomUserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        nid_number = self.request.data.get('nid_number')
        meta_mask_id = self.request.data.get('meta_mask_id')

        ethereum_connector = EthereumContractConnector()

        try:
            ethereum_connector.add_owner(email, nid_number, meta_mask_id)
            serializer.save()
            return Response({'message': 'User added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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

        # Call Ethereum client to add the plot on the blockchain
        self.ethereum_client.add_plot(plot_instance.plot_number, plot_instance.price, owner.meta_mask_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

        

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
            # Get the owner instances
            existing_owner = CustomUser.objects.get(email=existing_owner_email)
            new_owner = CustomUser.objects.get(email=new_owner_email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'The specified new owner does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Query metamask ids based on email addresses
        existing_owner_metamask_id = existing_owner.meta_mask_id
        new_owner_metamask_id = new_owner.meta_mask_id

        # Perform the transfer by updating the owner field
        instance.owner = new_owner
        instance.save()
        
        # Call the Ethereum smart contract to transfer plot ownership
        ethereum_connector = EthereumContractConnector()
        ethereum_connector.transfer_plot_ownership(instance.plot_number, existing_owner_metamask_id, new_owner_metamask_id)


        return Response({'message': f'Ownership of Plot {instance.plot_number} transferred to {new_owner.email}.'}, status=status.HTTP_200_OK)
