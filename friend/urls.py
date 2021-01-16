from django.urls import path

from friend.views import(
	send_friend_request,
	friend_request_view,
	accept_friend_request,
	remove_friend,
	decline_friend_request,
	cancel_friend_request,
	friend_list_view,
)

app_name = 'friend'

urlpatterns = [
    path('friend_list/<user_id>', friend_list_view, name='list'),
    path('friend_remove/', remove_friend, name='remove-friend'),
    path('friend_request/', send_friend_request, name='friend-request'),
    path('friend_requests/<user_id>/', friend_request_view, name='friend-requests'),
    path('friend_request_accept/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    path('decline_friend_request/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
    path('cancel_friend_request/', cancel_friend_request, name='friend-request-cancel'),
]