#!/usr/bin/python3

import argparse
import requests
import sys
import xml.etree.ElementTree as ET

BASE_URL = 'http://api.geonames.org/search'

JSON = 'json'
CSV = 'csv'

PLACE_CACHE = {}


class GeonamePlace:
    def __init__(self, toponym_name, name, lat, lng, geoname_id, country_code, country_name, fcl, fcode):
        self.toponym_name = toponym_name
        self.name = name
        self.lat = lat
        self.lng = lng
        self.geoname_id = geoname_id
        self.country_code = country_code
        self.country_name = country_name
        self.fcl = fcl
        self.fcode = fcode

    def __repr__(self):
        return 'GeonamePlace({id})'.format(id=self.geoname_id)

    def __dict__(self):
        return {
            'toponym_name': self.toponym_name,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'geoname_id': self.geoname_id,
            'country_code': self.country_code,
            'country_name': self.country_name,
            'fcl': self.fcl,
            'fcode': self.fcode
        }

    def __str__(self):
        return self.name

    @classmethod
    def fromxml(cls, xml_element):
        toponymName = xml_element.find('.//toponymName').text
        name = xml_element.find('.//name').text
        lat = xml_element.find('.//lat').text
        lng = xml_element.find('.//lng').text
        geoname_id = xml_element.find('.//geonameId').text
        country_code = xml_element.find('.//countryCode').text
        country_name = xml_element.find('.//countryName').text
        fcl = xml_element.find('.//fcl').text
        fcode = xml_element.find('.//fcode').text

        return cls(toponymName, name, lat, lng, geoname_id, country_code, country_name, fcl, fcode)


def search_place(place, username, limit=100):
    params = {'q': place, 'username': username, 'maxRows': limit}

    r = requests.get(BASE_URL, params=params)

    if r.status_code != 200:
        return []

    # parse XML
    root = ET.fromstring(r.text)

    return [GeonamePlace.fromxml(xml_element) for xml_element in root.findall('.//geoname')]


def search_with_cache(place_name, username):
    if place_name in PLACE_CACHE:
        return PLACE_CACHE[place_name]

    search_result = search_place(place_name, username, 1)
    if search_result:
        place = search_result[0]
        PLACE_CACHE[place_name] = place
        return place

    return None


def search_places(place_names, username):
    """Search for geonames for a list of place names"""
    places = []
    for name in place_names:
        place = search_place(name, username, 1)
        if place:
            places.append(place[0])

    return places


def main():
    parser = argparse.ArgumentParser(description='Get geo information for a list of places from Geonames')
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='input file (default: stdin)')
    parser.add_argument('output', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help='output file (default: stdout)')
    parser.add_argument('--username', '-u', nargs=1, dest='username', help='username to access geonames API',
                        required=True)
    format_group = parser.add_mutually_exclusive_group(required=True)
    format_group.add_argument('--json', dest='out_format', action='store_const', const=JSON,
                              help='format output as JSON')
    format_group.add_argument('--csv', dest='out_format', action='store_const', const=CSV,
                              help='format output as CSV')

    args = parser.parse_args()

    place_names = [name for name in args.input]
    places = search_places(place_names, args.username)

    if args.out_format == JSON:
        import json
        places = {'places': [vars(place) for place in places]}
        args.output.write(json.dumps(places))

    if args.out_format == CSV:
        import csv
        writer = csv.writer(args.output)
        writer.writerows([(place.name, place.lat, place.lng, place.geoname_id) for place in places])


if __name__ == '__main__':
    main()
