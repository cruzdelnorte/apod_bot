"""
Elementos básicos que componen un equipo astronómico.
"""


from dataclasses import dataclass


@dataclass
class Telescopio:
    """
    Representa un telescopio:

    diametro : diámetro del objetivo en mm
    focal: distancia focal del telescopio en mm
    ratio_focal

    """
    diametro_teles: float
    focal_teles: float

    def ratio_focal(self) -> float:
        return round(self.focal_teles / self.diametro_teles, 1)


@dataclass
class Ocular:
    """
     Representa un ocular:

     focal: distancia focal del ocular en mm
     campo_aparente: campo aparente del ocular en grados

     """
    focal_ocular: float
    campo_aparente_ocular: float


@dataclass
class EquipoVisual:
    """
    Representa una combinación de telescopio y ocular
    """

    telescopio: Telescopio
    ocular: Ocular

    def pupila_de_salida(self) -> float:
        return self.ocular.focal_ocular / self.telescopio.ratio_focal()

    def aumentos(self) -> float:
        return int(self.telescopio.focal_teles / self.ocular.focal_ocular)

    def fov(self) -> float:
        return round(self.ocular.campo_aparente_ocular / self.aumentos(), 2)

    def brillo(self) -> float:
        return int(2 * self.pupila_de_salida() * self.pupila_de_salida())
