def photonsPerMag(mag, mask, pxlScale, wvlBand, expTime):
    '''
    Calculates the photon flux for a given aperture, star magnitude and wavelength band

    Parameters:
        mag (float): Star apparent magnitude
        mask (ndarray): 2-d pupil mask array, 1 is transparent, 0 opaque
        pxlScale (float): size in metres of each pixel in mask
        wvlBand (float): length of wavelength band in nanometres
        expTime (float): Exposure time in seconds

    Returns:
        float: number of photons
    '''

    #Area defined in cm, so turn m to cm
    area = mask.sum() * pxlScale**2 * 100**2

    photonPerSecPerAreaPerWvl = 1000 * (10**(-float(mag)/2.5))

    #Wvl defined in Angstroms
    photonPerSecPerArea = photonPerSecPerAreaPerWvl * wvlBand*10

    photonPerSec = photonPerSecPerArea * area

    photons = photonPerSec * expTime

    return photons