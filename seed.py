import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')
django.setup()

from orders.models import Company,CustomUser,Product,Order

company1, _ = Company.objects.get_or_create(name="LapComp")
company2, _ = Company.objects.get_or_create(name="Motorcar")
company3, _ = Company.objects.get_or_create(name="Drinkuo")

#__USERS__
#__USERS FOR COMPANY 1
admin_user, _ = CustomUser.objects.get_or_create(
    username="admin",
    defaults={
        "email":"admin@gmail.com",
        "role":"admin",
        "company":company1,
        "is_staff":True,
        "is_superuser":True,
    },
)
admin_user.set_password("Admin@1234")
admin_user.save()


viewer_user, _ = CustomUser.objects.get_or_create(
    username="viewer",
    defaults={
        "email":"viewer@gmail.com",
        "role":"viewer",
        "company":company1,
        "is_staff":False,
        "is_superuser":False,
    },
)
viewer_user.set_password("Viewer@1234")
viewer_user.save()

operator_user, _ = CustomUser.objects.get_or_create(
    username="operator",
    defaults={
        "email":"operator@gmail.com",
        "role":"operator",
        "company":company1,
        "is_staff":True,
        "is_superuser":False,
    },
)
operator_user.set_password("Operator@1234")
operator_user.save()


#__USERS FOR COMPANY 2
admin_user2, _ = CustomUser.objects.get_or_create(
    username="admin2",
    defaults={
        "email":"admin2@gmail.com",
        "role":"admin",
        "company":company2,
        "is_staff":True,
        "is_superuser":True,
    },
)
admin_user2.set_password("Admin2@1234")
admin_user2.save()


viewer_user2, _ = CustomUser.objects.get_or_create(
    username="viewer2",
    defaults={
        "email":"viewer2@gmail.com",
        "role":"viewer",
        "company":company2,
        "is_staff":False,
        "is_superuser":False,
    },
)
viewer_user2.set_password("Viewer2@1234")
viewer_user2.save()

operator_user2, _ = CustomUser.objects.get_or_create(
    username="operator2",
    defaults={
        "email":"operator2@gmail.com",
        "role":"operator",
        "company":company2,
        "is_staff":True,
        "is_superuser":False,
    },
)
operator_user2.set_password("Operator2@1234")
operator_user2.save()


#__USERS FOR COMPANY 3
admin_user3, _ = CustomUser.objects.get_or_create(
    username="admin3",
    defaults={
        "email":"admin3@gmail.com",
        "role":"admin",
        "company":company3,
        "is_staff":True,
        "is_superuser":True,
    },
)
admin_user3.set_password("Admin3@1234")
admin_user3.save()


viewer_user3, _ = CustomUser.objects.get_or_create(
    username="viewer3",
    defaults={
        "email":"viewer3@gmail.com",
        "role":"viewer",
        "company":company3,
        "is_staff":False,
        "is_superuser":False,
    },
)
viewer_user3.set_password("Viewer3@1234")
viewer_user3.save()

operator_user3, _ = CustomUser.objects.get_or_create(
    username="operator3",
    defaults={
        "email":"operator3@gmail.com",
        "role":"operator",
        "company":company3,
        "is_staff":True,
        "is_superuser":False,
    },
)
operator_user3.set_password("Operator3@1234")
operator_user3.save()


#Products


products = [
    #Seeding Products for Company 1
    Product(company=company1,name="Laptop1",price=1500.00,stock=10,created_by=admin_user),
    Product(company=company1,name="Laptop2",price=1600.00,stock=7,created_by=admin_user),
    Product(company=company1,name="Laptop3",price=2000.00,stock=5,created_by=admin_user),

    #Seeding Products for Company 2
    Product(company=company2,name="car1",price=2000.00,stock=5,created_by=admin_user2),
    Product(company=company2,name="car2",price=2500.00,stock=2,created_by=admin_user2),
    Product(company=company2,name="car3",price=3000.00,stock=1,created_by=admin_user2),

    #Seeding Products for Company 3
    Product(company=company3,name="Soda1",price=100.00,stock=50,created_by=admin_user3),
    Product(company=company3,name="Soda2",price=150.00,stock=30,created_by=admin_user3),
    Product(company=company3,name="Soda3",price=200.00,stock=10,created_by=admin_user3),
]
Product.objects.bulk_create(products)



print("✅ Seed data created successfully!")