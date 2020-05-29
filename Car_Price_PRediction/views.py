from django.shortcuts import render, redirect
import json
import pickle
import numpy as np


def home(request):
    return render(request, 'app.html')

__Maker = None
__Engine_type = None
__Fuel_system = None
__data_columns = None
__model = None

def cal(request):
    global __data_columns
    global __Engine_type
    global __Fuel_system
    global __Maker

    with open('./artifacts/columns.json', 'r') as f:
        __data_columns = json.load(f)['data columns']
        __Engine_type = __data_columns[16:20]
        __Fuel_system = __data_columns[20:25]
        __Maker = __data_columns[25:]
    global __model
    with open('./artifacts/car_price_prediction.pickle', 'rb') as f:
        __model = pickle.load(f)

    if request.method == 'POST':
        fuel_type = request.POST.get('uifuel')
        aspiration = request.POST.get('uiasp')
        num_of_doors = int(request.POST.get('uinod'))
        body_style = request.POST.get('body_style')
        drive_wheels = request.POST.get('uidt')
        wheel_base = float(request.POST.get('wheel_base'))
        length = float(request.POST.get('length'))
        width = float(request.POST.get('width'))
        height = float(request.POST.get('height'))
        curb_weight = float(request.POST.get('curb_weight'))
        num_of_cylinders = int(request.POST.get('num_of_cylinders'))
        horsepower = int(request.POST.get('horsepower'))
        peak_rpm = int(request.POST.get('peak_rpm'))
        city_L = float(request.POST.get('city_L'))
        high_way_L = float(request.POST.get('high_way_L'))
        Maker = request.POST.get('car_brand')
        Engine_type = request.POST.get('Engine_Type')
        Fuel_system = request.POST.get('Fuel_System')

        make_index = __data_columns.index(Maker.lower())  # [0] index e ekta list ase so oitar [0] index e column value ta ase. That what we need
        Engine_type_index = __data_columns.index(Engine_type.lower())
        Fuel_system_index = __data_columns.index(Fuel_system.lower())

        if fuel_type == 'gas':
            ft = 1
        else:
            ft = 2

        if aspiration == 'std':
            asp = 1
        else:
            asp = 2

        if body_style == 'sedan':
            bds = 1
        elif body_style == 'hatchback':
            bds = 2
        elif body_style == 'wagon':
            bds = 3
        elif body_style == 'hardtop':
            bds = 4
        elif body_style == 'convertible':
            bds = 5

        if drive_wheels == 'fwd':
            dw = 1
        elif drive_wheels == '4wd':
            dw = 2
        elif drive_wheels == 'rwd':
            dw = 3


        x = np.zeros(len(__data_columns))

        x[0] = ft
        x[1] = asp
        x[2] = num_of_doors
        x[3] = bds
        x[4] = dw
        x[5] = 1
        x[6] = wheel_base
        x[7] = length
        x[8] = width
        x[9] = height
        x[10] = curb_weight
        x[11] = num_of_cylinders
        x[12] = horsepower
        x[13] = peak_rpm
        x[14] = city_L
        x[15] = high_way_L

        if make_index >= 0:
            x[make_index] = 1

        if Engine_type_index >= 0:
            x[Engine_type_index] = 1

        if Fuel_system_index >= 0:
            x[Fuel_system_index] = 1
        # print(round(__model.predict([x])[0], 2))
        foo = round(__model.predict([x])[0], 2)
        context = {'val': foo}
        return render(request, 'result.html', context)

    else:
        return redirect('/')