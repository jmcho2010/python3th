from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question ,Answer
from .forms import QuestionForm, AnswerForm
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
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

def test(request):
    return render(request, 'index.html')

# 21.09.23 답변등록하기
# 작성자 : 조준모
# get_object_or_404 : 사용자에게 보여지는 에러 메세지 제어 함수
#                     데이터의 유출을 막기 위한방법.
# redirect : 페이지의 재 요청 데이터를 전송후 페이지를 새로고침 하기 위함.
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 다음과 같은 방식이 가능했던 이유는 question, answer 모델이 외래키로
    # 연결되어있기 때문.
    #question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # answer 모델을 직접 사용하는 방법.
    answer = Answer(question=question, content=request.POST.get('content'),
                    create_date=timezone.now())
    answer.save()
    return redirect('board:detail', question_id=question.id)

# 21.09.24 조준모 질문등록 기능 구현
# @LOGIN_REQUIRED : 해당 함수가 로그인이 되어있는지를 확인하는 데코레이터
#                   만약 로그인 되어있지 않다면 해당 url을 호출
@login_required(login_url='common:login')
def question_create(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user # request.user : 현재 로그인한 계정의
                                           #                User모델 객체.
            question.create_date = timezone.now()
            question.save()
            return redirect('board:index')
    else:
        form = QuestionForm()
    return render(request, 'board/question_form.html', {'form': form})

@login_required(login_url='common:login')
def answer_create(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'question_detail.html', context)