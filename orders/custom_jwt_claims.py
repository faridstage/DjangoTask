from django.utils import timezone
from django.contrib.auth.signals import user_logged_in
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import exceptions

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self,attrs):

        data = super().validate(attrs)

        user_logged_in.send(sender=self.user.__class__,request=self.context['request'],user=self.user)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['is_admin'] = self.user.is_staff
        data['is_active'] = self.user.is_active
        data['username'] = self.user.username
        data['company_id'] = self.user.company_id
        data['role'] = self.user.role
        data['id'] = self.user.id

        return data
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args,**kwargs):

        try:
            response = super().post(request, *args,**kwargs)
        except exceptions.AuthenticationFailed as e:
            if getattr(request, "axes_locked_out", request):
                raise exceptions.AuthenticationFailed(detail="Due to the too many unseccessfull attempts your account is blocked. please contact the administrator")
            else:
                raise e
        return response