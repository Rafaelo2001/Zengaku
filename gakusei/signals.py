from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate, dispatch_uid="gakusei_default_users")
def default_users(sender, **kwargs):
    from django.contrib.auth.models import User

    if sender.name == 'gakusei':

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", None, "admin")
            print('Superusuario "admin" creado.')
        else:
            print('Superusuario "admin" ya existe.')


@receiver(post_migrate, dispatch_uid="gakusei_default_data")
def default_data(sender, **kwargs):
    from .models import Curso

    if sender.name == "gakusei":
        _, n5_created = Curso.objects.get_or_create(modulo="ZGN5")
        _, n4_created = Curso.objects.get_or_create(modulo="ZGN4")
        _, n3_created = Curso.objects.get_or_create(modulo="ZGN3")
        _, n2_created = Curso.objects.get_or_create(modulo="ZGN2")
        _, n1_created = Curso.objects.get_or_create(modulo="ZGN1")

        print('Curso "N5" creado') if n5_created else print('Curso "N5" ya existe')
        print('Curso "N4" creado') if n4_created else print('Curso "N4" ya existe')
        print('Curso "N3" creado') if n3_created else print('Curso "N3" ya existe')
        print('Curso "N2" creado') if n2_created else print('Curso "N2" ya existe')
        print('Curso "N1" creado') if n1_created else print('Curso "N1" ya existe')


@receiver(post_migrate, dispatch_uid="gakusei_default_sensei")
def default_sensei(sender, **kwargs):
    from .models import Persona, Sensei
    from django.db import transaction

    if sender.name == "gakusei":
        try:
            with transaction.atomic():
                personal_data = Persona.objects.create(
                    cedula="V1234567",
                    first_name="Alfonso",
                    last_name_1="Martinez",
                    personal_email="personal@email.com",
                    telefono="0424-8267200",
                )
                personal_data.save()

                sensei = Sensei.objects.create(
                    personal_data = personal_data,
                    institucional_email = "institucional@a.com",

                    EN_level = Sensei.EN_Levels.C1,
                    JP_level = Sensei.JP_Levels.N1,
                    status   = Sensei.Status.ACTIVO,
                )
                sensei.save()
                
            print("Sensei 'Alfonoso' registrado")
            
        except:
            print("Sensei ya registrado.")
