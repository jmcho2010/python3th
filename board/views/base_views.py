from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question ,Answer, Comment
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

# 메인 페이지 작성
# 질문 목록 출력
# 21.09.17 조준모
def index(request):
    # Question.objects.order_by('-create_date')
    # Question 모델에서 객체를 참조하는데 / -가 붙어 있으면 해당 객체를 기준으로 역순정렬
    # 역순으로 정렬해올것. (객체는 create_date)

    # 페이징처리 추가 21.09.24 조준모

    # 페이징 처리 관련 템플릿 태그 속성.(템플릿단 페이징 처리 속성)
    # .count : 전체 게시물 개수
    # .per_page : 페이지당 보여줄 게시물 개수
    # .page_range : 페이지 범위
    # number : 현재 페이지 번호
    # previous_page_number : 이전 페이지 번호
    # next_page_number : 다음 페이지 번호
    # has_previous : 이전 페이지 유무
    # has_next : 다음 페이지 유무
    # start_index : 현재 페이지 시작 인덱스
    # end_index : 현재 페이지 끝 인덱스

   # 페이지의 입력 파라미터 추가.
    page = request.GET.get('page', '1')

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리 기능 구현
    pagenator = Paginator(question_list, 10)# 페이지당 10개씩
    page_obj = pagenator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'question_list.html', context)

def detail(request, question_id):
    # 글의 제목과 내용 출력
    question = Question.objects.get(id=question_id)
    return render(request, 'question_detail.html', {'question': question})
