from django.shortcuts import render, redirect
from .models import Lecture, Division
import json

# Create your views here.
def test(request):
    return render(request, 'main/index_rework.html')


def index(request):
    return render(request, 'main/index.html')


def select(request):
    return render(request, 'main/select.html')


def set_break(request):
    return render(request, 'main/break.html')


def result(request, schedules):
    print(schedules)
    return render(request, 'main/result.html')


from django.http import Http404
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
@csrf_exempt
def lecture(request):
    if request.method=='GET':
        course_number = request.GET.get('course-number', None)
        if course_number==None:
            return JsonResponse({"message": "학수번호를 입력하지 않았습니다."}, status=400)
        
        try:
            lecture = Lecture.objects.get(pk=course_number)
        except Lecture.DoesNotExist:
            return JsonResponse({"message": "강의를 찾을 수 없습니다."}, status=404)

        response = {
            'name': lecture.name,
            'courseNumber': lecture.course_number,
            'credit': lecture.credit,
            'classification': lecture.classification,
            'department': lecture.department,
            'division': {}
        }
        divisions = lecture.division_set.all()
        for division in divisions:
            print(division)
            temp = {
                'divisionNumber': division.division_number,
                'professor': division.professor,
                'period': division.period,
                'lecture_room': division.lecture_room,
                'rating': division.rating
            }
            response["division"][division.division_number] = temp
        # response["division"] = divisions
        print(divisions)
        return JsonResponse(response)
    
    if request.method=='POST':
        data = json.loads(request.body)

        lecture = Lecture()
        lecture.name = data.get("name", None)
        lecture.course_number = data.get("course_number", None)
        lecture.grade = data.get("grade", None)
        lecture.classification = data.get("classification", None)
        lecture.credit = data.get("credit", None)
        lecture.department = data.get("department", None)
        try:
            lecture.save()
        except IntegrityError:
            return JsonResponse({"message": "강의 정보를 잘못 입력했습니다."}, status=400)


        division = Division()
        division.lecture = lecture
        division.division_number = data.get("division", None)
        division.professor = data.get("professor", None)
        division.period = data.get("period", None)
        division.lecture_room = data.get("lecture_room", None)
        division.rating = data.get("rating", None)
        division.applicant = data.get("applicant", None)
        division.annotation = data.get("annotation", None)
        division.capacity = data.get("capacity", None)
        try:
            division.save()
        except IntegrityError:
            return JsonResponse({"message": "강의 정보를 잘못 입력했습니다."}, status=400)

        return JsonResponse(data)


from .modules import schedule_generator
@csrf_exempt
def generate(request):
    if request.method=='POST':
        result = {}

        # data = json.loads(request.body)
        primary = json.loads(request.POST.get("primary"))
        non_primary = json.loads(request.POST.get("nonPrimary"))
        breaks = json.loads(request.POST.get("break"))

        lectures = {}

        for course_number in primary:
            lecture = Lecture.objects.get(pk=course_number)
            form = {
                "name": lecture.name,
                "courseNumber": lecture.course_number,
                "division": {},
                "primary": 1
            }
            for division in lecture.division_set.all():
                form["division"][division.division_number] = {
                    "professor": division.professor,
                    "divisionNumber": division.division_number,
                    "period": schedule_generator.convert_period_v2(division.period)
                }
            lectures[course_number] = form
        
        for course_number in non_primary:
            lecture = Lecture.objects.get(pk=course_number)
            form = {
                "name": lecture.name,
                "courseNumber": lecture.course_number,
                "division": {},
                "primary": 0
            }
            for division in lecture.division_set.all():
                form["division"][division.division_number] = {
                    "professor": division.professor,
                    "divisionNumber": division.division_number,
                    "period": schedule_generator.convert_period_v2(division.period)
                }
            lectures[course_number] = form

        result["lectures"] = lectures

        lectures["000000"] = {
            "name": "break",
            "periods": breaks
        }

        res = schedule_generator.generate_schedule(json.dumps(lectures))
        if res==[]:
            return redirect('main/failed.html')
        
        for schedule in res:
            for i in range(len(schedule)):
                schedule[i] = list(schedule[i].split("-"))

        result["result"] = res

        print(result)
        return render(request, 'main/result.html', result)
    else:
        print("POST가 아닌 다른게 들어옴")



def generate_table_html(result):

    return render(request, 'main/table.html', context)