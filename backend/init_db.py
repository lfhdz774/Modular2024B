import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from project import app, db
from project.models import Role, UserModel
from bcrypt import hashpw, gensalt


def create_default_roles():
    # Roles básicos
    user_role = Role(name='usuario', description='Solicitar y gestionar accesos.')
    approver_role = Role(name='aprobador', description='Aprobar o rechazar solicitudes de acceso.')

    # Roles administrativos

    super_user_role = Role(name='superusuario', description='Acceso total y sin restricciones.')
    admin_role = Role(name='administrador', description='Administrar roles, usuarios y conexiones.')
    connection_admin_role = Role(name='administrador_conexiones', description='Gestionar las conexiones a servidores y VMs.')

    # Roles adicionales (opcionales)

    auditor_role = Role(name='auditor', description='Auditar el historial de accesos y solicitudes.')
    support_role = Role(name='soporte', description='Asistir a los usuarios con la aplicación.')

    db.session.add_all([admin_role, user_role, approver_role, connection_admin_role, auditor_role, support_role, super_user_role])
    db.session.commit()

def create_superuser():
    password_hash = hashpw(b'password', gensalt())  # Encripta la contraseña

    new_user = UserModel(username='admin', password=password_hash, role_id=7, employee_code='0000', email="", first_name='Super', last_name='User', requester_id=0, approver_id=0)
    db.session.add(new_user)
    db.session.commit()



if __name__ == '__main__':
    app.app_context().push()
    #create_default_roles()
    create_superuser()