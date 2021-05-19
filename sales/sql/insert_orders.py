from sales.models.orders import Order
from sales import create_app

app = create_app()


def populate_orders():

    order1 = Order(
        worker=1,
        food=2,
        quantity= 3,
    )
    order2 = Order(
        worker=1,
        food=3,
        quantity= 1,
    )
    order3 = Order(
        worker=2,
        food=3,
        quantity= 5,
    )


    with app.app_context():
        from sales.models import db
        db.session.add(order1)
        db.session.add(order2)
        db.session.add(order3)

        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    print('Adding orders into  db...')
    populate_orders()
    print('Successfully populated!')
