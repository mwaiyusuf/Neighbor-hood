from django.shortcuts import render,redirect, get_object_or_404 
import datetime as dt
from .permissions import IsAdminOrReadOnly
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import MerchSerializer
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required.

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .email import send_welcome_email
from django.contrib import messages

# Create your views here.

def home(request):

    if request.user.is_authenticated:
        if Join.objects.filter(user_id=request.user).exists():
            hood = Hood.objects.get(pk=request.user.join.hood_id.id)
            posts = Posts.objects.filter(hood=request.user.join.hood_id.id)
            businesses = Business.objects.filter(
                hood=request.user.join.hood_id.id)

            return render(request, 'neighhoods/neighbor.html', {"hood": hood, "businesses": businesses, "posts": posts})
        else:
            neighbourhoods = Hood.objects.all()
            return render(request, 'index.html', {"neighbourhoods": neighbourhoods})
    else:
        neighbourhoods = Hood.objects.all()
        return render(request, 'index.html', {"neighbourhoods": neighbourhoods})

def new_business(request):
    current_user = request.user

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.hood = request.user.join.hood_id
            business.save()
            return redirect('home')

    else:
        form = BusinessForm()
    return render(request, 'biz.html', {"form": form})


@login_required(login_url='/accounts/login/')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    hoods = Hood.objects.filter(user=request.user).all()
    business = Business.objects.filter(user=request.user).all()
    return render(request, 'profiles/profile.html', {"profile": profile, "hoods": hoods, "business": business})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.email = current_user.email
            profile.save()
        return redirect('profile')

    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {"form": form})

def hoods(request):

    hood = Hood.objects.filter(user=request.user)

    return render(request, 'neighhoods/neighbor.html', {"hood": hood})

@login_required(login_url='/accounts/login/')
def join(request, hoodId):

    hood = Hood.objects.get(pk=hoodId)
    if Join.objects.filter(user_id=request.user).exists():
        Join.objects.filter(user_id=request.user).update(hood_id=hood)
    else:

        Join(user_id=request.user, hood_id=hood).save()

    messages.success(
        request, 'Success! You have succesfully joined this Neighbourhood ')
    return redirect('home')


class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)

     def post(self, request, format=None):
        serializers = MerchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
      permission_classes = (IsAdminOrReadOnly,)

class MerchDescription(APIView):
      permission_classes = (IsAdminOrReadOnly,)
      def get_merch(self, pk):
          try:
              return MoringaMerch.objects.get(pk=pk)
          except MoringaMerch.DoesNotExist:
              return Http404

      def get(self, request, pk, format=None):
          merch = self.get_merch(pk)
          serializers = MerchSerializer(merch)
          return Response(serializers.data)

       def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk, format=None):
        merch = self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
