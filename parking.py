from sodapy import Socrata
import operator
import functools
import datetime
import voluptuous as v

DATASET_LOCATIONS = 'dtpv-d4pf'
DATASET_BAYINFO = 'rzb8-bz3y'

# schema for returning information to client
format_row = v.Schema({
    v.Required('lat'): str,
    v.Required('lon'): str,
    v.Required('bay_id'): str,
    v.Optional('parking_info'): {
        v.Optional('description1'): str,
        v.Optional('description2'): str,
        v.Optional('description3'): str,
        v.Optional('description4'): str,
        v.Optional('description5'): str,
        v.Optional('description6'): str
    }
}, extra=v.REMOVE_EXTRA)

validate_input = v.Schema({
    v.Optional('latitude'): str,
    v.Optional('longitude'): str,
    v.Optional('radius'): int
}, extra=v.REMOVE_EXTRA)

# default to somewhere in the Melbourne CBD
default_latitude = '-37.8137309'
default_longitude = '144.9642396'

# extract bay_ids from a list of parking bays
get_bay_ids = functools.partial(map, operator.itemgetter('bay_id'))


# turn a list of dicts into an index
def dict_reducer(existing, item):
    existing[item['bayid']] = item
    return existing


def find_bays(latitude=default_latitude, longitude=default_longitude, radius=200, date=None):
    if date is None:
        date = datetime.datetime.now()

    client = Socrata("data.melbourne.vic.gov.au", None)

    # find all (limited) bays within the radius
    results = client.get(DATASET_LOCATIONS, where='within_circle(location, %s, %s, %d)' % (latitude, longitude, radius), limit=2000)
    if not results:
        return []
    # extract all bay ids to look up their bay information
    bay_ids = get_bay_ids(results)

    parking_info = functools.reduce(dict_reducer, client.get(DATASET_BAYINFO, where='bayid IN (%s)' % (','.join(bay_ids)), limit=2000), dict())

    for result in results:
        result.update(parking_info=parking_info.get(result.get('bay_id')))

    # todo: determine which day/time slot to look at

    return list(map(format_row, results))


def api_find_bays(params):
    return find_bays(**validate_input(params))


if __name__ == '__main__':
    print(find_bays())
