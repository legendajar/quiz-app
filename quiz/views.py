from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from account.models import Profile
from .models import *
from django.db.models import Q
from quiz.models import QuizSubmission
from django.contrib import messages

# Create your views here..

@ login_required(login_url='login')
def all_quiz(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    quizzez = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()

    context = {
        "user_profile": user_profile,
        "quizzez": quizzez,
        "categories": categories,
    }
    return render(request, 'all-quiz.html', context)

@login_required(login_url='login')
def search_view(request, category):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)


    # search by searchbar
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        query = Q(title__icontains=q) | Q(description__icontains=q)
        quizzez = Quiz.objects.filter(query)
    

    # search by category
    elif category != " ":
        quizzez = Quiz.objects.filter(category__name=category).order_by('-created_at')

    else:
        quizzez = Quiz.objects.order_by('-created_at')

    categories = Category.objects.all()

    context= {
        "user_profile": user_profile,
        "quizzez":quizzez,
        "categories": categories,
    }

    return render(request, 'all-quiz.html', context)

@login_required(login_url='login')
def quiz_view(request, quiz_id):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    quiz = Quiz.objects.filter(id=quiz_id).first()

    total_questions = quiz.question_set.all().count()

    if request.method == 'POST':
        # Get the score
        score = request.POST.get('score',0)

        # Check if the user has already attempted the quiz
        if QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists():
            messages.success(request, f"This time you got {score} out of {total_questions}")
            return redirect('quiz', quiz_id=quiz_id)
        
        # save the new quiz submission
        submission = QuizSubmission(user=request.user, quiz=quiz, score=score)
        submission.save()

        # show the result in message
        messages.success(request, f"Quiz Submitted Succesfully! You got {score} out of {total_questions}")
        return redirect('quiz', quiz_id)

    if quiz != None:
        context = {'user_profile': user_profile, 'quiz': quiz}
    else:
        return redirect('all_quiz')
    
    return render(request, 'quiz.html', context)