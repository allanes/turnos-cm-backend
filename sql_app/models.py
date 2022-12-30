from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
    
    
class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    telefono = Column(String)
    
    # turnos = relationship("Turno", back_populates="paciente")
    
    
class Medico(Base):
    __tablename__ = 'medicos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    telefono = Column(String)
    especialidad = Column(String)
    
    
class Recepcionista(Base):
    __tablename__ = 'recepcionistas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    telefono = Column(String)
    
    
class Consultorio(Base):
    __tablename__ = 'consultorios'
    
    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    sala = Column(Integer)
    descripcion = Column(String)
    estado = Column(String)
    
    
class Turno(Base):
    __tablename__ = 'turnos'
    
    id = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'))
    id_medico = Column(Integer, ForeignKey('medicos.id'))
    motivo_consulta = Column(String)
    fecha = Column(DateTime)
    estado = Column(String)
    
    # paciente = relationship("Paciente", back_populates="turnos")
    # medico = relationship("Medico", back_populates="turnos")

