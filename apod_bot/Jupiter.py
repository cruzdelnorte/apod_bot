#importamos librerias
from astropy import units as u
from astropy.time import Time,TimeDelta
from astropy.coordinates import solar_system_ephemeris, EarthLocation, AltAz,Angle
from astropy.coordinates import get_body_barycentric, get_body, get_moon

#inicalizamos variables
AACN = EarthLocation(lat='40d32m18.8s', lon='-3d37m56.4s',height=700*u.m)
40.53857421147425, -3.632167609129196
loc = AACN
transito_inicial = Time("2021-09-18 00:18:00")
t = Time.now()

contador = Time(transito_inicial)
intervalo_transitos = TimeDelta(35740,format='sec')

with solar_system_ephemeris.set('builtin'):jup = get_body('jupiter', contador, loc)
with solar_system_ephemeris.set('builtin'):sun = get_body('sun', contador, loc)

#buscamos el próximo transito con la condición de que Jupiter este sobre el horizonte y sol bajo el horizonte
while contador < t:
    contador = contador + intervalo_transitos
    jup = get_body('jupiter', contador, loc)
    sun = get_body('sun', contador, loc)
    jup_alt = jup.transform_to(AltAz(obstime=contador,location=loc))
    sun_alt = sun.transform_to(AltAz(obstime=contador,location=loc))

while jup_alt.alt < Angle('0d') and sun_alt.alt > Angle('0d'):
    contador = contador + intervalo_transitos
    jup = get_body('jupiter', contador, loc)
    sun = get_body('sun', contador, loc)
    jup_alt = jup.transform_to(AltAz(obstime=contador,location=loc))

print ("Próximo tránsito GMR:",contador, "UT.", "con Jupiter sobre horizonte:",jup_alt.alt)