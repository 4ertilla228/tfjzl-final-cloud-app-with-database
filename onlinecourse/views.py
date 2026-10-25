from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.all()

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    # Получаем или создаем запись Enrollment
    enrollment, _ = Enrollment.objects.get_or_create(user=user, course=course)

    # Создаем попытку сдачи
    submission = Submission.objects.create(enrollment=enrollment)

    # Извлекаем выбранные ID ответов из формы
    selected_choice_ids = []
    for key in request.POST:
        if key.startswith('choice_'):
            choice_id = request.POST[key]
            selected_choice_ids.append(int(choice_id))
            choice = get_object_or_404(Choice, id=choice_id)
            submission.choices.add(choice)

    submission.save()
    return redirect(reverse('onlinecourse:show_exam_result', args=[course.id, submission.id]))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_choice_ids = [c.id for c in submission.choices.all()]
    total_score = 0
    grade = 0

    for question in course.question_set.all():
        total_score += question.grade
        if question.is_get_score(selected_choice_ids):
            grade += question.grade

    passed = False
    if total_score > 0:
        percent = (grade / total_score) * 100
        if percent >= 70:
            passed = True
    else:
        percent = 100
        passed = True

    context = {
        'course': course,
        'submission': submission,
        'grade': grade,
        'total_score': total_score,
        'percent': percent,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)