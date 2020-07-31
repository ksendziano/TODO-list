from django import forms
from .models import Task, Board


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    moderator = forms.BooleanField(widget=forms.CheckboxInput,required=False)


class FormLogin(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


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
