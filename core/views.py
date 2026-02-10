from django.shortcuts import render

def webcam_detect_view(request):
    return render(request, 'core/webcam_detect.html')