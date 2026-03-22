import numpy as np

EARTH_RADIUS = 6378.137

def latlon_to_ecef(lat, lon):

    lat = np.radians(lat)
    lon = np.radians(lon)

    x = EARTH_RADIUS * np.cos(lat) * np.cos(lon)
    y = EARTH_RADIUS * np.cos(lat) * np.sin(lon)
    z = EARTH_RADIUS * np.sin(lat)

    return np.array([x, y, z])


def elevation_angle(sat_pos, gs_pos):

    rho = sat_pos - gs_pos

    rho_hat = rho / np.linalg.norm(rho)
    zenith = gs_pos / np.linalg.norm(gs_pos)

    elev = np.arcsin(np.dot(rho_hat, zenith))

    return np.degrees(elev)


def has_los(sat_pos, station):

    gs = latlon_to_ecef(station["lat"], station["lon"])

    elev = elevation_angle(sat_pos, gs)

    return elev > station["min_elevation"]