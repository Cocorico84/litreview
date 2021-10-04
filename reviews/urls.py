from django.urls import path

from .views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView, \
    TicketCreateView, TicketUpdateView, TicketDeleteView, CreateUserView, \
    FollowerListView, PostView, FollowerDelete, ReviewFromPostCreateView

urlpatterns = [
    path('', ReviewListView.as_view(), name='review_list'),
    path('review/add/', ReviewCreateView.as_view(), name='review_create'),
    path('review/response/<int:pk>', ReviewFromPostCreateView.as_view(), name='review_create_from_ticket'),
    path('review/<int:pk>/update', ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete', ReviewDeleteView.as_view(), name='review_delete'),
    path('ticket/add', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/<int:pk>/update', TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/<int:pk>/delete', TicketDeleteView.as_view(), name='ticket_delete'),
    path('create_user', CreateUserView.as_view(), name='create_user'),
    path('follower', FollowerListView.as_view(), name='follower'),
    path('follower/<int:pk>/delete', FollowerDelete.as_view(), name="follower_delete"),
    path('posts', PostView.as_view(), name='posts')
]
