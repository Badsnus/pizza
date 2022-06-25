import json

from django.shortcuts import HttpResponse, get_object_or_404, render

from pizza.settings import bot, telegram_chat_id
from .models import Pizzas


def add_pizzas(request):
    pizzas_to_add = json.loads(open('pizzas_to_add.json', encoding='utf-8').read())['pizzas']
    pizzas_add = {'pizzas': []}
    for pizza in pizzas_to_add:
        pizza_item = Pizzas.objects.filter(id=pizza['id'])
        if len(pizza_item) == 0:
            if type(pizza['price']) == list:
                if len(pizza['price']) == 2:
                    prices = [i for i in pizza['price'][0] + pizza['price'][1]]
                    if len(prices) == len(pizza['types']) * 3:
                        min_price = min([i for i in pizza['price'][0] + pizza['price'][1] if i > 0])
                        Pizzas.objects.create(id=pizza['id'], pizza=pizza, min_price=min_price)
                        pizzas_add['pizzas'].append({'id': pizza['id'], 'status': 'added'})
                        continue
            pizzas_add['pizzas'].append({'id': pizza['id'], 'status': 'invalid price'})
        else:
            pizza_item = pizza_item[0]
            if type(pizza['price']) == list:
                if len(pizza['price']) == 2:
                    prices = [i for i in pizza['price'][0] + pizza['price'][1]]
                    if len(prices) == len(pizza['types']) * 3:
                        pizza_item.pizza = pizza
                        min_price = min(
                            [i for i in pizza_item.pizza['price'][0] + pizza_item.pizza['price'][1] if i > 0])
                        pizza_item.min_price = min_price
                        pizza_item.save()
                        pizzas_add['pizzas'].append({'id': pizza['id'], 'status': 'updated'})
                        continue
            pizzas_add['pizzas'].append({'id': pizza['id'], 'status': 'invalid price'})

    return HttpResponse(json.dumps(pizzas_add))


def show_pizzas_list(request):
    if request.method == "GET":
        pizzas = Pizzas.objects.all()
        all_pizzas_json = {'pizzas': []}
        min_prices = []
        for pizza in pizzas:
            all_pizzas_json['pizzas'].append(pizza.pizza)
            min_prices.append({'pizza': pizza.pizza, 'min_price': pizza.min_price})
        if 'sort' not in request.GET.keys():
            sort = 'rating'
        else:
            sort = request.GET.get('sort')
            if sort not in ['rating', 'min_price', 'name']:
                sort = 'rating'
        pizzas_json = {'pizzas': []}
        if 'category' in request.GET.keys():
            for pizza in all_pizzas_json['pizzas']:
                if str(pizza['category']) == request.GET.get('category'):
                    pizzas_json['pizzas'].append(pizza)
        else:
            pizzas_json = all_pizzas_json
        if sort != 'min_price':
            pizzas_json['pizzas'] = sorted(pizzas_json['pizzas'], key=lambda x: x[sort])
        else:
            min_prices = sorted(min_prices, key=lambda x: x['min_price'])
            pizzas_json = {'pizzas': []}
            for pizza in min_prices:
                pizzas_json['pizzas'].append(pizza['pizza'])
        return HttpResponse(json.dumps(pizzas_json, ensure_ascii=False))
    return HttpResponse(status=400)


def add_order(request):
    if request.method == 'GET':
        if 'cart' in request.GET.keys() and 'address' in request.GET.keys():
            sizes = [26, 30, 40]
            cart = request.GET.get('cart').split(',')
            address = request.GET.get('address')
            pizzas_text = 'Новый заказ:\n'
            total_price = 0
            total_count = 0
            for item in cart:
                pizza_id, pizza_type, pizza_size, count = [int(i) for i in item.split('_')]
                pizza = get_object_or_404(Pizzas, id=pizza_id)
                pizza_name = pizza.pizza['name']
                pizza_price = pizza.pizza['price'][pizza_type][sizes.index(pizza_size)]
                pizzas_text += ('➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                f'{cart.index(item) + 1}.{pizza_name}\n'
                                f'Тип пиццы: {pizza_type}\n'
                                f'Размер пиццы: {pizza_size} см\n'
                                f'Цена: {pizza_price}\n'
                                f'Количество: {count}\n')
                total_price += pizza_price * count
                total_count += count
            pizzas_text += f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n' \
                           f'Адрес: {address}\n' \
                           f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n' \
                           f'Всего пиц: {total_count}\n' \
                           f'Общая стоимость: {total_price}'
            bot.send_message(telegram_chat_id, text=pizzas_text)

            return HttpResponse("OK")
    return HttpResponse(status=400)


def index(request):
    return render(request, 'index.html', {})
