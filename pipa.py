# ============================================================================================ #
# :::::::::::::::::::: PLANETARIUM with INTERSTELLAR POSITIONAL ASTRONOMY :::::::::::::::::::: #
# ============================================================================================ #
# ::::::::::::::::::::::::::::::::: by Fabrizio Melges Ferro ::::::::::::::::::::::::::::::::: #

import vpython as vp
import numpy as np
from skyfield.api import Star, load
from skyfield.data import hipparcos
import pandas as pd

# #################### Hipparcos Numbers for Reference #################### #
"""
alpha centauri A: HIP 71683
sirius: HIP 32349
polaris: HIP 11767
procyon: HIP 37279
betelgeuse: HIP 27989
rigel: HIP 24436
antares: HIP 80763
acrux: HIP 60718
THE SUN: -1 (Note: The Sun does not have a HIP Number)
"""
# http://simbad.u-strasbg.fr/simbad/sim-fbasic

# #################### Parameters and Variables #################### #

# Sun Parameters
L_sun = 3.828e26
d_sun = 1.496e11
m_sun = -26.74
F_sun = L_sun / (4 * np.pi * d_sun ** 2)

# Vector Variables
ihat = vp.vector(1, 0, 0)
jhat = vp.vector(0, 1, 0)
khat = vp.vector(0, 0, 1)
zero_vector = vp.vector(0, 0, 0)

# #################### Alterable Parameters and Variables #################### #

# Sky Parameters
R_sky = 37

# Reference Star
m_r0 = -1.46
R_r0 = 1
F_r0 = F_sun * 10 ** ((m_sun - m_r0) / 2.5)

# Filtering Variables
m_filt = 6.5 # best 5.5

# HIP Number of the Center Star
C_star = 71683 # The Sun: -1

# #################### Dataframe #################### #

with load.open(hipparcos.URL) as f:  # Load Hipparcos Catalog
    df = hipparcos.load_dataframe(f)  # Pandas dataframe of the Hipparcos Catalog (118218 stars)

# Filtering
df = df[df['ra_degrees'].notnull()]
df = df[df['magnitude'] <= m_filt]
print(f'After filtering, there are {len(df)} stars')

bright_stars = Star.from_dataframe(df)

# #################### Observe #################### #

planets = load('de421.bsp')
earth = planets['earth']

ts = load.timescale()
t = ts.utc(2000, 1, 1)
astrometric = earth.at(t).observe(bright_stars)
ra, dec, distance = astrometric.radec()

# #################### Stars Lists #################### #

# Actual position vector list
r_list = [vp.vector(zero_vector)]

for i in range(0, len(df)):
    x = distance.au[i] * np.cos(dec.degrees[i] * np.pi / 180) * np.cos(ra.hours[i] * 15 * np.pi / 180)
    y = distance.au[i] * np.cos(dec.degrees[i] * np.pi / 180) * np.sin(ra.hours[i] * 15 * np.pi / 180)
    z = distance.au[i] * np.sin(dec.degrees[i] * np.pi / 180)
    r_list.append(d_sun * vp.vector(x, y, z))

# Visual Luminosity list
L_list = [L_sun]

for i in range(0, len(df)):
    L_i = L_sun * (distance.au[i]) ** 2 * 10 ** ((m_sun - df.loc[df.index[i], 'magnitude']) / 2.5)
    L_list.append(L_i)

# #################### Set up Scene and Lighting #################### #

win = 700
scene = vp.canvas(title=f"<h1><b>The Sky as Seen From HIP {C_star}</b></h1>", width=1.5*win, height=win)
# scene.append_to_title("<div id='fps'/>")
scene.caption = """
<b>Drag with Right Click to Rotate</b>
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Reference Stars
Alpha Centauri A: Yellow
Sirius: Light Blue
Polaris: Purple
Betelgeuse: Red
Rigel: Blue
Antares: Orange
The Sun: Green
"""
scene.lights = []
scene.ambient = vp.color.gray(0.1)

scene.autoscale = False
scene.userzoom = False
scene.userpan = False
scene.camera.pos = vp.vector(0, 0, 0)
scene.up = vp.vector(0, 0, 1)
scene.forward = vp.vector(1, 0, 0)
scene.center = vp.vector(0, 0, 0)
scene.range = R_sky / 10

# #################### Define and Set up Bodies #################### #

Xtars = [] # List of Vpython objects, the stars
stars_dict_lum_index = {'sirius': df.index.get_loc(32349) + 1, 'polaris': df.index.get_loc(11767) + 1, # Dictionary for index in the luminosity and position list (if j>i)
              'alpha centauri': df.index.get_loc(71683) + 1, 'betelgeuse': df.index.get_loc(27989) + 1,
              'rigel': df.index.get_loc(24436) + 1, 'antares': df.index.get_loc(80763) + 1}

if C_star <= 0:
    j = 0
else:
    j = df.index.get_loc(C_star) + 1 # The index of the center star in the luminosity and position list. The +1 is because we added the Sun to the list

for i in range(0, len(df) + 1):
    if i == j:
        continue
    else:
        R = R_r0 * (L_list[i] / (4 * np.pi * vp.mag2(r_list[i] - r_list[j]) * F_r0)) ** (1 / 2)
        mag_rel = m_r0 + 2.5 * np.log10((4 * np.pi * vp.mag2(r_list[i] - r_list[j]) * F_r0) / L_list[i])
        Xtars.append(vp.sphere(pos=((r_list[i] - r_list[j]) / vp.mag(r_list[i] - r_list[j])) * R_sky,
                               radius=R, luminosity=L_list[i], relative_magnitude=mag_rel, color=vp.vector(1, 1, 1),
                               default_color=vp.vector(1, 1, 1), emissive=True))
        # THE SUN
        if i == 0:
            Xtars[i].color = vp.vector(0, 1, 0)
            Xtars[i].default_color = vp.vector(0, 1, 0)
        # POLARIS
        elif i == stars_dict_lum_index['polaris'] and j < i:
            Xtars[i - 1].color = vp.vector(1, 0, 1)
            Xtars[i - 1].default_color = vp.vector(1, 0, 1)
        elif i == stars_dict_lum_index['polaris'] and j > i:
            Xtars[i].color = vp.vector(1, 0, 1)
            Xtars[i].default_color = vp.vector(1, 0, 1)
        # SIRIUS
        elif i == stars_dict_lum_index['sirius'] and j < i:
            Xtars[i - 1].color = vp.vector(0, 1, 1)
            Xtars[i - 1].default_color = vp.vector(0, 1, 1)
        elif i == stars_dict_lum_index['sirius'] and j > i:
            Xtars[i].color = vp.vector(0, 1, 1)
            Xtars[i].default_color = vp.vector(0, 1, 1)
        # ALPHA CENTAURI A
        elif i == stars_dict_lum_index['alpha centauri'] and j < i:
            Xtars[i - 1].color = vp.vector(1, 1, 0)
            Xtars[i - 1].default_color = vp.vector(1, 1, 0)
        elif i == stars_dict_lum_index['alpha centauri'] and j > i:
            Xtars[i].color = vp.vector(1, 1, 0)
            Xtars[i].default_color = vp.vector(1, 1, 0)
        # BETELGEUSE
        elif i == stars_dict_lum_index['betelgeuse'] and j < i:
            Xtars[i - 1].color = vp.vector(1, 0, 0)
            Xtars[i - 1].default_color = vp.vector(1, 0, 0)
        elif i == stars_dict_lum_index['betelgeuse'] and j > i:
            Xtars[i].color = vp.vector(1, 0, 0)
            Xtars[i].default_color = vp.vector(1, 0, 0)
        # RIGEL
        elif i == stars_dict_lum_index['rigel'] and j < i:
            Xtars[i - 1].color = vp.vector(0, 0, 1)
            Xtars[i - 1].default_color = vp.vector(0, 0, 1)
        elif i == stars_dict_lum_index['rigel'] and j > i:
            Xtars[i].color = vp.vector(0, 0, 1)
            Xtars[i].default_color = vp.vector(0, 0, 1)
        # ANTARES
        elif i == stars_dict_lum_index['antares'] and j < i:
            Xtars[i - 1].color = vp.vector(1, 0.27, 0)
            Xtars[i - 1].default_color = vp.vector(1, 0.27, 0)
        elif i == stars_dict_lum_index['antares'] and j > i:
            Xtars[i].color = vp.vector(1, 0.27, 0)
            Xtars[i].default_color = vp.vector(1, 0.27, 0)

# #################### Stuff #################### #
#print(df.index.get_loc(C_star)+1)
print(j)
print(stars_dict_lum_index['polaris'])
print(stars_dict_lum_index['sirius'])

# TODO: color dictionary
