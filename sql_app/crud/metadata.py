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
    {'numero': 6, 'sala': 2},    
    {'numero': 7, 'sala': 2},    
    {'numero': 8, 'sala': 2},    
    {'numero': 9, 'sala': 2},    
    {'numero': 10, 'sala': 2},
]

medicos__ejemplo = [    
    {'id': 10000000, 'nombre': 'Juan', 'apellido': 'Pérez', 'email': 'juan@gmail.com', 'telefono': '111-222-333', 'especialidad': 'Cardiología'},
    {'id': 10000001, 'nombre': 'Ana', 'apellido': 'Sarasa', 'email': 'ana@gmail.com', 'telefono': '111-222-336', 'especialidad': 'Dermatología'},
    {'id': 10000002, 'nombre': 'Roberto', 'apellido': 'Garcia', 'email': 'roberto@gmail.com', 'telefono': '111-222-337', 'especialidad': 'Traumatología'},
    {'id': 10000003, 'nombre': 'Mario', 'apellido': 'Lopez', 'email': 'mario@gmail.com', 'telefono': '111-222-338', 'especialidad': 'Psiquiatría'},
    {'id': 10000004, 'nombre': 'Julia', 'apellido': 'Rodriguez', 'email': 'julia@gmail.com', 'telefono': '111-222-339', 'especialidad': 'Pediatría'},
    {'id': 10000005, 'nombre': 'Fernando', 'apellido': 'Gomez', 'email': 'fernando@gmail.com', 'telefono': '111-222-340', 'especialidad': 'Oncología'},
    {'id': 10000006, 'nombre': 'Cecilia', 'apellido': 'Diaz', 'email': 'cecilia@gmail.com', 'telefono': '111-222-341', 'especialidad': 'Neurología'},
    {'id': 10000007, 'nombre': 'Maria', 'apellido': 'Bencev', 'email': 'maria@gmail.com', 'telefono': '111-222-338', 'especialidad': 'Psiquiatría'},
    {'id': 10000008, 'nombre': 'Pablo', 'apellido': 'Martínez', 'email': 'pablo@gmail.com', 'telefono': '111-222-335', 'especialidad': 'Oftalmología'},
    {'id': 10000009, 'nombre': 'Laura', 'apellido': 'González', 'email': 'laura@gmail.com', 'telefono': '111-222-334', 'especialidad': 'Ginecología'},
]

paciente__ejemplo = {
    'id': 20000000, 'nombre': 'Paciente ', 'apellido': 'Apellido', 'fecha_nacimiento': datetime.date(1992,2,21), 'email': 'maria@gmail.com', 'telefono': '111-222-445'
}

pacientes__ejemplo = []
for index in range(50):
    paciente_nuevo = paciente__ejemplo.copy()
    paciente_nuevo['id'] = paciente_nuevo['id'] + index
    paciente_nuevo['nombre'] = paciente_nuevo['nombre'] + str(index + 1)
    pacientes__ejemplo.append(paciente_nuevo)


recepcionistas__ejemplo = [
    {'id': 34567890, 'nombre': 'María', 'apellido': 'García', 'email': 'maria@gmail.com', 'telefono': '111-222-555'},
    {'id': 45678901, 'nombre': 'Juan', 'apellido': 'Pérez', 'email': 'juan@gmail.com', 'telefono': '111-222-666'},
    {'id': 56789012, 'nombre': 'Ana', 'apellido': 'Rodríguez', 'email': 'ana@gmail.com', 'telefono': '111-222-777'}
]

turnos__ejemplo = []
for idx_med in range(len(medicos__ejemplo)):
    
    turnos_por_medico = 5
    for idx_numero_turno in range(turnos_por_medico):
        idx_paciente = idx_numero_turno*(turnos_por_medico+1)
        idx_paciente = idx_med * turnos_por_medico + idx_numero_turno
        nuevo_turnos = {
            'id_medico': medicos__ejemplo[idx_med]['id'], 
            'id_paciente': pacientes__ejemplo[idx_paciente]['id'], 
            'fecha': opening_timestamp + idx_numero_turno*tiempo_turno, 
            'motivo_consulta': 'estaba con la garganta'
        },

        turnos__ejemplo.append(nuevo_turnos)


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
