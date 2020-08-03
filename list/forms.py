from django import forms
<<<<<<< HEAD
from .models import Task, Board
=======
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from .models import *


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class FormLogin(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
>>>>>>> f9bd64681f6d662cbe8ab56681e597bccae2ba79


class CreateBoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'color')


class ReplaceTaskForm(forms.Form):
    new_parent_board = forms.ModelChoiceField(queryset=None)

    def __init__(self, board_list):
        super(ReplaceTaskForm, self).__init__()
        self.fields['new_parent_board'].queryset = board_list


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('description', 'task_status', 'file')


class AddTagForm(forms.Form):
    tag = forms.CharField(max_length=15)
