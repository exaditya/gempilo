import framework
# unique to module
import re

class Module(framework.module):

    def __init__(self, params):
        framework.module.__init__(self, params)
        self.register_option('domain', self.global_options['domain']['value'], 'yes', self.global_options['domain']['desc'])
        self.register_option('restrict', 1, 'yes', 'limit number of api requests (0 = unrestricted)')
        self.register_option('regex', '%s$' % (self.global_options['domain']['value']), 'no', 'regex to match for adding results to the database')
        self.info = {
                     'Name': 'Shodan Hostname Enumerator',
                     'Author': 'Tim Tomes (@LaNMaSteR53)',
                     'Description': 'Harvests hosts from the Shodanhq.com API by using the \'hostname\' search operator and updates the \'hosts\' table of the database with the results.',
                     'Comments': [
                                  'Note: \'RESTRICT\' option limits the number of API requests in order to prevent API query exhaustion.'
                                  ]
                     }

    def module_run(self):
        domain = self.options['domain']
        regex = self.options['regex']
        cnt = 0
        new = 0
        query = 'hostname:%s' % (domain)
        limit = self.options['restrict']
        results = self.search_shodan_api(query, limit)
        for host in results:
            if not 'hostnames' in host.keys():
                continue
            for hostname in host['hostnames']:
                cnt += 1
                self.output(hostname)
                if not regex or re.search(regex, hostname):
                    new += self.add_host(hostname)
        self.output('%d total hosts found.' % (cnt))
        if new: self.alert('%d NEW hosts found!' % (new))
