import datetime
from time import strptime
from sql_app import models

today = datetime.datetime.utcnow().date()
opening_time = datetime.time(8)
opening_timestamp = datetime.datetime.combine(today, opening_time)
tiempo_turno = datetime.timedelta(minutes=30)

fastapi_metadata = {
    'title': 'Administración de Turnos - Centro Médico Esperanza',
    # 'openapi_tags': tags_metadata,
    'swagger_ui_parameters': {
        'defaultModelsExpandDepth': 0,
        'docExpansion': 'list',
        'requestSnippetsEnabled': True,
        'tryItOutEnabled': True
    }
}

consultorios_ejemplo = [
    {'numero': 1, 'sala': 1, 'descripcion': 'Consultorio 1-1'},
    {'numero': 2, 'sala': 1, 'descripcion': 'Consultorio 2-1'},
    {'numero': 3, 'sala': 2, 'descripcion': 'Consultorio 3-2'},
    {'numero': 4, 'sala': 2, 'descripcion': 'Consultorio 4-2'},
]

medicos__ejemplo = [
    {'dni': 12345678, 'nombre': 'Juan', 'apellido': 'Pérez', 'email': 'juan@gmail.com', 'telefono': '111-222-333', 'especialidad': 'Cardiología'},
    {'dni': 12345679, 'nombre': 'Laura', 'apellido': 'González', 'email': 'laura@gmail.com', 'telefono': '111-222-334', 'especialidad': 'Ginecología'},
    {'dni': 12345680, 'nombre': 'Pablo', 'apellido': 'Martínez', 'email': 'pablo@gmail.com', 'telefono': '111-222-335', 'especialidad': 'Oftalmología'},
    {'dni': 12345683, 'nombre': 'Mario', 'apellido': 'Lopez', 'email': 'mario@gmail.com', 'telefono': '111-222-338', 'especialidad': 'Psiquiatría', 'activo': False}
]

pacientes__ejemplo = [
    {'dni': 23456789, 'nombre': 'Carlos', 'apellido': 'Sánchez', 'email': 'carlos@gmail.com', 'telefono': '111-222-444'},
    {'dni': 23456790, 'nombre': 'María', 'apellido': 'Rodríguez', 'email': 'maria@gmail.com', 'telefono': '111-222-445'},
    {'dni': 23456791, 'nombre': 'Jorge', 'apellido': 'González', 'email': 'jorge@gmail.com', 'telefono': '111-222-446'},
    {'dni': 23456792, 'nombre': 'Laura', 'apellido': 'Pérez', 'email': 'laura@gmail.com', 'telefono': '111-222-447'},
    {'dni': 23456793, 'nombre': 'Roberto', 'apellido': 'Gómez', 'email': 'roberto@gmail.com', 'telefono': '111-222-448'},
    {'dni': 23456794, 'nombre': 'Sandra', 'apellido': 'Martínez', 'email': 'sandra@gmail.com', 'telefono': '111-222-449'},
    {'dni': 23456795, 'nombre': 'Javier', 'apellido': 'Fernández', 'email': 'javier@gmail.com', 'telefono': '111-222-450'},
    {'dni': 23456796, 'nombre': 'Pablo', 'apellido': 'Muñoz', 'email': 'pablo@gmail.com', 'telefono': '111-222-451'},
]

turnos__ejemplo = [
    {'id_medico': 4, 'id_paciente': 5, 'fecha': opening_timestamp + 0*tiempo_turno, 'motivo_consulta': 'estaba con la garganta', 'pendiente': False},
    {'id_medico': 1, 'id_paciente': 1, 'fecha': opening_timestamp + 1*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
    {'id_medico': 2, 'id_paciente': 3, 'fecha': opening_timestamp + 2*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
    {'id_medico': 3, 'id_paciente': 4, 'fecha': opening_timestamp + 3*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
    {'id_medico': 3, 'id_paciente': 2, 'fecha': opening_timestamp + 4*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
    {'id_medico': 3, 'id_paciente': 1, 'fecha': opening_timestamp + 5*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
    {'id_medico': 2, 'id_paciente': 3, 'fecha': opening_timestamp + 6*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
    {'id_medico': 1, 'id_paciente': 4, 'fecha': opening_timestamp + 7*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
    {'id_medico': 2, 'id_paciente': 2, 'fecha': opening_timestamp + 8*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
]

registro_consultorios_ejemplo = [
    {'id_consultorio': 1, 'id_medico': 2, 'fecha': opening_timestamp + 0*tiempo_turno},
    {'id_consultorio': 2, 'id_medico': 4, 'fecha': opening_timestamp + 1*tiempo_turno},
    {'id_consultorio': 3, 'id_medico': 3, 'fecha': opening_timestamp + 2*tiempo_turno},
    {'id_consultorio': 4, 'id_medico': 1, 'fecha': opening_timestamp + 3*tiempo_turno},
    {'id_consultorio': 1, 'id_medico': 1, 'fecha': opening_timestamp - datetime.timedelta(days=1) + 4*tiempo_turno},
    {'id_consultorio': 2, 'id_medico': 2, 'fecha': opening_timestamp - datetime.timedelta(days=1) + 5*tiempo_turno},
    {'id_consultorio': 3, 'id_medico': 3, 'fecha': opening_timestamp - datetime.timedelta(days=1) + 6*tiempo_turno},
    {'id_consultorio': 4, 'id_medico': 4, 'fecha': opening_timestamp - datetime.timedelta(days=1) + 7*tiempo_turno},
]

# En las 2 siguientes listas, hacer rejuntar los ejemplos y sus modelos base
ejemplos = [
    consultorios_ejemplo,
    medicos__ejemplo,
    pacientes__ejemplo,
    turnos__ejemplo,
    registro_consultorios_ejemplo
]

modelos_base = [
    models.Consultorio,
    models.Medico,
    models.Paciente,
    models.Turno,
    models.RegistroConsultorios
]
