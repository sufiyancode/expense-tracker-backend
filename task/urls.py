from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from task.views import UserCreateView, UserDetailView, AddExpenseView, UserExpensesView, OverallExpensesView

urlpatterns = [
    path('login/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(), name='user-create'),
    path('users/', UserDetailView.as_view(), name='user-detail'),
    path('expenses/', AddExpenseView.as_view(), name='expense-create'),
    path('expenses/user-expenses/', UserExpensesView.as_view(), name='user-expenses'),
    path('expenses/all/', OverallExpensesView.as_view(), name='overall-expenses'),
]
