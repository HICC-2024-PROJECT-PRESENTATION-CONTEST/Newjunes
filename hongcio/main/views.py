from django.shortcuts import render
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


from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Lecture, Division
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