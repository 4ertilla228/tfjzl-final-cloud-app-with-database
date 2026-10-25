# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission

# Представление списка курсов
from django.views import generic

class CourseListView(generic.ListView):
    model = Course
    template_name = 'onlinecourse/course_list.html'

# Представление деталей курса
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

# Функция обработки отправки экзамена (Task 5)
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Логика обработки ответов и создания Submission
    submission = Submission.objects.create(course=course)
    return redirect(reverse('onlinecourse:show_exam_result', args=[course.id, submission.id]))

# Функция показа результатов экзамена (Task 5)
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    context = {
        'course': course,
        'submission': submission,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)