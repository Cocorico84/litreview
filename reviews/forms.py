from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.forms import ModelForm, RadioSelect, CharField
from .models import Ticket, Review, UserFollows


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

    def get_success_url(self):
        return reverse_lazy('create_user')

    def form_valid(self, form):
        """
        The form is valid only if the user put the same password twice during the creation of his account.
        """
        if form.cleaned_data['password1'] == form.cleaned_data['password2']:
            User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        return HttpResponseRedirect(reverse_lazy("create_user"))


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image",)


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "headline", "body",)
        widgets = {"rating": RadioSelect(choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                                         attrs={"class": "list-unstyled d-flex flex-row justify-content-around"})}


class FollowerForm(ModelForm):
    followed_user = CharField(max_length=30)

    class Meta:
        model = UserFollows
        exclude = ("followed_user", "user")

    def clean_followed_user(self):
        """
        In the input area, a checking is made to know if the user exists. It accepts only if the user is well written.
        """
        cleaned_data = super(FollowerForm, self).clean()
        if not User.objects.filter(username=cleaned_data["followed_user"]).exists():
            raise ValidationError("This user doesn't exist")
        return cleaned_data["followed_user"]
