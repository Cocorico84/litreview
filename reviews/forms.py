from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import ModelForm, RadioSelect
from .models import Ticket, Review


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

    def get_success_url(self):
        return reverse('create_user')

    def form_valid(self, form):
        if form.cleaned_data['password1'] == form.cleaned_data['password2']:
            User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        return HttpResponseRedirect(reverse("create_user"))


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image",)


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "headline", "body",)
        widgets = {"rating": RadioSelect(choices=[(0, "0"),
                                                  (1, "1"),
                                                  (2, "2"),
                                                  (3, "3"),
                                                  (4, "4"),
                                                  (5, "5")],
                                         attrs={"class": "list-unstyled d-flex flex-row justify-content-around"})}
