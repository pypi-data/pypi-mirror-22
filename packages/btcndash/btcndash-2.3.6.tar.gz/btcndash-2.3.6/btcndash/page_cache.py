#!/usr/bin/python
# -*- coding: utf-8 -*-

""""
Copyright (c) 2014, Matt Doiron. All rights reserved.

BTCnDash is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BTCnDash is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BTCnDash. If not, see <http://www.gnu.org/licenses/>.
"""

# System Imports
import time
import os
import json
import errno
from socket import error as socket_error
from bottle import template
import bitcoin.rpc as rpc
from bitcoin.rpc import JSONRPCError
try:
    import urllib.request as urlrequest
except ImportError:
    import urllib2 as urlrequest

# BTCnDash Imports
import logger

APP_ROOT = os.path.dirname(os.path.realpath(__file__))


class PageCache(object):
    """Retrieves data from bitcoind via RPC and generates static, cached pages."""

    def __init__(self, config):
        self.config = config
        self.log = logger.setup_logging(self.config['log_level'], __name__)
        self.location = {}

        # Make sure the html cache folder is present
        html_path = os.path.join(APP_ROOT, 'static', 'html')
        try:
            os.makedirs(html_path)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise

        # Prepare the RPC connection to bitcoind
        self.con = rpc.Proxy(service_url=self.config['rpc_urn'])

        # Generate and cache all pages
        self.cache_loc()
        self.cache_pages()

    def cache_loc(self):
        """Cache location/IP separately because they should rarely change."""

        # Refresh IP and location
        try:
            if 'detect' in [self.config['server_location'], self.config['server_ip_public']]:
                try:
                    loc = json.loads(urlrequest.urlopen(self.config['loc_url']).read().decode('utf-8'))
                except Exception as err:
                    self.log.error("Error caching location: {}".format(err))
                    loc = {"as": "n/a", "city": "n/a", "country": "n/a", "countryCode": "n/a",
                           "isp": "n/a", "lat": "n/a", "lon": "n/a", "org": "n/a", "query": "n/a",
                           "region": "n/a", "regionName": "n/a", "status": "n/a",
                           "timezone": "n/a", "zip": "n/a"}

            if self.config['server_location'] == 'detect':
                self.log.debug('Detecting server location and IP address...')
                self.location['server_location'] = ', '.join([loc['city'], loc['region'],
                                                              loc['country']])
                self.location['lat'] = loc['lat']
                self.location['lon'] = loc['lon']
            else:
                self.location['server_location'] = self.config['server_location']
                self.location['lat'] = self.config['server_latitude']
                self.location['lon'] = self.config['server_longitude']
            if self.config['server_ip_public'] == 'detect':
                self.location['server_ip_public'] = loc['query']
            else:
                self.location['server_ip_public'] = self.config['server_ip_public']
        except Exception as err:
            self.log.error("Error caching location: {}".format(err))
            self.location['server_location'] = 'Unknown'
            self.location['server_ip_public'] = 'n/a'
            self.location['lat'] = '0'
            self.location['lon'] = '0'

    def _condense_commands(self):
        """Creates a set of unique rpc commands to be executed."""

        # Create a set of blocks that will need data
        tiles = []
        for page_info in self.config['pages'].values():
            for tile in page_info['tiles']:
                tiles.extend(tile)
        tile_set = set(tiles)

        # Use the set of blocks to create a set of rpc commands required
        commands = []
        try:
            for tile in tile_set:
                rpc_commands = self.config['tiles'][tile]['rpc_commands']
                for command in rpc_commands:
                    commands.append(command)
            command_set = set(commands)
        except KeyError as err:
            self.log.error("Tile '{}' not found! Please verify your config file.".format(err))
            return []
        except Exception as err:
            self.log.error("Exception raised while condensing commands: {}".format(err))
            return []
        return command_set

    def _get_rpc_data(self, commands):
        """Retrieve and combine raw data from the RPC server."""

        data = {}

        self.log.debug('Retrieving data from bitcoind via RPC...')
        for command in commands:
            if command in ['bitnodes', '21co_fees']:
                continue
            try:
                command_split = command.split(',')
                if len(command_split) > 1:
                    if command_split[1].lower() == 'true':
                        args = True
                    elif command_split[1].lower() == 'false':
                        args = False
                    else:
                        args = command_split[1]
                    result = self.con.call(command_split[0], args)
                else:
                    result = self.con.call(command_split[0])
            except JSONRPCError as err:
                self.log.error("Error ({}): {}".format(err.error['code'], err.error['message']))
                self.log.error("Failed to retrieve data using command '{}'.".format(command))
                return {}
            except socket_error as err:
                self.log.error("Unable to connect to Bitcoin RPC server: {}".format(err))
                return {}
            except ValueError as err:
                self.log.error("No response from server. Please verify your username and password!")
                return {}
            except Exception as err:
                self.log.error("Exception raised while retrieving data from bitcoind: {}".format(err))
                return {}

            # Check if we can use update directly or with a derived key name
            if isinstance(result, dict):
                if command.startswith('getrawmempool'):
                    data.update({'rawmempool': result})
                else:
                    data.update(result)
            else:
                data.update({command.lstrip('get'): result})

        return data

    def _get_21co_fees(self):
        """Retrieves info relating to fee estimates from 21.co"""

        fee_url = self.config['fee_url'] + 'recommended'
        req = urlrequest.Request(fee_url, headers={'User-Agent': 'Mozilla/5.0'})
        fees = {"fastestFee": "n/a", "halfHourFee": "n/a", "hourFee": "n/a"}
        try:
            fees.update(json.loads(urlrequest.urlopen(req).read().decode('utf-8')))
        except (urlrequest.URLError, urlrequest.HTTPError) as err:
            pass
        except Exception as err:
            self.log.error("Exception raised while retrieving data from 21co: {}".format(err))

        return fees

    def _get_bitnodes_data(self):
        """Retrieves info relating to the Bitnodes program."""

        ip = '-'.join([self.location['server_ip_public'], str(self.config['node_port'])])
        rank_query = "nodes/leaderboard/{}/".format(ip)
        status_query = "nodes/{}/".format(ip)
        rank_url = self.config['bitnodes_url'] + rank_query
        status_url = self.config['bitnodes_url'] + status_query
        rank = {"node": "n/a", "vi": "n/a", "si": "n/a", "hi": "n/a", "ai": "n/a", "pi": "n/a",
                "dli": "n/a", "dui": "n/a", "wli": "n/a", "wui": "n/a", "mli": "n/a", "mui": "n/a",
                "ni": "n/a", "bi": "n/a", "peer_index": "n/a", "rank": 0}
        status = {"hostname": "n/a", "address": "n/a", "status": "n/a",
                  "data": [0, "n/a", 0, 0, 0, "n/a", "n/a", "n/a", 0,  0, "n/a", "n/a", "n/a"],
                  "bitcoin_address": "n/a", "url": "n/a", "verified": None}
        try:
            rank.update(json.loads(urlrequest.urlopen(rank_url).read().decode('utf-8')))
            status.update(json.loads(urlrequest.urlopen(status_url).read().decode('utf-8')))
        except (urlrequest.URLError, urlrequest.HTTPError) as err:
            pass
        except Exception as err:
            self.log.error("Exception raised while retrieving data from 21co: {}".format(err))
        bitnodes_link = self.config['bitnodes_url'].replace('api/v1', 'nodes') + ip
        return {'status': status, 'rank': rank, 'bitnodes_link': bitnodes_link}

    @staticmethod
    def _services_offered(service_bits_in):
        """Returns nice string listing the services corresponding to a service bit
        :param service_bits_in: String or integer of node service bits
        :return:
        """

        # Service bits directly from Bitcoin core source
        NODE_NETWORK = (1 << 0)
        NODE_GETUTXO = (1 << 1)
        NODE_BLOOM = (1 << 2)
        NODE_WITNESS = (1 << 3)

        # Convert type of input if necessary
        if isinstance(service_bits_in, int):
            service_bits = service_bits_in
        elif isinstance(service_bits_in, str) or isinstance(service_bits_in, unicode):
            service_bits = int(service_bits_in, 16)
        else:
            service_bits = service_bits_in

        # Construct list of services offered
        services = []
        if NODE_NETWORK == service_bits & NODE_NETWORK:
            services.append("NODE_NETWORK")
        if NODE_GETUTXO == service_bits & NODE_GETUTXO:
            services.append("NODE_GETUTXO")
        if NODE_BLOOM == service_bits & NODE_BLOOM:
            services.append("NODE_BLOOM")
        if NODE_WITNESS == service_bits & NODE_WITNESS:
            services.append("NODE_WITNESS")
        if not services:
            services.append("NONE")
        services_offered = ', '.join(services)

        return services_offered

    def get_data(self):
        """Gets data and processes it into the format required for the templates."""

        data = {}
        commands = self._condense_commands()
        data.update(self._get_rpc_data(commands))
        data.update(self.config)
        data.update(self.location)

        if 'bitnodes' in commands:
            data.update({'bitnodes': self._get_bitnodes_data()})

        if '21co_fees' in commands:
            data.update({'21co_fees': self._get_21co_fees()})

        try:
            services_offered = self._services_offered(data['localservices'])
            data.update({'services_offered': services_offered})
        except KeyError as err:
            self.log.error("Cannot find specified raw data for '{}'. Please double-check your "
                           "dash block registry to ensure you've included all required RPC "
                           "commands.".format(err))
        except Exception as err:
            self.log.error("Exception raised while retrieving data: {}".format(err))

        return data

    def cache_pages(self):
        """Creates and caches all pages depending on the age of any existing files."""

        self.log.debug('Caching pages...')
        now = time.time()
        pages = self.config['pages']
        path = os.path.join(APP_ROOT, 'static', 'html', pages['index']['static'])

        # Find the last modified time of the index page and the current time
        if os.path.exists(path):
            modified = os.path.getmtime(path)
        else:
            modified = False

        # Check if last modified time is > CACHE_TIME_LOC seconds ago
        if now - modified >= self.config['cache_time_loc'] or not modified:

            # Refresh location and ip before checking other pages
            self.cache_loc()

        # Check if last modified time is > CACHE_TIME seconds ago
        if now - modified >= self.config['cache_time'] or not modified:

            # Retrieve data for use in templates
            data = self.get_data()
            if not data:
                self.log.error('No data was retrieved. Pages will not be generated.')
                return

            # Open the static file for each page and write the compiled template
            for page, page_info in pages.items():
                try:
                    path = os.path.join(APP_ROOT, 'static', 'html', page_info['static'])
                    data['title'] = page_info['title']
                    data['header_title'] = self.config['header_title']
                    with open(path, 'w') as static_page:
                        self.log.debug('Writing static page cache for: {}'
                                       .format(page_info['static']))
                        static_page.write(template(page_info['template'], data=data,
                                                   page_info=page_info,
                                                   tiles=self.config['tiles']))
                except KeyError as err:
                    self.log.error('KeyError: Cannot find data: {}'.format(err))
                    self.log.error('Some data was missing. Page {} will not be generated. Please '
                                   'check error logs for more information.'
                                   .format(data['title']))
                except Exception as err:
                    self.log.error("Exception raised while caching pages: {}".format(err))
