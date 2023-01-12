from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_cal_submit(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        return HttpResponse("<h1>Submitted</h1>")
    return HttpResponse("<h1>Failed to submit</h1>")