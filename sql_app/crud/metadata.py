import datetime
from time import strptime
from sql_app import models

today = datetime.datetime.now().date()
opening_time = datetime.time(8)
opening_timestamp = datetime.datetime.combine(today, opening_time)
tiempo_turno = datetime.timedelta(minutes=30)


consultorios_ejemplo = [
    {'numero': 1, 'sala': 1},
    {'numero': 2, 'sala': 1},
    {'numero': 3, 'sala': 1},
    {'numero': 4, 'sala': 1},
    {'numero': 5, 'sala': 1},
    {'numero': 6, 'sala': 1},    
    {'numero': 7, 'sala': 1},    
    {'numero': 8, 'sala': 1},    
    {'numero': 9, 'sala': 1},    
    {'numero': 10, 'sala': 1},
    {'numero': 11, 'sala': 2},
    {'numero': 12, 'sala': 2},
    {'numero': 13, 'sala': 2},
    {'numero': 14, 'sala': 2},
    {'numero': 15, 'sala': 2},
    {'numero': 16, 'sala': 2},    
    {'numero': 17, 'sala': 2},    
    {'numero': 18, 'sala': 2},    
    {'numero': 19, 'sala': 2},    
    {'numero': 20, 'sala': 2},
]

medicos__ejemplo = [    
    {'id': 12345678, 'nombre': 'Juan', 'apellido': 'Pérez', 'email': 'juan@gmail.com', 'telefono': '111-222-333', 'especialidad': 'Cardiología'},
    {'id': 12345679, 'nombre': 'Laura', 'apellido': 'González', 'email': 'laura@gmail.com', 'telefono': '111-222-334', 'especialidad': 'Ginecología'},
    {'id': 12345680, 'nombre': 'Pablo', 'apellido': 'Martínez', 'email': 'pablo@gmail.com', 'telefono': '111-222-335', 'especialidad': 'Oftalmología'},
    {'id': 12345683, 'nombre': 'Maria', 'apellido': 'Bencev', 'email': 'maria@gmail.com', 'telefono': '111-222-338', 'especialidad': 'Psiquiatría'},
    {'id': 12345643, 'nombre': 'Mario', 'apellido': 'Lopez', 'email': 'mario@gmail.com', 'telefono': '111-222-338', 'especialidad': 'Psiquiatría'},
    {'id': 12345681, 'nombre': 'Ana', 'apellido': 'Sarasa', 'email': 'ana@gmail.com', 'telefono': '111-222-336', 'especialidad': 'Dermatología'},
    {'id': 12345682, 'nombre': 'Roberto', 'apellido': 'Garcia', 'email': 'roberto@gmail.com', 'telefono': '111-222-337', 'especialidad': 'Traumatología'},
    {'id': 12345684, 'nombre': 'Julia', 'apellido': 'Rodriguez', 'email': 'julia@gmail.com', 'telefono': '111-222-339', 'especialidad': 'Pediatría'},
    {'id': 12345685, 'nombre': 'Fernando', 'apellido': 'Gomez', 'email': 'fernando@gmail.com', 'telefono': '111-222-340', 'especialidad': 'Oncología'},
    {'id': 12345686, 'nombre': 'Cecilia', 'apellido': 'Diaz', 'email': 'cecilia@gmail.com', 'telefono': '111-222-341', 'especialidad': 'Neurología'},
    {'id': 22345678, 'nombre': 'Juan', 'apellido': 'Pérez', 'email': 'juan@gmail.com', 'telefono': '111-222-333', 'especialidad': 'Cardiología'},
    {'id': 22345679, 'nombre': 'Laura', 'apellido': 'González', 'email': 'laura@gmail.com', 'telefono': '111-222-334', 'especialidad': 'Ginecología'},
    {'id': 22345680, 'nombre': 'Pablo', 'apellido': 'Martínez', 'email': 'pablo@gmail.com', 'telefono': '111-222-335', 'especialidad': 'Oftalmología'},
    {'id': 22345683, 'nombre': 'Maria', 'apellido': 'Bencev', 'email': 'maria@gmail.com', 'telefono': '111-222-338', 'especialidad': 'Psiquiatría'},
    {'id': 22345643, 'nombre': 'Mario', 'apellido': 'Lopez', 'email': 'mario@gmail.com', 'telefono': '111-222-338', 'especialidad': 'Psiquiatría'},
    {'id': 22345681, 'nombre': 'Ana', 'apellido': 'Sarasa', 'email': 'ana@gmail.com', 'telefono': '111-222-336', 'especialidad': 'Dermatología'},
    {'id': 22345682, 'nombre': 'Roberto', 'apellido': 'Garcia', 'email': 'roberto@gmail.com', 'telefono': '111-222-337', 'especialidad': 'Traumatología'},
    {'id': 22345684, 'nombre': 'Julia', 'apellido': 'Rodriguez', 'email': 'julia@gmail.com', 'telefono': '111-222-339', 'especialidad': 'Pediatría'},
    {'id': 22345685, 'nombre': 'Fernando', 'apellido': 'Gomez', 'email': 'fernando@gmail.com', 'telefono': '111-222-340', 'especialidad': 'Oncología'},
    {'id': 22345686, 'nombre': 'Cecilia', 'apellido': 'Diaz', 'email': 'cecilia@gmail.com', 'telefono': '111-222-341', 'especialidad': 'Neurología'}
]

pacientes__ejemplo = [
    {'id': 23456789, 'nombre': 'Carlos', 'apellido': 'Sánchez', 'fecha_nacimiento': datetime.date(1990,1,21), 'email': 'carlos@gmail.com', 'telefono': '111-222-444'},
    {'id': 23456790, 'nombre': 'María', 'apellido': 'Rodríguez', 'fecha_nacimiento': datetime.date(1992,2,21), 'email': 'maria@gmail.com', 'telefono': '111-222-445'},
    {'id': 23456791, 'nombre': 'Jorge', 'apellido': 'González', 'fecha_nacimiento': datetime.date(1990,4,23), 'email': 'jorge@gmail.com', 'telefono': '111-222-446'},
    {'id': 23456792, 'nombre': 'Laura', 'apellido': 'Pérez', 'fecha_nacimiento': datetime.date(1955,4,25), 'email': 'laura@gmail.com', 'telefono': '111-222-447'},
    {'id': 23456793, 'nombre': 'Roberto', 'apellido': 'Gómez', 'fecha_nacimiento': datetime.date(1977,8,31), 'email': 'roberto@gmail.com', 'telefono': '111-222-448'},
    {'id': 23456794, 'nombre': 'Sandra', 'apellido': 'Martínez', 'fecha_nacimiento': datetime.date(1987,12,21), 'email': 'sandra@gmail.com', 'telefono': '111-222-449'},
    {'id': 23456795, 'nombre': 'Javier', 'apellido': 'Fernández', 'fecha_nacimiento': datetime.date(1999,6,20), 'email': 'javier@gmail.com', 'telefono': '111-222-450'},
    {'id': 23456796, 'nombre': 'Pablo', 'apellido': 'Muñoz', 'fecha_nacimiento': datetime.date(1990,1,1), 'email': 'pablo@gmail.com', 'telefono': '111-222-451'},
    {'id': 23456797, 'nombre': 'Sandra', 'apellido': 'Medina', 'fecha_nacimiento': datetime.date(1987,12,21), 'email': 'sandra@gmail.com', 'telefono': '111-222-449'},
    {'id': 23456798, 'nombre': 'Javier', 'apellido': 'Rojano', 'fecha_nacimiento': datetime.date(1999,6,20), 'email': 'javier@gmail.com', 'telefono': '111-222-450'},
    {'id': 23456799, 'nombre': 'Pablo', 'apellido': 'Veliz', 'fecha_nacimiento': datetime.date(1990,1,1), 'email': 'pablo@gmail.com', 'telefono': '111-222-451'},
]

recepcionistas__ejemplo = [
    {'id': 34567890, 'nombre': 'María', 'apellido': 'García', 'email': 'maria@gmail.com', 'telefono': '111-222-555'},
    {'id': 45678901, 'nombre': 'Juan', 'apellido': 'Pérez', 'email': 'juan@gmail.com', 'telefono': '111-222-666'},
    {'id': 56789012, 'nombre': 'Ana', 'apellido': 'Rodríguez', 'email': 'ana@gmail.com', 'telefono': '111-222-777'}
]

turnos__ejemplo = []
for idx_med in range(len(medicos__ejemplo)):
    nuevos_turnos = [
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[0]['id'], 'fecha': opening_timestamp + 0*tiempo_turno, 'motivo_consulta': 'estaba con la garganta'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[1]['id'], 'fecha': opening_timestamp + 1*tiempo_turno, 'motivo_consulta': 'estaba con dolor en el pecho'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[2]['id'], 'fecha': opening_timestamp + 2*tiempo_turno, 'motivo_consulta': 'estaba con fiebre'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[3]['id'], 'fecha': opening_timestamp + 3*tiempo_turno, 'motivo_consulta': 'estaba con dolor de cabeza'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[4]['id'], 'fecha': opening_timestamp + 4*tiempo_turno, 'motivo_consulta': 'estaba con dolor de estómago'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[5]['id'], 'fecha': opening_timestamp + 5*tiempo_turno, 'motivo_consulta': 'estaba con dolor de oído'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[6]['id'], 'fecha': opening_timestamp + 6*tiempo_turno, 'motivo_consulta': 'estaba con una lesión en la rodilla'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[7]['id'], 'fecha': opening_timestamp + 7*tiempo_turno, 'motivo_consulta': 'estaba con una erupción cutánea'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[8]['id'], 'fecha': opening_timestamp + 8*tiempo_turno, 'motivo_consulta': 'estaba con dolor en el hombro'},
        {'id_medico': medicos__ejemplo[idx_med]['id'], 'id_paciente': pacientes__ejemplo[9]['id'], 'fecha': opening_timestamp + 9*tiempo_turno, 'motivo_consulta': 'estaba con dolor de espalda'},    
    ]
    turnos__ejemplo.extend(nuevos_turnos)

registro_consultorios_ejemplo = [
    {'id_consultorio': 1, 'id_medico': medicos__ejemplo[0]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 2, 'id_medico': medicos__ejemplo[1]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 3, 'id_medico': medicos__ejemplo[2]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 4, 'id_medico': medicos__ejemplo[3]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 5, 'id_medico': medicos__ejemplo[4]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 6, 'id_medico': medicos__ejemplo[5]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 7, 'id_medico': medicos__ejemplo[6]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 8, 'id_medico': medicos__ejemplo[7]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 9, 'id_medico': medicos__ejemplo[8]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 10, 'id_medico': medicos__ejemplo[9]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 11, 'id_medico': medicos__ejemplo[10]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 12, 'id_medico': medicos__ejemplo[11]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 13, 'id_medico': medicos__ejemplo[12]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 14, 'id_medico': medicos__ejemplo[13]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 15, 'id_medico': medicos__ejemplo[14]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 16, 'id_medico': medicos__ejemplo[15]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 17, 'id_medico': medicos__ejemplo[16]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 18, 'id_medico': medicos__ejemplo[17]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 19, 'id_medico': medicos__ejemplo[18]['id'], 'fecha': opening_timestamp},
    {'id_consultorio': 20, 'id_medico': medicos__ejemplo[19]['id'], 'fecha': opening_timestamp},
]

# En las 2 siguientes listas, hacer rejuntar los ejemplos y sus modelos base
ejemplos = [
    consultorios_ejemplo,
    medicos__ejemplo,
    pacientes__ejemplo,
    recepcionistas__ejemplo,
    registro_consultorios_ejemplo,
    turnos__ejemplo,
]

modelos_base = [
    models.Consultorio,
    models.Medico,
    models.Paciente,
    models.Recepcionista,
    models.RegistroConsultorios,
    models.Turno,
]
