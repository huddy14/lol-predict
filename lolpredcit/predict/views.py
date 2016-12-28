import matplotlib.pyplot as plt
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from utils.naive_bayes import bayes, Data
from utils.service import RiotService, ServiceException
from utils.service import regions
from utils.charts import accuracy_chart, split_chart


# Create your views here.

def home(request):
    return render(request, 'predict/home.html', {'regions': regions})


def about(request):
    clf = bayes[Data.DEFAULT]
    return render(request, 'predict/about.html',
                  {
                      'regions': regions,
                      'total': clf.total_size,
                      'training': clf.training_size,
                      'test': clf.test_size,
                      'accuracy': clf.score
                  })


def search(request):
    if request.method == 'GET':
        # return render(request, 'predict/loading.html')
        try:
            api = RiotService(request.GET['region'])
            summoner_id = api.get_summoner_id(request.GET['summoner'])
            current_match = api.get_current_game(summoner_id)
        except ServiceException as e:
            return render(request, 'predict/error.html', {'message': str(e), 'regions': regions})
        data = api.get_data_from_current_match(current_match)
        predict = data['data']
        players = data['players']
        red = []
        blue = []

        clf = bayes[Data.DEFAULT].clf

        probability = clf.predict_proba(predict)[0]
        probability[0] = round(probability[0] * 100, 2)
        probability[1] = round(probability[1] * 100, 2)

        for player in players:
            if player.team == 200:
                red.append(player)
            elif player.team == 100:
                blue.append(player)
        return render(request, 'predict/search.html',
                      {'name': request.GET['summoner'], 'region': request.GET['region'], 'regions': regions, 'red': red,
                       'blue': blue, 'prediction': probability})

    return render(request, 'predict/error.html',
                  {'message': 'Something went wrong. Please try again in a minute', 'regions': regions})


def statistics(request):
    return render(request, 'predict/statistics.html', {'regions': regions, 'graphs': [split_chart(), accuracy_chart()]})


def accuracy_grid(request):
    chart = plt.bar(np.arange(3), [10, 20, 30, 40, 50, 60], 0.35, color='r')
    canvas = FigureCanvas(chart)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
