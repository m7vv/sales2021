from sales.models.orders import Order
from sales.models.workers import Worker
from sales.models.foods import Food

from sales import create_app

app = create_app()

with app.app_context():
    res_all = Order.query.all()
    # for m in res_all:
    #     print(m)
    #     print(m.food.name)
    #     print(m.food.id)
    all_food = Food.query.all()
    for f in all_food:
        print(f)
    res_1 = Order.query.group_by(Order.food_id).count()
    print(res_1)
