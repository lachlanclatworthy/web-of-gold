from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse

from .models import Question, Choice

def index(request):
    context = {"latest_questions" : Question.objects.order_by("-pub_date")[:5]}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": q})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = q.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Go back to the question voting form
        return render(request, "polls/detail.html",
                      {
                          "question": q,
                          "error_message": "You need to select a choice.",
                      })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # NOTE - We avoid a potential double POST by issuing a redirect
        return HttpResponseRedirect(reverse("polls:results", args=(q.id,)))
