# plots/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Plot,CustomUser

User = get_user_model()



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Assuming your model is named CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'nid_number', 'meta_mask_id']



class PlotSerializer(serializers.ModelSerializer):
    # Define a new field 'owner_email' for input
    owner_email = serializers.EmailField(write_only=True,required=False)

    class Meta:
        model = Plot
        fields = ['id', 'owner', 'plot_number', 'area', 'price', 'owner_email']
        read_only_fields = ['owner']  # 'owner' is read-only, it will be set by the view
    

class PlotOwnershipTransferSerializer(serializers.Serializer):
    existing_owner_email = serializers.EmailField()
    new_owner_email = serializers.EmailField()

    def validate(self, data):
        existing_owner_email = data.get('existing_owner_email', None)
        new_owner_email = data.get('new_owner_email', None)

        if existing_owner_email is None or new_owner_email is None:
            raise serializers.ValidationError('Please provide both existing and new owner emails.')

        return data

