from django import forms

from user.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'min_distance', 'max_distance', 'min_dating_age',
                  'max_dating_age', 'dating_sex', 'vibration', 'only_matche',
                  'auto_play']
