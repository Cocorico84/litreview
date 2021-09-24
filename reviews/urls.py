from django.urls import path

from .views import ReviewListView, ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView, \
    TicketDetailView, TicketListView, TicketCreateView, TicketUpdateView, TicketDeleteView, CreateUserView, AddFollowerView, FollowerListView, PostView

urlpatterns = [
    path('', ReviewListView.as_view(), name='review_list'),
    path('review/<int:pk>', ReviewDetailView.as_view(), name='review_detail'),
    path('review/add/', ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/update', ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete', ReviewDeleteView.as_view(), name='review_delete'),
    path('ticket', TicketListView.as_view(), name='ticket_list'),
    path('ticket', TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/add', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/<int:pk>/update', TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/<int:pk>/delete', TicketDeleteView.as_view(), name='ticket_delete'),
    path('create_user', CreateUserView.as_view(), name='create_user'),
    path('follower/add', AddFollowerView.as_view(), name='add_follower'),
    path('follower', FollowerListView.as_view(), name='follower'),
    path('posts', PostView.as_view(), name='posts')
]
