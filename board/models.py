from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# ORM
# 데이터베이스의 데이터를 조회하거나 저장하기위해 원래는
# 쿼리(SQL)을 사용했지만 Django에서는
# 데이터베이스 테이블을 '모델화'해서 사용하고 쿼리들을
# Django 기준 python 코드로 처리하는 방법.

# ORM의 특징
# 개발자만의 쿼리(sql)을 만들기가 어렵다.
# 쿼리를 잘못 작성할 가능성이 낮아진다(간단한 명령에 한해서)
# DBMS를 변경(이관)할때 쿼리를 바꿀 필요가 없다.

# 모델 작성
# 질문, 답변 모델을 생성
# 질문모델
# subject : 질문의 제목
# content : 질문의 내용
# create_date : 질문을 작성한 일시

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject
# 답변모델
# question : 질문
# content: 답변의 내용
# create_date : e답변 작성 일시.
# 컬럼에 null을 허용하고 싶다면 null=True를 추가
# null=True : 컬럼에 null을 허용하는 속성
# blank=True : 어떤 조건으로도 값을 비워둘수 있음.
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

# 질문과 답변에 댓글기능 추가 21.10.05
# author : 댓글의 글쓴이
# content : 댓글 내용
# create_date : 댓글 작성일
# modify_date : 댓글 수정일
# question : 이 댓글이 달린 질문
# answer : 이 댓글이 달린 답변
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)






