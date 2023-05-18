from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from .database import Base
    
    
class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    nombre = Column(String)
    apellido = Column(String)
    fecha_nacimiento = Column(DateTime, default=lambda:datetime.now())
    email = Column(String)
    telefono = Column(String)
    
    turnos = relationship('Turno', back_populates='paciente')
    

class Recepcionista(Base):
    __tablename__ = 'recepcionistas'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    telefono = Column(String)
    

class Medico(Base):
    __tablename__ = 'medicos'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    telefono = Column(String)
    especialidad = Column(String)
    activo = Column(Boolean, default=True)
    
    turnos = relationship('Turno', back_populates='medico')
    
    
class Consultorio(Base):
    __tablename__ = 'consultorios'
    
    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    sala = Column(Integer)
    

class RegistroConsultorios(Base):
    __tablename__ = 'registro_consultorios'
    
    id = Column(Integer, primary_key=True)
    id_consultorio = Column(Integer, ForeignKey('consultorios.id'))
    id_medico = Column(Integer, ForeignKey('medicos.id'))
    fecha = Column(DateTime, default=lambda: datetime.now())
    
    
class Turno(Base):
    __tablename__ = 'turnos'
    
    id = Column(Integer, primary_key=True)
    nro_orden = Column(Integer)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'))
    id_medico = Column(Integer, ForeignKey('medicos.id'))
    motivo_consulta = Column(String)
    fecha = Column(DateTime, default=lambda: datetime.now())
    pendiente = Column(Boolean, default=True)
    
    paciente = relationship(Paciente, back_populates='turnos')
    medico = relationship(Medico, back_populates='turnos')
