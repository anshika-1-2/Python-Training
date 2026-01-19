from django.http import HttpResponse
from django.template import loader

def members(request):
  """
  Returns a rendered HTML template for the members page.

  Args:
      request (django.http.request.HttpRequest): The incoming request.

  Returns:
      django.http.response.HttpResponse: The rendered HTML template.
  """
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())
