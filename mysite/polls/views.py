from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions"

    def get_queryset(self):
        """
        Return the last five published questions (not including those
        set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes unpublished questions
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


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
