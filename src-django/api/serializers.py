from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
    
class CustomRegisterSerializer(RegisterSerializer):
    username = None
    name = serializers.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

    def get_cleaned_data(self):
        # data = super().get_cleaned_data()
        # data['name'] = self.validated_data.get('name', '')
        # return data
        return{
            'email':self.validated_data.get('email',''),
            'password':self.validated_data.get('password',''),
            'name':self.validated_data.get('name',''),
        }
    
    def save(self, request):
        print("🔥 Using CustomRegisterSerializer")
        # user = super().save(request)
        # user.name = self.cleaned_data.get('name', '')
        # user.save()
        # return user
        from allauth.account.adapter import get_adapter
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.email = self.cleaned_data.get('email')
        user.name = self.cleaned_data.get('name', '')
        adapter.save_user(request, user, self)
        return user