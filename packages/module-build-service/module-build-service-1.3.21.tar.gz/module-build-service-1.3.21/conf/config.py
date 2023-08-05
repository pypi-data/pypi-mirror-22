from os import path

# FIXME: workaround for this moment till confdir, dbdir (installdir etc.) are
# declared properly somewhere/somehow
confdir = path.abspath(path.dirname(__file__))
# use parent dir as dbdir else fallback to current dir
dbdir = path.abspath(path.join(confdir, '..')) if confdir.endswith('conf') \
        else confdir


class BaseConfiguration(object):
    DEBUG = False
    # Make this random (used to generate session keys)
    SECRET_KEY = '74d9e9f9cd40e66fc6c4c2e9987dce48df3ce98542529fd0'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(path.join(
        dbdir, 'module_build_service.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Where we should run when running "manage.py runssl" directly.
    HOST = '0.0.0.0'
    PORT = 5000

    # Global network-related values, in seconds
    NET_TIMEOUT = 120
    NET_RETRY_INTERVAL = 30

    SYSTEM = 'koji'
    MESSAGING = 'fedmsg'  # or amq
    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.prod']
    KOJI_CONFIG = '/etc/module-build-service/koji.conf'
    KOJI_PROFILE = 'koji'
    KOJI_ARCHES = ['i686', 'armv7hl', 'x86_64']
    KOJI_PROXYUSER = True
    KOJI_REPOSITORY_URL = 'https://kojipkgs.fedoraproject.org/repos'
    KOJI_TAG_PREFIXES = ['module']
    COPR_CONFIG = '/etc/module-build-service/copr.conf'
    PDC_URL = 'http://pdc.fedoraproject.org/rest_api/v1'
    PDC_INSECURE = True
    PDC_DEVELOP = True
    SCMURLS = ["git://pkgs.fedoraproject.org/modules/"]
    YAML_SUBMIT_ALLOWED = False

    # How often should we resort to polling, in seconds
    # Set to zero to disable polling
    POLLING_INTERVAL = 600

    # Determines how many builds that can be submitted to the builder
    # and be in the build state at a time. Set this to 0 for no restrictions
    NUM_CONSECUTIVE_BUILDS = 5

    RPMS_DEFAULT_REPOSITORY = 'git://pkgs.fedoraproject.org/rpms/'
    RPMS_ALLOW_REPOSITORY = False
    RPMS_DEFAULT_CACHE = 'http://pkgs.fedoraproject.org/repo/pkgs/'
    RPMS_ALLOW_CACHE = False

    MODULES_DEFAULT_REPOSITORY = 'git://pkgs.fedoraproject.org/modules/'
    MODULES_ALLOW_REPOSITORY = False

    SSL_ENABLED = True
    SSL_CERTIFICATE_FILE = '/etc/module-build-service/server.crt'
    SSL_CERTIFICATE_KEY_FILE = '/etc/module-build-service/server.key'
    SSL_CA_CERTIFICATE_FILE = '/etc/module-build-service/cacert.pem'

    PKGDB_API_URL = 'https://admin.fedoraproject.org/pkgdb/api'

    ALLOWED_GROUPS = set([
        'packager',
        #'modularity-wg',
    ])

    # Available backends are: console, file, journal.
    LOG_BACKEND = 'journal'

    # Path to log file when LOG_BACKEND is set to "file".
    LOG_FILE = 'module_build_service.log'

    # Available log levels are: debug, info, warn, error.
    LOG_LEVEL = 'info'

    # Settings for Kerberos
    KRB_KEYTAB = None
    KRB_PRINCIPAL = None
    KRB_CCACHE = None

    # AMQ prefixed variables are required only while using 'amq' as messaging backend
    # Addresses to listen to
    AMQ_RECV_ADDRESSES = ['amqps://messaging.mydomain.com/Consumer.m8y.VirtualTopic.eng.koji',
                          'amqps://messaging.mydomain.com/Consumer.m8y.VirtualTopic.eng.module_build_service']
    # Address for sending messages
    AMQ_DEST_ADDRESS = 'amqps://messaging.mydomain.com/Consumer.m8y.VirtualTopic.eng.module_build_service'
    AMQ_CERT_FILE = '/etc/module_build_service/msg-m8y-client.crt'
    AMQ_PRIVATE_KEY_FILE = '/etc/module_build_service/msg-m8y-client.key'
    AMQ_TRUSTED_CERT_FILE = '/etc/module_build_service/Root-CA.crt'

    # Disable Client Authorization
    NO_AUTH = False

    CACHE_DIR = '~/modulebuild/cache'


class DevConfiguration(BaseConfiguration):
    DEBUG = True
    LOG_BACKEND = 'console'
    LOG_LEVEL = 'debug'

    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.dev', 'org.fedoraproject.stg']

    ALLOWED_GROUPS = set([
        'packager',
        # Make this convenient for f2.0 developers
        'factory2',
        'modularity-wg',
    ])

    # Global network-related values, in seconds
    NET_TIMEOUT = 5
    NET_RETRY_INTERVAL = 1

    # Uncomment next line for local builds
    # SYSTEM = 'mock'

    if path.exists('/home/fedora/modularity.keytab'):
        KRB_PRINCIPAL = 'modularity@STG.FEDORAPROJECT.ORG'
        KRB_KEYTAB = '/home/fedora/modularity.keytab'
        KRB_CCACHE = '/var/tmp/krb5cc'
    else:
        # This requires that your principal be listed server side in
        # ProxyPrincipals, and that is only true for our modularity system
        # user.  See:   https://infrastructure.fedoraproject.org/cgit/ansible.git/commit/?id=a28a93dad75248c30c1792ec35f588c8e317c067
        KOJI_PROXYUSER = False

    KOJI_CONFIG = path.join(confdir, 'koji.conf')
    KOJI_PROFILE = 'staging'
    KOJI_ARCHES = ['x86_64']
    KOJI_REPOSITORY_URL = 'http://kojipkgs.stg.fedoraproject.org/repos'

    OIDC_CLIENT_SECRETS = path.join(confdir, 'client_secrets.json')
    OIDC_REQUIRED_SCOPE = 'https://mbs.fedoraproject.org/oidc/submit-build'

    SSL_CERTIFICATE_FILE = path.join(confdir, 'server.crt')
    SSL_CERTIFICATE_KEY_FILE = path.join(confdir, 'server.key')
    SSL_CA_CERTIFICATE_FILE = path.join(confdir, 'cacert.pem')

    COPR_CONFIG = path.join(confdir, 'copr.conf')


class TestConfiguration(BaseConfiguration):
    LOG_BACKEND = 'console'
    LOG_LEVEL = 'debug'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(
        path.join(dbdir, 'tests', 'test_module_build_service.db'))
    DEBUG = True
    MESSAGING = 'in_memory'
    PDC_URL = 'http://pdc.fedoraproject.org/rest_api/v1'

    # Global network-related values, in seconds
    NET_TIMEOUT = 3
    NET_RETRY_INTERVAL = 1

    KOJI_CONFIG = './conf/koji.conf'
    KOJI_PROFILE = 'staging'
    SERVER_NAME = 'localhost'

    KOJI_REPOSITORY_URL = 'https://kojipkgs.stg.fedoraproject.org/repos'
    SCMURLS = ["git://pkgs.stg.fedoraproject.org/modules/"]
    PKGDB_API_URL = 'https://admin.stg.fedoraproject.org/pkgdb/api'


class ProdConfiguration(BaseConfiguration):
    pass
