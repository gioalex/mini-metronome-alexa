import re

ISO_8601_DURATION_REGEX = r"P((?P<years>\d+)Y)?((?P<months>\d+)M)?((?P<weeks>\d+)W)?((?P<days>\d+)D)?(T((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?)?"


def get_metronome_url(tempo, seconds):
    beats = int(seconds * tempo / 60)
    return "https://metronomer.com/download.php?mp3=/Click_{}_1_4_{}_rdm.mp3&pan=".format(tempo, beats + 1)


def iso_8601_duration_to_seconds(iso_8601_duration):
    match = re.match(ISO_8601_DURATION_REGEX, iso_8601_duration).groupdict()
    return int(match['years'] or 0)*365*24*3600 + \
        int(match['months'] or 0)*30*24*3600 + \
        int(match['weeks'] or 0)*7*24*3600 + \
        int(match['days'] or 0)*24*3600 + \
        int(match['hours'] or 0)*3600 + \
        int(match['minutes'] or 0)*60 + \
        int(match['seconds'] or 0)
