from rest_framework import serializers
from task.models import User, Expense, ExpenseSplit
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number', "password"]
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        # If password is being updated, hash it
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'split_method', 'created_at']

class ExpenseSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSplit
        fields = ['expense', 'user', 'amount_owed', 'percentage_owed']