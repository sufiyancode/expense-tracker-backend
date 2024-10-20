from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from task.models import User, Expense, ExpenseSplit
from task.serializers import UserSerializer, ExpenseSerializer, ExpenseSplitSerializer

# Register view
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Get the user data for profile view for the respective user
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user 
        serializer = UserSerializer(user) 
        return Response(serializer.data)  


# Create the Expense and Split it according to split method
class AddExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        description = request.data.get("description")
        split_method = request.data.get("split_method") # Exact, equal, percentage
        participants = request.data.get("participants") # Array of Participants
        splits = request.data.get("splits", None)

        # Validate the fields
        if not amount or not description or not split_method or not participants:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            expense = Expense.objects.create(
                amount=amount,
                description=description,
                split_method=split_method
            )

            # Add participants to the expense
            expense.participants.add(*participants)

            # Handle 'exact' and 'percentage' splits
            if split_method in ['exact', 'percentage']:
                if not splits:
                    return Response({"error": "Splits are required for exact/percentage split."}, status=status.HTTP_400_BAD_REQUEST)

                # Clear existing splits if they exist 
                ExpenseSplit.objects.filter(expense=expense).delete()

                for split in splits:
                    ExpenseSplit.objects.create(
                        expense=expense,
                        user_id=split['user'],
                        amount_owed=split.get('amount_owed', 0),
                        percentage_owed=split.get('percentage_owed', 0)
                    )

            return Response({"message": "Expense created successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# To list all the expenses by respective user

class UserExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error":"User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        expenses = Expense.objects.filter(participants__id = user_id)
        expense_data = [{"id": expense.id, "amount": expense.amount, "description": expense.description, "split_method": expense.split_method, "created_at": expense.created_at} for expense in expenses]

        return Response(expense_data)
    
class OverallExpensesView(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

