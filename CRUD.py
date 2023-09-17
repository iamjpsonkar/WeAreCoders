from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Userdb



engine=create_engine('sqlite:///userdb.db')

Base.metadata.bind=engine

DBSession= sessionmaker(bind=engine)

session= DBSession()




'''

#CRUD Create

print(session.query(MenuItem).all())

print(session.query(Restaurant).all())

myfirstrestaurant= Restaurant(name="Pizza Palace")

session.add(myfirstrestaurant)

session.commit()

print(session.query(Restaurant).all())

cheesepizza= MenuItem(name="Cheese Pizza", description="Made with all natural ingredients and fresh mozzarella", course="Entree",price="$8.99",restaurant=myfirstrestaurant)

session.add(cheesepizza)

session.commit()

print(session.query(MenuItem).all())

'''


'''
#CRUD Read

firstresult= session.query(Restaurant).first()
print(firstresult)

item=session.query(Restaurant).all()
for i in item:
    print(i.name,end=" ")
print()

'''


'''
#CRUD Update

result= session.query(Userdb).all()
for col in result:
    print(col.prflpic)

firstresult.name="New Pizza Palace"
session.add(firstresult)
session.commit()
firstresult= session.query(Restaurant).first()
print(firstresult.name)
'''


'''
#CRUD Delete
firstresult= session.query(Userdb).filter_by(rno=1604310004).first()
session.delete(firstresult)
session.commit()


'''



