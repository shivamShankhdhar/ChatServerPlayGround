from django.db import models
from django.conf import settings 
from django.utils import timezone

class FriendList(models.Model):
	user 			= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "user")
	friends			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name = "friends")

	def __str__(self):
		return self.user.username

	def add_friend(self, account):
		"""
		Add a new friend
		"""
		if not account in self.friends.all():
			self.friends.add(account)
			# self.save()

	def remove_friend(self, account):
		"""
		Remove a  friend
		"""
		if account in self.friends.all():
			self.friends.remove(account)


	def unfriend(self , removee):
		"""
		Initiate the action of unfriending someone
		"""
		remover_friend_list = self # person terminating the friendship

		# remove friend from remover friend list
		remover_friend_list.remove_friend(removee)

		# Remove friend from removee friend list 
		removee_friend_list = FriendList.objects.get(user = removee)
		removee_friend_list.remove_friend(self.user)

	def is_mutual_friend(self, friend):
		"""
		Is this a friend ?
		"""
		if friend in self.friends.all():
			return True
		return False


class FriendRequest(models.Model):
	sender 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "sender")
	receiver			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "receiver")

	# status of friend request 
	is_active 			= models.BooleanField(blank = True, null = False, default = True)
	timestamp 			= models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return f" {self.sender.username} Requested {self.receiver.username}"

	def accept(self):
		"""
		Accept a friend request
		update both SENDER and RECEIVER friend lists
		"""
		receiver_friend_list = FriendList.objects.get(username = self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user = self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()


	def decline(self):
		"""
		Decline a friend request 
		by setting is_active = False
		"""
		self.is_active = False
		self.save()

	def cancel(self):
		"""
		cancel friend request 
		it is 'cancelled' by setting the 'is_active' False
		This is only difference with respect to "declining" through the notification that is generated.
		"""
		self.is_active = False
		self.save()
































































