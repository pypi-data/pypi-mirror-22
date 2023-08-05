from functools import wraps
from .definitions import OHM2HandlersLightInputException
import inspect

def ohm2_handlers_light_safe_request(func):

	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
		except Exception as e:
			frm = inspect.trace()[-1]

			ins_filename = frm[1]
			ins_lineno = frm[2]
			ins_function = frm[3]

			if hasattr(e, "code"):
				code = e.code
			else:
				code = -1	

			
			if hasattr(e, "message"):
				message = e.message
				extra = ""
			else:
				message = "Uncaught exception"
				extra = "Uncaught exception: {0}".format(e)

			return (None, OHM2HandlersLightInputException(code, message, ins_filename, ins_lineno, ins_function, extra = extra))
		else:
			return (result, None)

	return wrapper