import dork_compose.plugin
import platform
import pkg_resources
from subprocess import call
import tempfile
import os

import logging
log = logging.getLogger(__name__)

class Plugin(dork_compose.plugin.Plugin):

    def environment(self):
        return {
            'DORK_DNS_PORT': self.dns_port,
            'DORK_DNS_HOST': self.dns_host,
            'DORK_PROXY_DOMAIN': self.proxy_domain,
        }

    @property
    def auxiliary_project(self):
        return pkg_resources.resource_filename('dork_compose', 'auxiliary/dns')

    @property
    def proxy_domain(self):
        return self.env.get('DORK_PROXY_DOMAIN', 'dork.io')

    @property
    def dns_port(self):
        return self.env.get('DORK_DNS_PORT', '53')

    @property
    def dns_host(self):
        return self.env.get('DORK_DNS_HOST', '127.0.0.1')

    def initializing(self, project, service_names=None):
        if platform.system() == "Darwin":
            resolver = '/etc/resolver/%s' % self.env.get('DORK_PROXY_DOMAIN')
            log.warn("Root password required to update DNS settings.")
            if not os.path.isfile(resolver):
                content = "# Generated by dork-composer\nnameserver %s\nport %s" % (
                    self.environment()['DORK_DNS_HOST'],
                    self.environment()['DORK_DNS_PORT']
                )
                tmp = tempfile.NamedTemporaryFile(delete=False)
                tmp.write(content)
                tmp.close()
                call(['sudo', 'mkdir', '-p', '/etc/resolver'])
                call(['sudo', 'cp', tmp.name, resolver])
                call(['sudo', 'chmod', '664', resolver])
                os.remove(tmp.name)
            call(['sudo', 'dscacheutil', '-flushcache'])
            call(['sudo', 'killall', '-HUP', 'mDNSResponder'])

        if platform.system() == "Linux":
            resolver = '/etc/resolv.conf'
            confline = 'nameserver %s' % self.environment()['DORK_DNS_HOST']

            lines = []
            lines.append(confline + '\n')
            with open(resolver, 'r') as resolvconf:
                for line in resolvconf.readlines():
                    if confline in line:
                        return
                    lines.append(line)

            lines.append('\n')
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(''.join(lines))
            tmp.close()
            log.warn("Root password required to update DNS settings.")
            call(['sudo', 'cp', tmp.name, resolver])
            call(['sudo', 'chmod', '664', resolver])
            os.remove(tmp.name)
