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
    from .models import Curso, Sede

    if sender.name == "gakusei":
        # Cursos
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

        # Sedes
        _, altamira_created = Sede.objects.get_or_create(nombre="Altamira", ubicacion="---", contacto="Teléfono: 0424-2668068")
        _, aruflo_created   = Sede.objects.get_or_create(nombre="Aruflo",   ubicacion="---", contacto="Teléfono: 0424-2668068")
        _, online_created   = Sede.objects.get_or_create(nombre="Online",   ubicacion="---", contacto="Teléfono: 0424-2668068")

        print('Sede "Altamira" creado') if altamira_created else print('Sede "Altamira" ya existe')
        print('Sede "Aruflo" creado')   if aruflo_created   else print('Sede "Aruflo" ya existe')
        print('Sede "Online" creado')   if online_created   else print('Sede "Online" ya existe')



@receiver(post_migrate, dispatch_uid="gakusei_default_sensei")
def default_sensei(sender, **kwargs):
    from .models import Persona, Sensei
    from django.db import transaction

    if sender.name == "gakusei":

        # Gabriel Machado
        try:
            with transaction.atomic():
                personal_data = Persona.objects.create(
                    nacionalidad=Persona.NACIONALITIES.VEN,
                    cedula="001",
                    first_name="Gabriel",
                    last_name_1="Machado",
                    personal_email="gabriel@email.com",
                    telefono="0424-0000000",
                )
                personal_data.save()

                sensei = Sensei.objects.create(
                    personal_data = personal_data,
                    institucional_email = "gabriel@zengaku.com",
                    # EN_level = Sensei.EN_Levels.C1,
                    # JP_level = Sensei.JP_Levels.N1,
                    # status   = Sensei.Status.ACTIVO,
                )
                sensei.save()
                
            print('Sensei "Gabriel Machado" registrado.')
            
        except:
            print('Sensei "Gabriel Machado" ya registrado.')

        
        # Thony Duque
        try:
            with transaction.atomic():
                personal_data = Persona.objects.create(
                    nacionalidad=Persona.NACIONALITIES.VEN,
                    cedula="002",
                    first_name="Thony",
                    last_name_1="Duque",
                    personal_email="thony@email.com",
                    telefono="0424-0000000",
                )
                personal_data.save()

                sensei = Sensei.objects.create(
                    personal_data = personal_data,
                    institucional_email = "thony@zengaku.com",
                    # EN_level = Sensei.EN_Levels.C1,
                    # JP_level = Sensei.JP_Levels.N1,
                    # status   = Sensei.Status.ACTIVO,
                )
                sensei.save()
                
            print('Sensei "Thony Duque" registrado.')
            
        except:
            print('Sensei "Thony Duque" ya registrado.')


        # Irina Indriago
        try:
            with transaction.atomic():
                personal_data = Persona.objects.create(
                    nacionalidad=Persona.NACIONALITIES.VEN,
                    cedula="003",
                    first_name="Irina",
                    last_name_1="Indriago",
                    personal_email="irina@email.com",
                    telefono="0424-0000000",
                )
                personal_data.save()

                sensei = Sensei.objects.create(
                    personal_data = personal_data,
                    institucional_email = "irina@zengaku.com",
                    # EN_level = Sensei.EN_Levels.C1,
                    # JP_level = Sensei.JP_Levels.N1,
                    # status   = Sensei.Status.ACTIVO,
                )
                sensei.save()
                
            print('Sensei "Irina Indriago" registrado.')
            
        except:
            print('Sensei "Irina Indriago" ya registrado.')

        
