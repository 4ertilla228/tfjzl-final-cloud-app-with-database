from django.shortcuts import render, get_object_or_404, redirect
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
    enrollment, _ = Enrollment.objects.get_or_create(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

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

    selected_ids = [c.id for c in submission.choices.all()]
    grade = 0
    possible_score = 0

    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            grade += question.grade

    total_score = possible_score
    percent = int((grade / possible_score) * 100) if possible_score > 0 else 100
    passed = percent >= 70

    context = {
        'course': course,
        'submission': submission,
        'grade': grade,
        'score': grade,
        'possible_score': possible_score,
        'total_score': total_score,
        'selected_ids': selected_ids,
        'percent': percent,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)