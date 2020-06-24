# chart/migrations/0002_auto_popuate.py
"""
DB 현행화 작업이 실행될 때, csv 파일 자료를 DB에 자동적으로 적재한다.
"""
import csv
import os
from django.db import migrations
from django.conf import settings

# csv 파일의 해당 열 번호를 상수로 정의(열 이름)
TICKET_CLASS = 0  # 승차권 등급
SURVIVED = 1  # 생존 여부
NAME = 2  # 이름
SEX = 3  # 성별
AGE = 4  # 나이
EMBARKED = 10  # 탑승지


def add_passengers(apps, schema_editor):
    Passenger = apps.get_model('chart', 'Passenger')  # (app_label, model_name)
    csv_file = os.path.join(settings.BASE_DIR, 'titanic.csv')
    with open(csv_file) as dataset:  # 파일 객체 dataset
        reader = csv.reader(dataset)  # 파일 객체 dataset에 대한 판독기 획득
        next(reader)  # ignore first row (headers)      # __next__() 호출 때마다 한 라인 판독
        for entry in reader:  # 판독기에 대하여 반복 처리
            Passenger.objects.create(  # DB 행 생성
                name=entry[NAME],
                sex='M' if entry[SEX] == 'male' else 'F',
                survived=bool(int(entry[SURVIVED])),  # int()로 변환하고, 다시 bool()로 변환
                age=float(entry[AGE]) if entry[AGE] else 0.0,
                ticket_class=int(entry[TICKET_CLASS]),  # int()로 변환
                embarked=entry[EMBARKED],
            )


class Migration(migrations.Migration):
    dependencies = [  # 선행 관계
        ('chart', '0001_initial'),  # app_label, preceding migration file
    ]
    operations = [  # 작업
        migrations.RunPython(add_passengers),  # add_passengers 함수를 호출
    ]