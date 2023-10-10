import locale

locales = {
    "United States": "en_US",
    "United Kingdom": "en_GB",
    "France": "fr_FR",
    "Belgium": "fr_BE",
    "Luxembourg": "fr_LU",
    "Switzerland": "fr_CH",
    "Norway": "no_NO",
}


def SetLocale(country):
    try:
        # locale.setlocale(locale.LC_ALL,locales[country]) # TODO Needs to be decided by city/town!
        if country == "United States":
            locale.setlocale(locale.LC_ALL, "en_US")
        else:
            locale.setlocale(locale.LC_ALL, "en_GB")
    except:
        pass
