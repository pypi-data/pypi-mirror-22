from unittest import TestCase
from unittest.mock import call, patch, MagicMock, Mock
from conductr_cli.test.cli_test_case import strip_margin, create_mock_logger
from conductr_cli.exceptions import BundleResolutionError, ContinuousDeliveryError
from conductr_cli import resolver
from conductr_cli.resolvers import \
    bintray_resolver, docker_resolver, docker_offline_resolver, uri_resolver, offline_resolver, stdin_resolver
from pyhocon import ConfigFactory
import tempfile


class TestResolver(TestCase):

    def test_resolve_bundle_success(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_from_cache = MagicMock(return_value=(False, None, None))
        first_resolver_mock.resolve_bundle = MagicMock(return_value=(False, None, None))

        second_resolver_mock = Mock()
        second_resolver_mock.load_bundle_from_cache = MagicMock(return_value=(False, None, None))
        second_resolver_mock.resolve_bundle = MagicMock(return_value=(True, 'bundle_name', 'mock bundle_file'))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock, second_resolver_mock])

        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            bundle_name, bundle_file = resolver.resolve_bundle(custom_settings, '/some-cache-dir', '/some-bundle-path')
            self.assertEqual('bundle_name', bundle_name)
            self.assertEqual('mock bundle_file', bundle_file)

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_from_cache('/some-cache-dir', '/some-bundle-path')
        first_resolver_mock.resolve_bundle.assert_called_with('/some-cache-dir', '/some-bundle-path')

        second_resolver_mock.load_from_cache('/some-cache-dir', '/some-bundle-path')
        second_resolver_mock.resolve_bundle.assert_called_with('/some-cache-dir', '/some-bundle-path')

    def test_resolve_bundle_failure(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_from_cache = MagicMock(return_value=(False, None, None))
        first_resolver_mock.resolve_bundle = MagicMock(return_value=(False, None, None))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            self.assertRaises(BundleResolutionError, resolver.resolve_bundle, custom_settings, '/some-cache-dir',
                              '/some-bundle-path')

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_from_cache('/some-cache-dir', '/some-bundle-path')
        first_resolver_mock.resolve_bundle.assert_called_with('/some-cache-dir', '/some-bundle-path')

    def test_resolve_bundle_from_cache(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_from_cache = MagicMock(return_value=(True, 'bundle_name', 'mock bundle_file'))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            bundle_name, bundle_file = resolver.resolve_bundle(custom_settings, '/some-cache-dir',
                                                               '/some-bundle-path')
            self.assertEqual('bundle_name', bundle_name)
            self.assertEqual('mock bundle_file', bundle_file)

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_from_cache('/some-cache-dir', '/some-bundle-path')

    def test_resolve_bundle_configuration_success(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_configuration_from_cache = MagicMock(return_value=(False, None, None))
        first_resolver_mock.resolve_bundle_configuration = MagicMock(return_value=(False, None, None))

        second_resolver_mock = Mock()
        second_resolver_mock.load_bundle_configuration_from_cache = MagicMock(return_value=(False, None, None))
        second_resolver_mock.resolve_bundle_configuration = MagicMock(return_value=(True, 'bundle_name',
                                                                                    'mock bundle_file'))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock, second_resolver_mock])

        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            bundle_name, bundle_file = resolver.resolve_bundle_configuration(
                custom_settings, '/some-cache-dir', '/some-bundle-path')
            self.assertEqual('bundle_name', bundle_name)
            self.assertEqual('mock bundle_file', bundle_file)

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_bundle_configuration_from_cache('/some-cache-dir', '/some-bundle-path')
        first_resolver_mock.resolve_bundle_configuration.assert_called_with('/some-cache-dir', '/some-bundle-path')

        second_resolver_mock.load_bundle_configuration_from_cache('/some-cache-dir', '/some-bundle-path')
        second_resolver_mock.resolve_bundle_configuration.assert_called_with('/some-cache-dir', '/some-bundle-path')

    def test_resolve_bundle_configuration_failure(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_configuration_from_cache = MagicMock(return_value=(False, None, None))
        first_resolver_mock.resolve_bundle_configuration = MagicMock(return_value=(False, None, None))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            self.assertRaises(BundleResolutionError, resolver.resolve_bundle_configuration, custom_settings,
                              '/some-cache-dir', '/some-bundle-path')

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_bundle_configuration_from_cache('/some-cache-dir', '/some-bundle-path')
        first_resolver_mock.resolve_bundle_configuration.assert_called_with('/some-cache-dir', '/some-bundle-path')

    def test_resolve_bundle_configuration_from_cache(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_configuration_from_cache = MagicMock(return_value=(True, 'bundle_name',
                                                                                           'mock bundle_file'))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            bundle_name, bundle_file = resolver.resolve_bundle_configuration(custom_settings, '/some-cache-dir',
                                                                             '/some-bundle-path')
            self.assertEqual('bundle_name', bundle_name)
            self.assertEqual('mock bundle_file', bundle_file)

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_bundle_configuration_from_cache('/some-cache-dir', '/some-bundle-path')


class TestResolverResolveBundleVersion(TestCase):
    def test_resolve_bundle_version_success(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.resolve_bundle_version = MagicMock(return_value=None)

        second_resolver_mock = Mock()
        resolved_version = {'test': 'only'}
        second_resolver_mock.resolve_bundle_version = MagicMock(return_value=resolved_version)

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock, second_resolver_mock])

        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            result = resolver.resolve_bundle_version(custom_settings, 'bundle')
            self.assertEqual(resolved_version, result)

        resolver_chain_mock.assert_called_with(custom_settings, False)
        first_resolver_mock.resolve_bundle_version.assert_called_with('bundle')
        second_resolver_mock.resolve_bundle_version.assert_called_with('bundle')

    def test_resolve_bundle_version_success_offline(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.resolve_bundle_version = MagicMock(return_value=None)

        second_resolver_mock = Mock()
        resolved_version = {'test': 'only'}
        second_resolver_mock.resolve_bundle_version = MagicMock(return_value=resolved_version)

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock, second_resolver_mock])

        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            result = resolver.resolve_bundle_version(custom_settings, 'bundle', offline_mode=True)
            self.assertEqual(resolved_version, result)

        resolver_chain_mock.assert_called_with(custom_settings, True)
        first_resolver_mock.resolve_bundle_version.assert_called_with('bundle')
        second_resolver_mock.resolve_bundle_version.assert_called_with('bundle')

    def test_resolve_bundle_version_failure(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.resolve_bundle_version = MagicMock(return_value=None)

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            self.assertRaises(BundleResolutionError, resolver.resolve_bundle_version, custom_settings, 'bundle')

        resolver_chain_mock.assert_called_with(custom_settings, False)
        first_resolver_mock.resolve_bundle_version.assert_called_with('bundle')


class TestResolverContinuousDeliveryUri(TestCase):
    resolved_version = {
        'test': 'only'
    }

    def test_success(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.continuous_delivery_uri = MagicMock(return_value=None)

        resolved_cd_url = 'http://test'

        second_resolver_mock = Mock()
        second_resolver_mock.continuous_delivery_uri = MagicMock(return_value=resolved_cd_url)

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock, second_resolver_mock])

        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            result = resolver.continuous_delivery_uri(custom_settings, self.resolved_version)
            self.assertEqual(resolved_cd_url, result)

        resolver_chain_mock.assert_called_with(custom_settings, False)
        first_resolver_mock.continuous_delivery_uri.assert_called_with(self.resolved_version)
        second_resolver_mock.continuous_delivery_uri.assert_called_with(self.resolved_version)

    def test_success_offline(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.continuous_delivery_uri = MagicMock(return_value=None)

        resolved_cd_url = 'http://test'

        second_resolver_mock = Mock()
        second_resolver_mock.continuous_delivery_uri = MagicMock(return_value=resolved_cd_url)

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock, second_resolver_mock])

        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            result = resolver.continuous_delivery_uri(custom_settings, self.resolved_version, offline_mode=True)
            self.assertEqual(resolved_cd_url, result)

        resolver_chain_mock.assert_called_with(custom_settings, True)
        first_resolver_mock.continuous_delivery_uri.assert_called_with(self.resolved_version)
        second_resolver_mock.continuous_delivery_uri.assert_called_with(self.resolved_version)

    def test_not_found(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.continuous_delivery_uri = MagicMock(return_value=None)

        second_resolver_mock = Mock()
        second_resolver_mock.continuous_delivery_uri = MagicMock(return_value=None)

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock, second_resolver_mock])

        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock):
            self.assertRaises(ContinuousDeliveryError, resolver.continuous_delivery_uri, custom_settings,
                              self.resolved_version)

        resolver_chain_mock.assert_called_with(custom_settings, False)
        first_resolver_mock.continuous_delivery_uri.assert_called_with(self.resolved_version)
        second_resolver_mock.continuous_delivery_uri.assert_called_with(self.resolved_version)


class TestResolverChain(TestCase):
    def test_custom_resolver_chain(self):
        custom_settings = ConfigFactory.parse_string(
            strip_margin("""|resolvers = [
                            |   conductr_cli.resolvers.uri_resolver
                            |]
                            |""")
        )

        get_logger_mock, log_mock = create_mock_logger()

        with patch('logging.getLogger', get_logger_mock):
            result = resolver.resolver_chain(custom_settings, False)
            expected_result = [uri_resolver]
            self.assertEqual(expected_result, result)

        get_logger_mock.assert_called_with('conductr_cli.resolver')
        log_mock.info.assert_called_with('Using custom bundle resolver chain [\'conductr_cli.resolvers.uri_resolver\']')

    def test_none_input(self):
        result = resolver.resolver_chain(None, False)
        expected_result = [stdin_resolver, uri_resolver, bintray_resolver, docker_resolver]
        self.assertEqual(expected_result, result)

    def test_custom_settings_no_resolver_config(self):
        custom_settings = ConfigFactory.parse_string(
            strip_margin("""|dummy = foo
                            |""")
        )
        result = resolver.resolver_chain(custom_settings, False)
        expected_result = [stdin_resolver, uri_resolver, bintray_resolver, docker_resolver]
        self.assertEqual(expected_result, result)

    def test_offline_mode(self):
        result = resolver.resolver_chain(None, True)
        expected_result = [stdin_resolver, offline_resolver, docker_offline_resolver]
        self.assertEqual(expected_result, result)


class TestResolverStdIn(TestCase):
    def test_tty_in(self):
        with patch('sys.stdin.isatty', lambda: True):
            self.assertEqual(
                resolver.stdin_resolver.resolve_bundle('/some/cache/dir', None, None),
                (False, None, None)
            )

    def test_not_used_for_given_file(self):
        with patch('sys.stdin.isatty', lambda: False):
            self.assertEqual(
                resolver.stdin_resolver.resolve_bundle('/some/cache/dir', 'somefile.zip', None),
                (False, None, None)
            )

    def test_file_in(self):
        read_mock = MagicMock(side_effect=[b'hello', b''])

        file = tempfile.NamedTemporaryFile()

        with patch('sys.stdin.isatty', lambda: False), \
                patch('sys.stdin.buffer.read', read_mock),\
                patch('tempfile.NamedTemporaryFile', MagicMock(return_value=file)):
            self.assertEqual(
                resolver.stdin_resolver.resolve_bundle('/some/cache/dir', '-', None),
                (True, None, file.name)
            )

            file.seek(0)

            self.assertEqual(file.read(), b'hello')


class TestResolverDocker(TestCase):
    def test_parse_uri(self):
        self.assertEqual(docker_resolver.parse_uri('alpine'), (
            (None, 'registry.hub.docker.com'),
            (None, 'library'),
            ('alpine', 'alpine'),
            (None, 'latest')
        ))

        self.assertEqual(docker_resolver.parse_uri('alpine:3.5'), (
            (None, 'registry.hub.docker.com'),
            (None, 'library'),
            ('alpine', 'alpine'),
            ('3.5', '3.5')
        ))

        self.assertEqual(docker_resolver.parse_uri('lightbend-docker.registry.bintray.io/conductr/oci-in-docker'), (
            ('lightbend-docker.registry.bintray.io', 'lightbend-docker.registry.bintray.io'),
            ('conductr', 'conductr'),
            ('oci-in-docker', 'oci-in-docker'),
            (None, 'latest')
        ))

        self.assertEqual(docker_resolver.parse_uri('lightbend-docker.registry.bintray.io/conductr/oci-in-docker:0.1'), (
            ('lightbend-docker.registry.bintray.io', 'lightbend-docker.registry.bintray.io'),
            ('conductr', 'conductr'),
            ('oci-in-docker', 'oci-in-docker'),
            ('0.1', '0.1')
        ))

    def test_offline_mode(self):
        mock_is_file = MagicMock(return_value=True)
        mock_json_load = MagicMock(return_value='1234')
        mock_open = MagicMock(return_value=MagicMock())

        with \
                patch('os.path.isfile', mock_is_file), \
                patch('json.load', mock_json_load), \
                patch('builtins.open', mock_open):
            self.assertEqual(
                docker_resolver.fetch_manifest('/tmp', 'registry.hub.docker.com', 'library', 'alpine', '3.5', True),
                '1234'
            )

        mock_is_file.assert_called_once_with('/tmp/docker-manifest-624ab327c0f6bb1039ca62'
                                             '9a2c1ec806514b9194c30491c02e9800254c73d998')

    def test_load_docker_credentials(self):
        with \
                tempfile.NamedTemporaryFile('w') as one, \
                tempfile.NamedTemporaryFile('w') as two, \
                tempfile.NamedTemporaryFile('w') as three:
            one.write('user=one\npassword=one-password')
            one.flush()
            two.write('username=two\npassword=two-password')
            two.flush()
            three.write('hello')
            three.flush()

            with \
                    open(one.name, 'r') as one_in, \
                    patch('os.path.exists', MagicMock(return_value=True)), \
                    patch('builtins.open', MagicMock(return_value=one_in)):
                self.assertEqual(
                    resolver.docker_resolver.load_docker_credentials('test'),
                    ('one', 'one-password')
                )

            with \
                    open(two.name, 'r') as two_in, \
                    patch('os.path.exists', MagicMock(return_value=True)), \
                    patch('builtins.open', MagicMock(return_value=two_in)):
                self.assertEqual(
                    resolver.docker_resolver.load_docker_credentials('test'),
                    ('two', 'two-password')
                )

            with \
                    open(three.name, 'r') as three_in, \
                    patch('os.path.exists', MagicMock(return_value=True)), \
                    patch('builtins.open', MagicMock(return_value=three_in)):
                self.assertEqual(
                    resolver.docker_resolver.load_docker_credentials('test'),
                    None
                )

            path_exists_mock = MagicMock(side_effect=[False, True])

            with \
                    open(one.name, 'r') as one_in, \
                    patch('os.path.exists', path_exists_mock), \
                    MagicMock(return_value=one_in) as open_mock, \
                    patch('builtins.open', open_mock):
                resolver.docker_resolver.load_docker_credentials('test')

                path_exists_mock.assert_has_calls([
                    call('{}-{}'.format(docker_resolver.DOCKER_CREDENTIAL_FILE_PATH, 'test')),
                    call(docker_resolver.DOCKER_CREDENTIAL_FILE_PATH)
                ])
