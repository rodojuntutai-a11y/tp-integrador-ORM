from datetime import date
from typing import List
from sqlalchemy import String, Integer, Boolean, Float, Date, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Jugador(Base):
    __tablename__ = "jugadores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    usuario: Mapped[str] = mapped_column(String(50), unique=True)
    pais: Mapped[str] = mapped_column(String(50))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class Equipo(Base):
    __tablename__ = "equipos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    pais: Mapped[str] = mapped_column(String(50))
    fundacion: Mapped[int] = mapped_column(Integer)

    partidas_local: Mapped[List["Partida"]] = relationship(
        "Partida", foreign_keys="[Partida.equipo_local_id]", back_populates="equipo_local"
    )
    partidas_visitante: Mapped[List["Partida"]] = relationship(
        "Partida", foreign_keys="[Partida.equipo_visitante_id]", back_populates="equipo_visitante"
    )


class Torneo(Base):
    __tablename__ = "torneos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    juego: Mapped[str] = mapped_column(String(50))
    fecha_inicio: Mapped[date] = mapped_column(Date)
    premio: Mapped[float] = mapped_column(Float)

    partidas: Mapped[List["Partida"]] = relationship("Partida", back_populates="torneo")


class Partida(Base):
    __tablename__ = "partidas"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date] = mapped_column(Date)
    resultado: Mapped[str] = mapped_column(String(50))

    torneo_id: Mapped[int] = mapped_column(ForeignKey("torneos.id"))
    equipo_local_id: Mapped[int] = mapped_column(ForeignKey("equipos.id"))
    equipo_visitante_id: Mapped[int] = mapped_column(ForeignKey("equipos.id"))

    torneo: Mapped["Torneo"] = relationship("Torneo", back_populates="partidas")
    equipo_local: Mapped["Equipo"] = relationship("Equipo", foreign_keys=[equipo_local_id], back_populates="partidas_local")
    equipo_visitante: Mapped["Equipo"] = relationship("Equipo", foreign_keys=[equipo_visitante_id], back_populates="partidas_visitante")


engine = create_engine("sqlite:///esports.db", echo=True)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("\n--- ¡Base de datos y tablas creadas exitosamente! ---")    