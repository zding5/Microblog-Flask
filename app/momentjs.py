# A wrapper for momentjs
# Easy for us to change the way we render timestamps

from jinja2 import Markup

class momentjs(object):
# New-style class. Why do we need new-style class here ???
	def __init__(self, timestamp):
		self.timestamp = timestamp

	def render(self, format): # ???
		return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))
	# Markup() can prevent double escaping ???
	# Essentially, Jinja2 escapes all strings by default, so e.g <script> will arrive as &lt;script&gt; and Markup tells Jinja2 not to escape this string. !!!
	

	def format(self, fmt):
		return self.render("format(\"%s\")" % fmt)

	def calendar(self):
		return self.render("calendar()")

	def fromNow(self):
		return self.render("fromNow()")