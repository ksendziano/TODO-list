import os
import zipfile
from copy import deepcopy
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.core.validators import validate_email
from django.db import IntegrityError

from users.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import *


def board_list(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_moderator or request.user.is_staff:
                board_object_list = Board.objects.all()
            else:
                board_object_list = Board.objects.filter(user_creator=request.user)
            context = {'board_list': board_object_list}
            return render(request, 'BoardList.html', context)
        else:
            context = {'form': FormLogin()}
            return render(request, 'LoginPage.html', context)

    elif request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main-page')
            else:
                messages.add_message(request, messages.WARNING, 'Incorrect email or password')
                return render(request, 'LoginPage.html', {'form': form})


def log_in(request):
    pass

def task_list(request, pk):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, pk=pk)
        task_object_list = board.task_set.all()
        create_task_form = CreateTaskForm()
        context = {'task_list': task_object_list, 'board': board, 'create_task_form': create_task_form}
        return render(request, 'TaskList.html', context)
    else:
        return redirect('main-page')


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('main-page')


def create_board(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            color = request.POST.get('color', None)
            if len(color) != 7 or color[0] != '#' or str(color[1:]).isalpha() is not True:
                messages.add_message(request, messages.WARNING, 'Color format is: #AAAAAA')
                return render(request, 'CreateBoard.html', context={'create_board_form': CreateBoardForm()})
            title_board = request.POST.get('title', None)
            if title_board is not None:
                Board.objects.create(title=title_board, user_creator=request.user, color=color)
                title_board = None
        elif request.method == 'GET':
            return render(request, 'CreateBoard.html', context={'create_board_form': CreateBoardForm()})
    return redirect('main-page')


def delete_board(request, pk):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, pk=pk)
        board.delete()
    return redirect('main-page')


def create_task(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'CreateTask.html', context={'create_task_form': CreateTaskForm(),
                                                               'pk': pk, 'title_page': 'Create task',
                                                               'color': board.color})
        elif request.method == 'POST':
            description = request.POST.get('description', None)
            scheduled_deadline = request.POST.get('scheduled_deadline', None)
            if len(scheduled_deadline) == 0:
                messages.add_message(request, messages.WARNING, 'Input deadlines !!!')
                return redirect(reverse('create_task', kwargs={'pk': pk}))
            if date_validate(scheduled_deadline) is not True:
                print(scheduled_deadline)
                messages.add_message(request, messages.WARNING, 'Deadline should be today or later')
                return redirect(reverse('create_task', kwargs={'pk': pk}))
            status = request.POST.get('task_status', None)
            file = request.FILES.get('file', None)
            if file is None or file.size > 8388608:
                file = None
            board = get_object_or_404(Board, pk=pk)
            task = board.task_set.create(description=description,
                                         scheduled_deadline=scheduled_deadline,
                                         task_status=status, file=file)
            task.save()
    return redirect(reverse('Board', kwargs={'pk': pk}))


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'SignUp.html', context={'form': SignUpForm()})
    else:
        form = SignUpForm(request.POST)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        moderator = request.POST.get('moderator',False)
        form = SignUpForm(request.POST)
        try:
            validate_email(email)
        except ValidationError:
            messages.add_message(request, messages.WARNING, 'Input correct email')
            return redirect(reverse('sign_up'))
        try:
            validate_password(password)
        except ValidationError:
            messages.add_message(request,messages.WARNING,'Password is very simple')
            return redirect(reverse('sign_up'))
        try:
            user = User.objects.create_user(email=email, password=password)
        except IntegrityError:
            messages.add_message(request,messages.WARNING,'That email has already taken')
            return redirect(reverse('sign_up'))
        if user is not None:
            user.name = username
            if moderator:
                user.is_moderator = True
            else:
                user.is_moderator = False
            user.save()
            return redirect('main-page')
        else:
            return redirect(reverse('sign_up'))


def replace_task(request, board_pk, task_pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            new_parent_board_id = request.POST.get('new_parent_board', None)
            task = Task.objects.get(pk=task_pk)
            new_parent_board = Board.objects.get(pk=new_parent_board_id)
            if 'replace' in request.POST:
                task.parent_board = new_parent_board
                task.save()
            elif 'copy' in request.POST:
                copy_of_task = new_parent_board.task_set.create(description=task.description,
                                                                scheduled_deadline=task.scheduled_deadline,
                                                                real_deadline=task.real_deadline,
                                                                task_status=task.task_status,
                                                                file=task.file)
                for tag in task.tag_set.all():
                    copy_of_task.tag_set.create(text=tag.text)
                copy_of_task.save()
            return redirect(reverse('Board', kwargs={'pk': board_pk}))
        elif request.method == 'GET':
            board = get_object_or_404(Board, pk=board_pk)
            if request.user.is_staff or request.user.is_moderator:
                board_object_list = Board.objects.all()
            else:
                board_object_list = Board.objects.filter(user_creator=request.user)
            return render(request, 'Replace_copy_task.html', context={'title_page': 'Replace or copy task',
                                                                      'board_pk': board_pk,
                                                                      'task_pk': task_pk,
                                                                      'replace_task_form': ReplaceTaskForm(
                                                                          board_object_list),
                                                                      'board_list': board_object_list,
                                                                      'color': board.color})
    return redirect('main-page')


def detail_task(request, task_pk, board_pk):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, pk=board_pk)
        task = board.task_set.get(pk=task_pk)
        edit_task_form = CreateTaskForm()
        add_tag_form = AddTagForm()
        if request.user.is_staff:
            board_object_list = Board.objects.all()
        else:
            board_object_list = Board.objects.filter(user_creator=request.user)
        replace_task_form = ReplaceTaskForm(board_object_list)
        return render(request, 'DetailTask.html',
                      context={'task': task, 'board': board,
                               'edit_task_form': edit_task_form,
                               'replace_task_form': replace_task_form,
                               'add_tag_form': add_tag_form, 'color': board.color})
    return redirect('main-page')


def delete_task(request, task_pk, board_pk):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, pk=board_pk)
        deleting_task = board.task_set.get(pk=task_pk)
        deleting_task.delete()
        return redirect(reverse('Board', kwargs={'pk': board_pk}))
    return redirect('main-page')


def edit_board(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            board = get_object_or_404(Board, pk=pk)
            new_board_title = request.POST.get('title', None)
            new_board_color = request.POST.get('color', None)
            if len(new_board_color) != 7 or new_board_color[0] != '#' or str(new_board_color[1:]).isalpha() != True:
                messages.add_message(request, messages.WARNING, 'Color format is: #AAAAAA')
                return render(request, 'EditBoard.html', context={'title_page': 'Edit board',
                                                                  'edit_board_form': CreateBoardForm(),
                                                                  'pk': pk,
                                                                  'color': board.color})
            board.title = new_board_title
            board.color = new_board_color
            board.save()
            return redirect(reverse('Board', kwargs={'pk': pk}))
        elif request.method == 'GET':
            board = get_object_or_404(Board, pk=pk)
            return render(request, 'EditBoard.html', context={'title_page': 'Edit board',
                                                              'edit_board_form': CreateBoardForm,
                                                              'pk': pk, 'color': board.color})
    else:
        return redirect('main-page')


def edit_task(request, board_pk, task_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            board = get_object_or_404(Board, pk=board_pk)
            task = board.task_set.get(pk=task_pk)
            description = request.POST.get('description', None)
            scheduled_deadline = request.POST.get('scheduled_deadline', None)
            status = request.POST.get('task_status', None)
            file = request.FILES.get('file', None)
            if file is None or file.size > 8388608:
                file = None
            task.description = description
            task.scheduled_deadline = scheduled_deadline
            task.task_status = status
            if status == 'COMPLETED':
                task.real_deadline = datetime.date(datetime.now())
            task.file = file
            try:
                task.save()
            except ValidationError:
                messages.add_message(request, messages.WARNING, 'Input deadlines !!!')
                return render(request, 'EditTask.html', context={'edit_task_form': CreateTaskForm(),
                                                                 'title_page': 'Edit task',
                                                                 'board_pk': board_pk,
                                                                 'task_pk': task_pk,
                                                                 'color': board.color})
            return redirect(reverse('detail_task', kwargs={'board_pk': board_pk,
                                                           'task_pk': task_pk}))
        elif request.method == 'GET':
            return render(request, 'EditTask.html', context={'edit_task_form': CreateTaskForm(),
                                                             'title_page': 'Edit task',
                                                             'board_pk': board_pk, 'task_pk': task_pk,
                                                             'color': board.color})
    else:
        return redirect('main-page')


def get_json(request):
    if request.user.is_authenticated:
        response = HttpResponse(content_type='application/zip')
        if request.user.is_staff or request.user.is_moderator:
            boards = Board.objects.all()
        else:
            boards = Board.objects.filter(user_creator=request.user)
        file_list = []
        if len(boards) is 0:
            messages.add_message(request, messages.WARNING, "You have not board")
            return redirect(reverse('main-page'))
        for board in boards:
            tasks = board.task_set.all()
            with open("{0}.json".format(board.title), "w") as out:
                file_list.append(out.name)
                strings = serializers.serialize('json', tasks)
                out.writelines(strings)
        zip_file = zipfile.ZipFile(response, 'w')
        for file in file_list:
            file_path = os.path.join(os.getcwd(), file)
            if (os.path.exists(file_path)):
                zip_file.write(os.path.basename(file_path))
                os.remove(file_path)
        zip_file.close()
        response['Content-Disposition'] = f'attachment; filename={str(request.user)}.zip'
        return response
    return redirect('main-page')


def get_task_file(request, board_pk, task_pk):
    if request.user.is_authenticated:
        response = HttpResponse(content_type='application/zip')
        zip_file = zipfile.ZipFile(response, 'w')
        task = get_object_or_404(Task, pk=task_pk)
        filepath = os.path.join(os.getcwd(), 'media', str(task.file))
        if os.path.exists(filepath):
            zip_file.write((os.path.relpath(filepath)))
            zip_file.close()
            response['Content-Disposition'] = f'attachment; filename={str(request.user)}.zip'
            return response
        return redirect(reverse('detail_task', kwargs={'board_pk': board_pk, 'task_pk': task_pk}))
    return redirect('main-page')


def add_tag(request, board_pk, task_pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            board = get_object_or_404(Board, pk=board_pk)
            task = board.task_set.get(pk=task_pk)
            tag = request.POST.get('tag', None)
            task.tag_set.create(text=tag)
            return redirect(reverse('detail_task', kwargs={'board_pk': board_pk, 'task_pk': task_pk}))
        elif request.method == 'GET':
            board = get_object_or_404(Board, pk=board_pk)
            return render(request, 'AddTag.html', context={'title_page': 'Add tag',
                                                           'add_tag_form': AddTagForm(),
                                                           'board_pk': board_pk, 'task_pk': task_pk,
                                                           'color': board.color})
    else:
        return redirect('main-page')


def search_tag(request, tag):
    if request.user.is_authenticated:
        tasks_with_current_tag = []
        list_of_lists = []
        all_boards = []
        list_for_test = []
        if request.user.is_staff or request.user.is_moderator:
            board_object_list = Board.objects.all()
        else:
            board_object_list = Board.objects.filter(user_creator=request.user)
        for board in board_object_list:
            for task in board.task_set.all():
                for current_tag in task.tag_set.all():
                    if current_tag.text == tag:
                        if board not in all_boards:
                            all_boards.append(board)
                            list_for_test.append(task)
                        tasks_with_current_tag.append(task)
                        break
            list_of_lists.append(deepcopy(tasks_with_current_tag))
            tasks_with_current_tag.clear()
        list_of_lists = [list for list in list_of_lists if list]
        pair_list = zip(all_boards, list_of_lists)
        return render(request, 'SearchedTask.html', context={'board_list': pair_list,
                                                             'tag': tag,
                                                             'list_for_test': list_for_test})
    return redirect('main-page')


def complete_task(request, board_pk, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if task.task_status == 'COMPLETED':
        messages.add_message(request, messages.WARNING, 'This task has already been completed')
        return redirect(reverse('detail_task', kwargs={'board_pk': board_pk, 'task_pk': task_pk}))
    else:
        task.task_status = 'COMPLETED'
        task.real_deadline = datetime.date(datetime.now())
        task.save()
        return redirect(reverse('detail_task', kwargs={'board_pk': board_pk,
                                                       'task_pk': task_pk}))


def date_validate(scheduled_deadline):
    today_date = datetime.date(datetime.now())
    deadline_month = int(scheduled_deadline[5:7])
    deadline_day = int(scheduled_deadline[8:10])
    deadline_year = int(scheduled_deadline[0:4])
    if deadline_year < today_date.year:
        return False
    elif deadline_year == today_date.year and deadline_month < today_date.month:
        return False
    elif deadline_year == today_date.year and deadline_month == today_date.month and \
            deadline_day < today_date.day:
        return False
    else:
        return True
