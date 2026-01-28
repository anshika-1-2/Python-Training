from django.http import HttpResponse
from django.template import loader
from .models import Member

def members(request):
  """
  Displays all members of the club.

  :param request: The HTTP request object
  :return: An HTTP response containing the rendered HTML page
  """
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))
  
def details(request, id):
  """
  Displays the details of a member.

  :param request: The HTTP request object
  :param id: The id of the member to display
  :return: An HTTP response containing the rendered HTML page
  """
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))


def main(request):
  """
  Displays the main page of the club.

  :param request: The HTTP request object
  :return: An HTTP response containing the rendered HTML page
  """
  template = loader.get_template('main.html')
  return HttpResponse(template.render())


def testing(request):
  """
  Displays a simple HTML page with a list of fruits.

  :param request: The HTTP request object
  :return: An HTTP response containing the rendered HTML page
  """
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],   
  }
  return HttpResponse(template.render(context, request))