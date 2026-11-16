from fastapi import FastAPI, HTTPException, status

from database import Alumno, Materia, AlumnoMateria, db_session
from schema import (
    CreacionAlumno,
    CreacionMateria,
    CreacionAlumnoMateria,
    RespuestaAlumno,
    RespuestaMateria,
    RespuestaAlumnoMateria,
)

app = FastAPI()


@app.middleware("http")
def cerrar_sesion_bd(request, call_next):
    try:
        return call_next(request)
    finally:
        db_session.remove()


# ---------------- ALUMNOS ----------------

@app.get("/alumnos", response_model=list[RespuestaAlumno])
def obtener_alumnos():
    try:
        return Alumno.query.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los alumnos: {e}",
        )


@app.get("/alumnos/{alumno_id}", response_model=RespuestaAlumno)
def obtener_alumno(alumno_id: int):
    try:
        alumno = Alumno.query.get(alumno_id)

        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado",
            )

        return alumno
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el alumno: {e}",
        )


@app.post(
    "/alumnos",
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaAlumno,
)
def crear_alumno(alumno_data: CreacionAlumno):
    try:
        alumno = Alumno(
            nombre=alumno_data.nombre,
            email=alumno_data.email
        )

        db_session.add(alumno)
        db_session.commit()
        db_session.refresh(alumno)

        return alumno
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el alumno: {e}",
        )


# ---------------- MATERIAS ----------------

@app.get("/materias", response_model=list[RespuestaMateria])
def obtener_materias():
    try:
        return Materia.query.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las materias: {e}",
        )


@app.get("/materias/{materia_id}", response_model=RespuestaMateria)
def obtener_materia(materia_id: int):
    try:
        materia = Materia.query.get(materia_id)

        if not materia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Materia no encontrada",
            )

        return materia
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la materia: {e}",
        )


@app.post(
    "/materias",
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaMateria,
)
def crear_materia(materia_data: CreacionMateria):
    try:
        materia = Materia(
            nombre=materia_data.nombre,
            profesor=materia_data.profesor
        )

        db_session.add(materia)
        db_session.commit()
        db_session.refresh(materia)

        return materia
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la materia: {e}",
        )


# ---------------- RELACION MUCHOS A MUCHOS ----------------

# INSCRIBIR ALUMNO EN MATERIA
@app.post(
    "/alumnos-materias",
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaAlumnoMateria,
)
def inscribir_alumno(datos: CreacionAlumnoMateria):
    try:
        alumno = Alumno.query.get(datos.alumno_id)

        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado",
            )

        materia = Materia.query.get(datos.materia_id)

        if not materia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Materia no encontrada",
            )

        relacion_existente = AlumnoMateria.query.filter_by(
            alumno_id=datos.alumno_id,
            materia_id=datos.materia_id
        ).first()

        if relacion_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El alumno ya está inscripto en esta materia",
            )

        relacion = AlumnoMateria(
            alumno_id=datos.alumno_id,
            materia_id=datos.materia_id
        )

        db_session.add(relacion)
        db_session.commit()
        db_session.refresh(relacion)

        return relacion

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al inscribir al alumno: {e}",
        )


# OBTENER LAS MATERIAS DE UN ALUMNO
@app.get(
    "/alumnos/{alumno_id}/materias",
    response_model=list[RespuestaAlumnoMateria],
)
def obtener_materias_alumno(alumno_id: int):
    try:
        alumno = Alumno.query.get(alumno_id)

        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado",
            )

        relaciones = AlumnoMateria.query.filter_by(
            alumno_id=alumno_id
        ).all()

        return relaciones

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las materias del alumno: {e}",
        )


# OBTENER LOS ALUMNOS DE UNA MATERIA
@app.get(
    "/materias/{materia_id}/alumnos",
    response_model=list[RespuestaAlumnoMateria],
)
def obtener_alumnos_materia(materia_id: int):
    try:
        materia = Materia.query.get(materia_id)

        if not materia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Materia no encontrada",
            )

        relaciones = AlumnoMateria.query.filter_by(
            materia_id=materia_id
        ).all()

        return relaciones

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los alumnos de la materia: {e}",
        )


# ELIMINAR UNA INSCRIPCION
@app.delete("/alumnos-materias/{relacion_id}")
def eliminar_inscripcion(relacion_id: int):
    try:
        relacion = AlumnoMateria.query.get(relacion_id)

        if not relacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inscripcion no encontrada",
            )

        db_session.delete(relacion)
        db_session.commit()

        return {"mensaje": "Inscripcion eliminada"}

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la inscripcion: {e}",
        )
