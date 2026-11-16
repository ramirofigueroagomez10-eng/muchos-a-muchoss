from pydantic import BaseModel, ConfigDict


class CreacionAlumno(BaseModel):
    nombre: str
    email: str


class RespuestaAlumno(BaseModel):
    id: int
    nombre: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class CreacionMateria(BaseModel):
    nombre: str
    profesor: str


class RespuestaMateria(BaseModel):
    id: int
    nombre: str
    profesor: str

    model_config = ConfigDict(from_attributes=True)


class CreacionAlumnoMateria(BaseModel):
    alumno_id: int
    materia_id: int


class RespuestaAlumnoMateria(BaseModel):
    id: int
    alumno_id: int
    materia_id: int

    model_config = ConfigDict(from_attributes=True)
