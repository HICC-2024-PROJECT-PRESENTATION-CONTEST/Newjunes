from django.shortcuts import render
import json

# Create your views here.
def test(request):
    return render(request, 'main/index_rework.html')


def index(request):
    return render(request, 'main/index.html')


def search(request):
    if request.method=='POST':
        return

    if request.method=='GET':
        return render(request, 'main/search.html')


from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Lecture, Division
from django.http.response import JsonResponse
from django.core import serializers
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def lecture(request):
    if request.method=='GET':
        course_number = request.GET.get('course-number', None)
        if course_number==None:
            raise Http404("학수번호가 입력되지 않았습니다.")
        
        lecture = get_object_or_404(Lecture, pk=course_number)
        lecture_json = serializers.serialize('json', [lecture])
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
        lecture.save()

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
        division.save()

        return JsonResponse(data)