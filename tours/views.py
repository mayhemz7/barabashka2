import random

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views import View

from tours import data


class MainView(View):
    def get(self, request):
        random_tour_ids = random.sample(range(1, len(data.tours)), 6)
        tours = {tour_id: data.tours[tour_id] for tour_id in random_tour_ids}
        return render(
            request, 'index.html', context={'title': data.title,
                                            'subtitle': data.subtitle,
                                            'description': data.description,
                                            'tours': tours,
                                            'departures': data.departures}
        )


class DepartureView(View):
    def get(self, request, departure):
        if departure not in data.departures:
            raise Http404

        current_departure_dict = {
            k: v for k, v in data.tours.items() if v['departure'] == departure}
        min_price = min(current_departure_dict.values(),
                        key=lambda x: x['price'])['price']
        max_price = max(current_departure_dict.values(),
                        key=lambda x: x['price'])['price']
        min_nights = min(current_departure_dict.values(),
                         key=lambda x: x['nights'])['nights']
        max_nights = max(current_departure_dict.values(),
                         key=lambda x: x['nights'])['nights']
        return render(
            request, 'departure.html',
            context={'departures': data.departures,
                     'city_from': data.departures[departure].split()[1],
                     'min_price': min_price,
                     'max_price': max_price,
                     'min_nights': min_nights,
                     'max_nights': max_nights,
                     'tours': current_departure_dict,
                     'title': data.title}
        )


class TourView(View):
    def get(self, request, id):
        if id not in data.tours:
            raise Http404

        return render(
            request, 'tour.html',
            context={'tour': data.tours[id],
                     'city_from': data.departures[data.tours[id]['departure']],
                     'departures': data.departures,
                     'title': data.tours[id]['title'] + ' ' + data.tours[id]['stars'] + '★'}
        )


def custom_handler404(request, exception):
    return HttpResponseNotFound('Брысь отсюда')


def custom_handler500(request):
    return HttpResponseServerError('Моя-Твоя connection lost')
