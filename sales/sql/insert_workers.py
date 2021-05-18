from sales.models.workers import Worker
from sales import create_app

app = create_app()


def populate_workers():
    ivanov = Worker(
        name='Ivanov',
        salary=6000,
    )
    petrov = Worker(
        name='Petrov',
        salary=7000,
    )
    nazarov = Worker(
        name='Nazarov',
        salary=5500,
    )

    with app.app_context():
        from sales.models import db
        db.session.add(ivanov)
        db.session.add(petrov)
        db.session.add(nazarov)

        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    print('Adding workers into  db...')
    populate_workers()
    print('Successfully populated!')
