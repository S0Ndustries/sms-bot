# first we have to import random module as this
# provides the backbone for our random string
# generator and then we have to import the string
# module.

import random
import string

# now lets see what this string module provide us.
# I wont be going into depth because the python
# documentation provides ample information.
# so lets generate a random string with 32 characters.
def randomgen():
	return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
