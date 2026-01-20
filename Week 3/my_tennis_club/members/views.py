from django.http import HttpResponse
from django.template import loader

def members(request):
  """
  Render the myfirst.html template.

  This view function renders the myfirst.html template.
  It takes a request object as an argument and returns
  an HttpResponse object with the rendered template.

  :param request: A request object from Django.
  :return: An HttpResponse object with the rendered template.
  """
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())
