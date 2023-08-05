#!/usr/bin/env python

"""
metadata
~~~~~~~~~~~~~~~~~
Download metadata from the commandline
"""

import argparse
import codecs
import json
import sys
import traceback
import re

from src.core.dhis import Dhis
from src.core.helpers import properties_to_remove, csv_import_objects
from src.core.logger import *


class Downloader(Dhis):
    def get_dhis_version(self):
        """ return DHIS2 verson (e.g. 26) as integer"""
        response = self.get(endpoint='system/info', file_type='json')

        # remove -snapshot for play.dhis2.org/dev
        snapshot = '-SNAPSHOT'
        version = response.get('version')
        if snapshot in version:
            version = version.replace(snapshot, '')

        return int(version.split('.')[1])

    def get_metadata(self, o_type, o_filter, file_type, fields, compressed, dhis_version):

        if o_type in {'dataSets', 'programs', 'categoryCombos'}:
            print("Looking for export {} with dependencies? "
                  "Look at docs.dhis2.org > Dev guide > 'Metadata export with dependencies'".format(o_type))
        if file_type == 'csv':
            print("WARNING: CSV file needs to be edited correctly before importing.")
            if o_type not in csv_import_objects:
                print("WARNING: {} cannot be imported to DHIS2 directly with CSV files.".format(o_type))

        params = {o_type: True}

        if compressed:
            if file_type != 'csv':
                file_type += ".zip"
            else:
                print("Can't zip CSVs.")

        # DHIS 2.22 and older
        if dhis_version < 23:
            params['assumeTrue'] = False
            endpoint = 'metaData'
            if fields or o_filter:
                print("Can't filter objects or fields on metadata export in version 2.{}".format(dhis_version))

        # DHIS 2.23 and newer
        else:
            if fields:
                params['fields'] = fields
            else:
                to_remove = ",!{}".format(",!".join(properties_to_remove))
                params['fields'] = ":owner{}".format(to_remove)
            if o_filter:
                params['filter'] = o_filter
            if dhis_version == 24:
                endpoint = '23/metadata'
            else:
                endpoint = '{}/metadata'.format(dhis_version)

        return self.get(endpoint=endpoint, file_type=file_type, params=params)


def parse_args():
    file_types = ['json', 'xml', 'csv']

    parser = argparse.ArgumentParser(description="Download metadata")
    parser.add_argument('-s', dest='server', action='store', help="Server, e.g. play.dhis2.org/demo", required=True)
    parser.add_argument('-t', dest='object_type', action='store', required=True,
                        help="DHIS2 object types to get, e.g. -t=dataElements")
    parser.add_argument('-f', dest='object_filter', action='store', help="Object filter, e.g. -f='name:like:Acute'",
                        required=False)
    parser.add_argument('-e', dest='fields', action='store', help="Fields to include, e.g. -f='id,name'",
                        required=False)
    parser.add_argument('-y', dest='file_type', action='store', help="File format, defaults to JSON", required=False,
                        choices=file_types,
                        default='json')
    parser.add_argument('-z', dest='compress', action='store_true', help="Compress/zip download", default=False, required=False)
    parser.add_argument('-u', dest='username', action='store', help="DHIS2 username", required=True)
    parser.add_argument('-p', dest='password', action='store', help="DHIS2 password", required=True)
    parser.add_argument('-d', dest='debug', action='store_true', default=False, required=False,
                        help="Debug flag - writes more info to log file")

    return parser.parse_args()


def main():
    args = parse_args()
    init_logger(args.debug)
    log_start_info(__file__)

    if args.object_filter:
        o_filter = args.object_filter.decode()
    else:
        o_filter = None

    dhis = Downloader(server=args.server, username=args.username, password=args.password, api_version=None)
    version = dhis.get_dhis_version()
    o_type = dhis.get_all_object_type(args.object_type)

    data = dhis.get_metadata(o_type=o_type, o_filter=o_filter, file_type=args.file_type, fields=args.fields,
                             compressed=args.compress, dhis_version=version)

    if o_filter:
        # replace special characters in filter for file name
        remove = ":^!$"
        filter_sanitized = o_filter
        for char in remove:
            filter_sanitized = filter_sanitized.replace(char, "-")
        file_name = "metadata-{}_{}_{}.{}".format(o_type, dhis.file_timestamp, filter_sanitized, args.file_type)
    else:
        file_name = "metadata-{}_{}.{}".format(o_type, dhis.file_timestamp, args.file_type)

    # saving the file depending on format
    try:
        if args.file_type == 'json':
            # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
            with open(file_name, 'wb') as json_file:
                json.dump(data, codecs.getwriter('utf-8')(json_file), ensure_ascii=False, indent=4)
        elif args.file_type == 'xml':
            with codecs.open(file_name, 'wb', encoding='utf-8') as xml_file:
                xml_file.write(data)
        elif args.file_type == 'csv':
            with codecs.open(file_name, 'wb', encoding='utf-8') as csv_file:
                csv_file.write(data)
        log_info(u"+++ Success! {} file exported to {}".format(args.file_type.upper(), file_name))
    except Exception:
        os.remove(file_name)
        log_info(traceback.print_exc())


if __name__ == "__main__":
    main()
