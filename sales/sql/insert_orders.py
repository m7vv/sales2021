from sales.models.orders import Order
from sales.models.workers import Worker
from sales.models.foods import Food

from sales import create_app

app = create_app()


def populate_orders():
    """helper to add orders to project database"""
    worker1 = Worker(name='Kozlov', salary=3456)
    food1 = Food(name='Cheese cake', price=4500)
    order1 = Order(
        worker=worker1,
        food=food1,
        quantity=5,
    )
    order2 = Order(
        worker=Worker(name='Meresiev', salary=5800),
        food=Food(name='Pan Cake', price=4600),
        quantity= 2,
    )
    worker3 = Worker(name='Raduniza', salary=6800)
    food3 = Food(name='Pie with banana', price=5500)
    order3 = Order(
        worker=worker1,
        food=food3,
        quantity=2,
    )
    order4 = Order(
        worker=worker3,
        food=food3,
        quantity=2,
    )


    with app.app_context():
        from sales.models import db

        db.session.add(order1)
        db.session.add(order2)
        db.session.add(order3)
        db.session.add(order4)

        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    print('Adding orders into  db...')
    populate_orders()
    print('Successfully populated!')
