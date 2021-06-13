from sales.models.foods import Food
from sales import create_app

app = create_app()


def populate_foods():
    """helper to add foods to project database"""
    hamburger = Food(
        name='Hamburger',
        price=2000,
    )
    pancake_milk = Food(
        name='Pancake with milk',
        price=1000,
    )
    pancake_apples = Food(
        name='Pancake with apples',
        price=1500,
    )

    with app.app_context():
        from sales.models import db
        db.session.add(hamburger)
        db.session.add(pancake_milk)
        db.session.add(pancake_apples)

        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    print('Adding food into  db...')
    populate_foods()
    print('Successfully populated!')
