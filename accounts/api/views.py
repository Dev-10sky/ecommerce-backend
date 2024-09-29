from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import status
from accounts.forms import CustomUserLoginForm
from accounts.api.serializers import CustomRegisterSerializer, CustomLoginSerializer
from accounts.models import CustomUser
from carts.models import Cart


class CustomLoginView(LoginView):
    
    redirect_authenticated_user = True
    serializer_class = CustomLoginSerializer

    def get_success_url(self):
        return reverse_lazy('')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Authentication')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get(self, request, format=None):
        context = {
            'form': AuthenticationForm(request=request)
        }
        return render(request,"account/login.html",context=context)
    
    def post(self, request, format=None):
        if request.method == "POST":
            authform = AuthenticationForm(data=request.POST)
            if authform.is_valid():
                login(request, authform.get_user())
                post_dict = request.data
                email = post_dict['username']
                context = None
                if request.user.is_authenticated:
                    print("Current logged in User ID: ",request.user.id)
                    user_data = CustomUser.objects.get(pk=request.user.id)
                    cart_data = CustomUser.objects.get(pk=request.user.id).cart
                    print(cart_data)
                    context = {
                        'User': {
                                    'first_name': user_data.first_name,
                                    'last_name': user_data.last_name,
                                    'email':user_data.email
                                },
                        'Cart': {'name': cart_data.name}
                    }
                else:
                    return Response(request.data,status=status.HTTP_404_NOT_FOUND)
                return render(request,"account/homepage.html",context=context)
            else:
                return Response(request.data,status=status.HTTP_400_BAD_REQUEST)

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
