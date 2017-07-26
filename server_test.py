from webob import Request
from app import application


req = Request.blank('http://localhost/test')
resp = req.get_response(application)
