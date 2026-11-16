from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///database.db")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Alumno(Base):
    __tablename__ = "alumno"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    materias = relationship("AlumnoMateria", back_populates="alumno", cascade="all, delete-orphan")


class Materia(Base):
    __tablename__ = "materia"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    profesor = Column(String(100), nullable=False)

    alumnos = relationship("AlumnoMateria", back_populates="materia", cascade="all, delete-orphan")


class AlumnoMateria(Base):
    __tablename__ = "alumno_materia"

    id = Column(Integer, primary_key=True)
    alumno_id = Column(Integer, ForeignKey("alumno.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materia.id"), nullable=False)

    alumno = relationship("Alumno", back_populates="materias")
    materia = relationship("Materia", back_populates="alumnos")


Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
