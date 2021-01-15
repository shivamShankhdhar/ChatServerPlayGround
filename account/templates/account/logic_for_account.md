1. is_self
	1. True: You are looking at your own profile (**1**)
	2. False: Move to next
		2.1.  is_friend:
			2.1.1 - True:This is yourfriend (**2**)
			2.1.2 - False:This is not your friend
				2.1.2.1 No_REQUEST_SENT (**3**)
				2.1.2.2 THEM_SENT_TO_YOU (**4**)
				2.1.2.3 YOU_SENT_TO_THEM (**5**)
