from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import Ticket, Review, UserFollows
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUserForm, TicketForm, ReviewForm, FollowerForm
from itertools import chain
from django.db.models import CharField, Value, Q


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "flow.html"

    def get_context_data(self, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        reviews = Review.objects.filter(user=self.request.user).annotate(content_type=Value('REVIEW', CharField()))
        tickets = Ticket.objects.filter(user=self.request.user).annotate(content_type=Value('TICKET', CharField()))

        # followers = UserFollows.objects.filter(user=self.request.user).values_list('followed_user__username')
        followers = UserFollows.objects.filter(user=self.request.user)
        my_followers = [follow.followed_user for follow in followers]
        users = User.objects.filter(username__in=my_followers)

        follower_tickets = Ticket.objects.filter(user__in=users).annotate(
            content_type=Value('FOLLOWER_TICKET', CharField()))
        follower_reviews = Review.objects.filter(user__in=users).annotate(
            content_type=Value('FOLLOWER_REVIEW', CharField()))

        context["posts"] = sorted(
            chain(reviews, tickets, follower_tickets, follower_reviews),
            key=lambda post: post.time_created,
            reverse=True
        )
        return context


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


class ReviewFromPostCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ("headline", "body", "rating",)
    template_name = "create_review_from_ticket.html"
    success_url = reverse_lazy("review_list")

    def get_context_data(self, **kwargs):
        context = super(ReviewFromPostCreateView, self).get_context_data(**kwargs)
        context["ticket"] = Ticket.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ("headline", "body", "rating",)
    template_name = "update.html"
    success_url = reverse_lazy("review_list")


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "delete.html"
    success_url = reverse_lazy("review_list")


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
    success_url = reverse_lazy("posts")


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "delete.html"
    success_url = reverse_lazy("posts")


class FollowerListView(LoginRequiredMixin, CreateView):
    form_class = FollowerForm
    model = UserFollows
    template_name = "followers.html"
    success_url = reverse_lazy("follower")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.followed_user = User.objects.get(username=form.cleaned_data["followed_user"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FollowerListView, self).get_context_data(**kwargs)
        context["users"] = UserFollows.objects.filter(followed_user=self.request.user)
        context["followers"] = UserFollows.objects.filter(user=self.request.user)
        return context


class FollowerDelete(LoginRequiredMixin, DeleteView):
    model = UserFollows
    template_name = "delete.html"
    success_url = reverse_lazy("follower")


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
