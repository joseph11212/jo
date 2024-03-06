from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.corecode.models import StudentClass, AcademicSession, AcademicTerm, Subject
from apps.students.models import Student
from .models import Result


@login_required
def create_result(request):
    classes = StudentClass.objects.all()
    subjects = Subject.objects.all()
    sessions = AcademicSession.objects.all()  # Retrieve all academic sessions
    terms = AcademicTerm.objects.all()  # Retrieve all academic terms
    students = None
    selected_subjects = []

    if request.method == "POST":
        class_id = request.POST.get('current_class')
        selected_subject_ids = request.POST.getlist('selected_subjects')
        session_id = request.POST.get('session')
        term_id = request.POST.get('term')

        if class_id and selected_subject_ids and session_id and term_id:
            students = Student.objects.filter(current_class_id=class_id)
            selected_subjects = Subject.objects.filter(id__in=selected_subject_ids)
        else:
            messages.error(request, "Please select a class, session, term, and at least one subject.")
            return redirect('create-result')

        def save_scores():
            # Validate if all score inputs are filled for each student and subject
            scores_filled = True
            for student in students:
                for subject in selected_subjects:
                    score_key = f'score_{student.id}_{subject.id}'
                    score_value = request.POST.get(score_key, '').strip()
                    if not score_value:
                        scores_filled = False
                        break
            if not scores_filled:
                messages.error(request, "Please fill in all score inputs.")
                return redirect('create-result')

            # Process and save scores
            academic_session = AcademicSession.objects.get(id=session_id)
            academic_term = AcademicTerm.objects.get(id=term_id)
            for student in students:
                for subject in selected_subjects:
                    score_key = f'score_{student.id}_{subject.id}'
                    score_value = request.POST.get(score_key, '').strip()
                    # Create or get the result instance
                    result, created = Result.objects.get_or_create(
                        student=student,
                        session=academic_session,
                        term=academic_term,
                        current_class=student.current_class,
                        subject=subject
                    )
                    # Update or save the score to the database
                    result.scores[score_key] = score_value
                    result.save()

            # Display a success message
            messages.success(request, "Scores saved successfully.")
            # Redirect to view result page
            return redirect('view-result')

        if 'save_scores' in request.POST:
            return save_scores()

    return render(request, "result/create_result.html", {"classes": classes, "students": students, "subjects": subjects, "selected_subjects": selected_subjects, "sessions": sessions, "terms": terms})


@login_required
def view_result(request):
    # Retrieve all results from the database
    results = Result.objects.all()

    # Prepare data for rendering in the template
    result_data = []

    for result in results:
        # Process each result as needed
        result_info = {
            'student': result.student,
            'session': result.session,
            'term': result.term,
            'class': result.current_class,
            'subject': result.subject,
            'scores': result.scores
        }
        result_data.append(result_info)

    # Pass data to the template for rendering
    return render(request, 'result/view_result.html', {'result_data': result_data})

