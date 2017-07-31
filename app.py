import controller


@controller.controller
def hello(req):
    if req.method == 'POST':
        return 'hello'
