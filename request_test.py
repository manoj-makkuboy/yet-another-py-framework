from router import Router
from webob import Request
import pdb

hello_world = Router()
hello_world.add_route('/{number:[0-9]}', 'controller:hello_0')

req = Request.blank('/7')
resp = req.get_response(hello_world)
print(resp)
