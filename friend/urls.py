from django.urls import path

from friend.views import(
	send_friend_request,
	friend_request_view,
)

app_name = 'friend'

urlpatterns = [
    path('friend_request/', send_friend_request, name='friend-request'),
    path('friend_request/<user_id>/', friend_request_view, name='friend-requests'),
]