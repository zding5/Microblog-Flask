from threading import Thread
# For asynchronous calls !!!

def async(f):
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		# Look up ... !!!
		# target is the callabe object(func), and args is the args passed to the callable.

		thr.start()
		# Make the thread alive.
	return wrapper

# How a decorator works: ... !!!