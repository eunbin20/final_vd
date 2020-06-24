# chart/views.py
from typing import Tuple

from django.shortcuts import render
from .models import Passenger
from .models import Confirmers
from django.db.models import Count, Q
import json
from django.http import JsonResponse

from django.core.serializers.json import DjangoJSONEncoder
import urllib.request
from django.http import HttpResponse
import csv # !!
import pandas as pd  # !!
import matplotlib.pyplot as plt # !!
from matplotlib.dates import DateFormatter # !!
import matplotlib.ticker as ticker # !!
import numpy as np # 결측값 처리를 위해 추가! # !!



def summary_chart(request):
    return render(request, 'chart/summary.html')


def world_population(request):
    return render(request, 'chart/world_population.html')


def ticket_class_view_1(request):  # 방법 1
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
            survived_count=Count('ticket_class',
                                 filter=Q(survived=True)),
            not_survived_count=Count('ticket_class',
                                     filter=Q(survived=False)),
            all_count=Count('id')) \
        .order_by('ticket_class')
    return render(request, 'chart/ticket_class_1.html', {'dataset': dataset})


def ticket_class_view_2(request):  # 방법 2
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False)),
                  all_count=Count('id')) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비
    categories = list()  # for xAxis
    survived_series = list()  # for series named 'Survived'
    not_survived_series = list()  # for series named 'Not survived'
    all_count_series = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s 등석' % entry['ticket_class'])  # for xAxis
        survived_series.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])  # for series named 'Not survived'
        all_count_series.append(entry['survived_count'] / entry['all_count'] * 100)

    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'chart/ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series),
        'all_count_series': json.dumps(all_count_series)
    })


def ticket_class_view_3(request):  # 방법 3
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False)),
                  all_count=Count('id')) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    survived_series_data = list()  # for series named 'Survived'
    not_survived_series_data = list()  # for series named 'Not survived'
    all_count_series_data = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])  # for xAxis
        survived_series_data.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'
        all_count_series_data.append(entry['survived_count'] / entry['all_count'] * 100)

    survived_series = {
        'name': '생존',
        'data': survived_series_data,
        'color': 'green'
    }
    not_survived_series = {
        'name': '비생존',
        'data': not_survived_series_data,
        'color': 'red'
    }
    survival_rate = {
        'name': '생존율',
        'data': all_count_series_data,
        'color': 'skyblue',
        'marker': {'readius': 4},
        'type': 'line',
        'yAxis': 1,

    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': '좌석 등급에 따른 타이타닉 생존/비 생존 인원 및 생존율'},
        'xAxis': {'categories': categories},
        'yAxis': [{'opposite':'true', 'title':{'text':'인원'},
                   'labels':{'align':'right', 'x':-3, 'y':16, 'format':'{value}명'}},
                  {'title':{'text':'생존율'}, 'labels':{'align':'left', 'x':3, 'y':16, 'format':'{value}%'},
                    'showFirstLabel':'true'}],
        'legend': {'align':'left', 'verticalAlign':'top', 'layout':'vertical','x':120,'y':100,
                   'floating':'true'},
        'series': [survived_series, not_survived_series, survival_rate]
    }
    dump = json.dumps(chart)

    return render(request, 'chart/ticket_class_3.html', {'chart': dump})


def json_example(request):  # 접속 경로 'json-example/'에 대응하는 뷰
    return render(request, 'chart/json_example.html')


def chart_data(request):  # 접속 경로 'json-example/data/'에 대응하는 뷰
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('id')) \
        .order_by('-total')

    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]
    # port_display_name = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Number of Titanic Passengers by Embarkation Port'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(
                lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']},
                dataset))
            # 'data': [ {'name': 'Southampton', 'y': 914},
            #           {'name': 'Cherbourg', 'y': 270},
            #           {'name': 'Queenstown', 'y': 123}]
        }]
    }
    # [list(map(lambda))](https://wikidocs.net/64)

    return JsonResponse(chart)


def covid_19_view(request):  # COVID-19
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                parse_dates=['Date'])
    # df = df.to_json()
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]
    df_confirmed = df.pivot(index='Date', columns='Country', values='Confirmed')
    covid_confirmed = df_confirmed.reset_index('Date')
    countries_col = list(df_confirmed.columns)
    covid_confirmed.set_index(['Date'], inplace=True)
    covid_confirmed.columns = countries_col
    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita_confirmed = covid_confirmed.copy()
    for country in list(percapita_confirmed.columns):
        percapita_confirmed[country] = percapita_confirmed[country] / populations[country] * 100000

    france = percapita_confirmed['France']
    france = france.values.tolist()
    korea = percapita_confirmed['Korea, South']
    korea = korea.values.tolist()
    germany = percapita_confirmed['Germany']
    germany = germany.values.tolist()
    us = percapita_confirmed['US']
    us = us.values.tolist()
    uk = percapita_confirmed['United Kingdom']
    uk = uk.values.tolist()

    chart={
        'chart': {'type': 'line'},
        'title': {'text': 'COVID-19 확진자 발생율'},
        'xAxis': {'type': 'datetime'},
        'yAxis': [
            {'labels': {'format': "{value}건/백만명"},
             "title": {"text": "합계건수"}}],
        'series':[{
                  'name': '한국',
                  'data': korea
              }, {
                  'name': '영국',
                  'data': uk
              }, {
                  'name': '프랑스',
                  'data': france
              }, {
                  'name': '독일',
                  'data': germany
              }, {
                  'name': '미국',
                  'data': us
              }]}
    dump = json.dumps(chart,cls=DjangoJSONEncoder)
    return render(request, 'chart/covid19.html', {'chart': dump})


