from django.http import HttpResponse

def health_check_view(request):
    return HttpResponse(status=200)



