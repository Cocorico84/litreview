from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import Ticket, Review, UserFollows
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUserForm, TicketForm, ReviewForm
from itertools import chain
from django.db.models import CharField, Value, Q


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "flow.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        reviews = Review.objects.filter(user=self.request.user).annotate(content_type=Value('REVIEW', CharField()))
        tickets = Ticket.objects.filter(user=self.request.user).annotate(content_type=Value('TICKET', CharField()))
        context["posts"] = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return context


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = "example.html"


class ReviewCreateView(LoginRequiredMixin, CreateView):
    review_form_class = ReviewForm
    ticket_form_class = TicketForm
    template_name = "create_review.html"

    def get(self, request, *args, **kwargs):
        review_form = self.review_form_class(**self.get_form_kwargs())
        ticket_form = self.ticket_form_class()
        return render(request, self.template_name, {'review_form': review_form, 'ticket_form': ticket_form})

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST)
        ticket_form.instance.user = self.request.user
        review_form.instance.user = self.request.user
        if ticket_form.is_valid():
            ticket = ticket_form.save()
            review_form.instance.ticket = ticket
            if review_form.is_valid():
                review_form.save()
            else:
                ticket.delete()
                return render(request, self.template_name, {'review_form': review_form, 'ticket_form': ticket_form})
        else:
            return render(request, self.template_name, {'review_form': review_form, 'ticket_form': ticket_form})
        return HttpResponseRedirect('/')


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ("headline", "body", "rating",)
    template_name = "update.html"
    success_url = reverse_lazy("review_list")


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "delete.html"
    success_url = reverse_lazy("review_list")


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket


class TicketCreateView(LoginRequiredMixin, CreateView):
    form_class = TicketForm
    template_name = "create_ticket.html"
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ("title", "description", "image",)
    template_name = "update.html"
    success_url = "/"


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "delete.html"
    success_url = "/"


class AddFollowerView(LoginRequiredMixin, CreateView):
    model = UserFollows
    fields = "__all__"
    template_name = "followers.html"


class FollowerListView(LoginRequiredMixin, ListView):
    model = UserFollows
    template_name = "followers.html"
    context_object_name = "follows"

    def get_queryset(self):
        return UserFollows.objects.filter(Q(user=self.request.user) | Q(followed_user=self.request.user))

    # def get(self, request, *args, **kwargs):
    #     # user = UserFollows.objects.get(user__username__icontains=request.GET.get("search_user"))
    #     user = UserFollows.objects.filter(user__username__icontains=request.GET.get("search_user"))
    #     return render(request, self.template_name, {'user': user})


class PostView(LoginRequiredMixin, ListView):
    template_name = "posts.html"
    context_object_name = "tickets"
    model = Ticket

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        reviews = Review.objects.filter(user=self.request.user).annotate(content_type=Value('REVIEW', CharField()))
        tickets = Ticket.objects.filter(user=self.request.user).annotate(content_type=Value('TICKET', CharField()))
        context["posts"] = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return context


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'registration.html'
    success_url = '/'
