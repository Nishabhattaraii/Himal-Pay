
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout

from authentication.models import SubmissionID, WebhookResponse
from .forms import KYCPrefillForm, RegisterForm, LoginForm , KYCForm
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .forms import KYCForm
import uuid
import requests
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from authentication.serializers import WebhookSerializer
from rest_framework.response import Response
from rest_framework import status
import json
from django.conf import settings

a = settings.URL
class RegisterView(View):
    
    def get(self,request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class LoginView(View):
    
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)
            return redirect('kyc_form')
        return render(request, 'login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('login')

 
class KYCView(View):
    
    def get(self, request):
        form = KYCForm(user=request.user)
        return render(request, 'kyc_form.html', {'form': form})

    def post(self, request):
        form = KYCForm(request.POST, user=request.user)
        if form.is_valid():
            user_profile = request.user
            user_profile.full_name = form.cleaned_data['full_name']
            user_profile.email = form.cleaned_data['email']
            user_profile.mobile_number = form.cleaned_data['mobile_number']
            user_profile.dob = form.cleaned_data['dob']
            user_profile.gender = form.cleaned_data['gender']
            user_profile.save()
            unique_id = self.create_submission_id(user=request.user)
            url = self.start_vkyc(submission_id=unique_id, user=request.user)
            return redirect(url)
        return render(request, 'kyc_form.html', {'form': form})
    
    def create_submission_id(self, user):
        while True:
            unique_id = uuid.uuid4().hex[:3].upper() + str(int(uuid.uuid4().int & (1<<12)-1)).zfill(3)
            unique_id = 'HP' + unique_id

            submission_id= SubmissionID.objects.filter(
                submission_id=unique_id
            ).first()

            if not submission_id:
                SubmissionID.objects.create(
                    user=user,
                    submission_id=unique_id
                )
                return unique_id
            continue
    
    
    def start_vkyc(self,submission_id, user):
        from datetime import date
        url = "http://202.166.198.129:8069/api/core/initiate/"
        dob = user.dob
        data ={
            "full_name": user.full_name,
            'dob' : dob.strftime('%Y-%m-%d') if isinstance(dob, date) else dob,     
            "gender":user.gender,
            "email":user.email,
            "submission_id":submission_id
        }
        try:
            response = requests.post(url, json=data)
        except Exception as e:
            print("Exception: ", e)
            return
        redirection_url = response.json().get("data")
        return response.json().get("data")

        
class WebhookView(APIView):

    @csrf_exempt
    def post(self, request):
        serializer = WebhookSerializer(data =self.get_webhook_response())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK) 

    def get(self, request):
        submission_id = request.GET.get('submission_id')
        
        if submission_id:
            webhook_data = WebhookResponse.objects.filter(submission_id=submission_id)
            serializer = WebhookSerializer(webhook_data, many=True)
            return render(request, 'webhook_responses.html', {'webhook_responses': serializer.data})
        else:
            submission_ids = WebhookResponse.objects.values_list('submission_id', flat=True).distinct()
            return render(request, 'submission_ids.html', {'submission_ids': submission_ids})
    def get_webhook_response(self):
        if self.request.body :
            return json.loads(str(self.request.body,"utf-8"))
        return None

        
