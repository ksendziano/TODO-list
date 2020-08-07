import os
import zipfile
from copy import deepcopy
from datetime import datetime
from django.core import serializers
from list.models import Board

DATE_VALIDATE_STRING_ERROR = 'Deadline should be today or later' 
#У тебя здесь набор функционала разного рода, где ты прочитал и увидел, что все эти вещи держаться в одном файле и имеют такие названия?жно я




# В этой функции можно явно проверить 2 даты datetime.today()>=scheduled_deadline
def date_validate(scheduled_deadline):
    if len(scheduled_deadline) == 0: # Только за вот эту строчку (проверку), если ты захочешь показать этот код компании, например, как пример того, что ты делаешь, тебя сразу откинут навсегда
        return 'Input deadline !!!'
    today_date = datetime.date(datetime.now()) # datetime.today()
    deadline_month = int(scheduled_deadline[5:7])#
    deadline_day = int(scheduled_deadline[8:10])# 
    deadline_year = int(scheduled_deadline[0:4])#
    if deadline_year < today_date.year:
        return DATE_VALIDATE_STRING_ERROR
    elif deadline_year == today_date.year and deadline_month < today_date.month:
        return DATE_VALIDATE_STRING_ERROR
    elif deadline_year == today_date.year and deadline_month == today_date.month and \
            deadline_day < today_date.day:
        return DATE_VALIDATE_STRING_ERROR
    else:
        return 'Okay' # https://www.youtube.com/watch?v=Obgnr9pc820


def get_all_boards(user):
    if user.is_moderator or user.is_staff:
        return Board.objects.all()
    else:
        return Board.objects.filter(user_creator=user)


def add_json_in_zip(board_object_list, response, file_list):
    for board in board_object_list:
        task_object_list = board.task_set.all()
        with open("{0}.json".format(board.title), "w") as out:
            file_list.append(out.name)
            strings = serializers.serialize('json', task_object_list)
            out.writelines(strings)
    zip_file = zipfile.ZipFile(response, 'w')
    for file in file_list:
        file_path = os.path.join(os.getcwd(), file)
        if os.path.exists(file_path):
            zip_file.write(os.path.basename(file_path))
            os.remove(file_path)
    zip_file.close()

# Здесь можно все сделать через .filter() и не прокидывать ненужные пустые объекты
def search_tasks_by_tag(board_object_list, tag, all_boards, list_of_lists):
    tasks_with_current_tag = []
    for board in board_object_list:
        for task in board.task_set.all():
            for current_tag in task.tag_set.all():
                if current_tag.text == tag:
                    if board not in all_boards: 
                        all_boards.append(board)
                    tasks_with_current_tag.append(task)
                    break
        list_of_lists.append(deepcopy(tasks_with_current_tag))
        tasks_with_current_tag.clear()


def change_task_fields_from_request(task, request):
    description = request.POST.get('description', None) # Зачем ты понасоздавал эти переменные, почему просто не сделал task.description = request.POST.get('description', None) и т.д.
    scheduled_deadline = request.POST.get('scheduled_deadline', None)
    status = request.POST.get('task_status', None)
    file = request.FILES.get('file', None)
    if file is None or file.size > 8388608: # Число в константы и зачем None превращать в None??? Это должна быть отдельная валидация
        file = None
    task.description = description
    task.scheduled_deadline = scheduled_deadline
    task.task_status = status
    if status == 'COMPLETED' and len(str(task.real_deadline)) == 0:# снова какая-то странная валидация
        task.real_deadline = datetime.date(datetime.now())
    task.file = file
 
    
 
