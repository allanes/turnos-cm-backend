from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Persona(Base):
    __tablename__ = 'personas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    telefono = Column(String)
    
    
class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    id_persona = Column(Integer, ForeignKey('personas.id'))
    tipo = Column(String)
    username = Column(String)
    password = Column(String)
    
    persona = relationship("Persona")
    
    
class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    id_persona = Column(Integer, ForeignKey('personas.id'))
    
    persona = relationship("Persona")
    turnos = relationship("Turno", back_populates="paciente")
    
    
class Medico(Base):
    __tablename__ = 'medicos'
    
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    especialidad = Column(String)
    
    usuario = relationship("Usuario")
    turnos = relationship("Turno", back_populates="medico")
    
    
class Recepcionista(Base):
    __tablename__ = 'recepcionistas'
    
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    
    usuario = relationship("Usuario")
    
    
class Consultorio(Base):
    __tablename__ = 'consultorios'
    
    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    sala = Column(Integer)
    descripcion = Column(String)
    estado = Column(String)
    
    
class MedicoConsultorio(Base):
    __tablename__ = 'medicos_consultorios'
    
    id = Column(Integer, primary_key=True)
    id_medico = Column(Integer, ForeignKey('medicos.id'))
    id_consultorio = Column(Integer, ForeignKey('consultorios.id'))
    
    medico = relationship("Medico")
    consultorio = relationship("Consultorio")
    
    
class Turno(Base):
    __tablename__ = 'turnos'
    
    id = Column(Integer, primary_key=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'))
    id_medico = Column(Integer, ForeignKey('medicos.id'))
    motivo_consulta = Column(String)
    fecha = Column(DateTime)
    estado = Column(String)
    
    paciente = relationship("Paciente", back_populates="turnos")
    medico = relationship("Medico", back_populates="turnos")

