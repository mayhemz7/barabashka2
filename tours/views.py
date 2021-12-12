from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError


def main_view(request):
    return render(request, 'index.html')


def departure_view(request, departure):
    return render(request, 'departure.html')


def tour_view(request, id):
    return render(request, 'tour.html')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Брысь отсюда')


def custom_handler500(request):
    return HttpResponseServerError('Моя-Твоя connection lost')
