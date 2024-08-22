from django.db import models

# Create your models here.


class Lecture(models.Model):
    course_number = models.CharField(primary_key=True, max_length=6) # 학수번호
    grade = models.DecimalField(max_digits=1, decimal_places=0) # 개설학년
    classification = models.CharField(max_length=20) # 이수구분(전공/교양)
    name = models.CharField(max_length=50) # 과목명
    credit = models.DecimalField(max_digits=1, decimal_places=0) # 학점
    department = models.CharField(max_length=20) # 개설학과

    
class Division(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE) # 강의
    division_number = models.CharField(max_length=3) # 분반 번호
    professor = models.CharField(max_length=30) # 교수
    period = models.CharField(max_length=15) # 강의 시간
    lecture_room = models.CharField(max_length=25) # 강의실
    rating = models.DecimalField(max_digits=3, decimal_places=2) # 강의평
    capacity = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True) # 정원
    applicant = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True) # 담은 인원
    annotation = models.TextField(null=True, blank=True) # 비고