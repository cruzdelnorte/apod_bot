from dataclasses import dataclass
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u


@dataclass
class Sitio:
    """
    Objeto que representa un sitio de observación. Contiene métodos para trabakjar en astropy y cambiar de hora local a universal.
    """
    nombre: str
    latitud: float
    longitud: float
    altitud: float
    utc_offset: float
    dst: bool

    def location(self):
        return EarthLocation(lat=self.latitud * u.deg, lon=self.longitud * u.deg, height=self.altitud * u.m)

    def utcoffset(self):
        return self.utc_offset * u.hour

    def resumen(self):
        texto = f'El sitio de observación {self.nombre}, de  coordenadas {self.latitud} y {self.longitud} y situado a \
                {self.altitud} m sobre el nivel del mar tiene una diferencia horaria de {self.utc_offset} horas '
        return texto

    def to_local_time(self, hora_universal):
        return Time(hora_universal) + self.utcoffset() + float(self.dst) * u.hour

    def to_universal_time(self, hora_local):
        return Time(hora_local) - self.utcoffset() - float(self.dst) * u.hour
