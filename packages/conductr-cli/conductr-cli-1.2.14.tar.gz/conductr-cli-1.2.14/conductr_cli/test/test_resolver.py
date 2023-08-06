from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
from conductr_cli.test.cli_test_case import strip_margin, create_mock_logger
from conductr_cli.exceptions import BundleResolutionError, ContinuousDeliveryError
from conductr_cli import resolver
from conductr_cli.resolvers import \
    bintray_resolver, docker_resolver, docker_offline_resolver, uri_resolver, offline_resolver, stdin_resolver
from pyhocon import ConfigFactory


class TestResolver(TestCase):

    def test_resolve_bundle_success(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_from_cache = MagicMock(return_value=(False, None, None, None))
        first_resolver_mock.resolve_bundle = MagicMock(return_value=(False, None, None, None))

        second_resolver_mock = Mock()
        second_resolver_mock.load_bundle_from_cache = MagicMock(return_value=(False, None, None, None))
        second_resolver_mock.resolve_bundle = MagicMock(return_value=(True, 'bundle_name', 'mock bundle_file', None))

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

    def test_resolve_bundle_success_with_some_resolver_returning_errors(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_load_bundle_from_cache_error = MagicMock(name='first_resolver_load_bundle_from_cache_error')
        first_resolver_mock.load_bundle_from_cache = MagicMock(
            return_value=(False, None, None, first_resolver_load_bundle_from_cache_error))
        first_resolver_mock.resolve_bundle = MagicMock(return_value=(False, None, None, None))

        second_resolver_mock = Mock()
        second_resolver_load_bundle_from_cache_error = MagicMock(name='second_resolver_load_bundle_from_cache_error')
        second_resolver_mock.load_bundle_from_cache = MagicMock(
            return_value=(False, None, None, second_resolver_load_bundle_from_cache_error))
        second_resolver_mock.resolve_bundle = MagicMock(return_value=(True, 'bundle_name', 'mock bundle_file', None))

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

    def test_resolve_bundle_not_found(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()

        first_resolver_mock.load_bundle_from_cache = MagicMock(return_value=(False, None, None, None))
        first_resolver_mock.resolve_bundle = MagicMock(return_value=(False, None, None, None))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock), \
                self.assertRaises(BundleResolutionError) as e:
            resolver.resolve_bundle(custom_settings, '/some-cache-dir', '/some-bundle-path')

        self.assertEqual([], e.exception.cache_resolution_errors)
        self.assertEqual([], e.exception.bundle_resolution_errors)

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_from_cache('/some-cache-dir', '/some-bundle-path')
        first_resolver_mock.resolve_bundle.assert_called_with('/some-cache-dir', '/some-bundle-path')

    def test_resolve_bundle_error(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_load_bundle_from_cache_error = MagicMock(name='first_resolver_load_bundle_from_cache_error')
        first_resolver_mock.load_bundle_from_cache = MagicMock(
            return_value=(False, None, None, first_resolver_load_bundle_from_cache_error))
        first_resolver_mock.resolve_bundle = MagicMock(return_value=(False, None, None, None))

        second_resolver_mock = Mock()
        second_resolver_load_bundle_from_cache_error = MagicMock(name='second_resolver_load_bundle_from_cache_error')
        second_resolver_mock.load_bundle_from_cache = MagicMock(
            return_value=(False, None, None, second_resolver_load_bundle_from_cache_error))
        second_resolver_resolve_bundle_error = MagicMock(name='second_resolver_resolve_bundle_error')
        second_resolver_mock.resolve_bundle = MagicMock(
            return_value=(False, None, None, second_resolver_resolve_bundle_error))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock, second_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock), \
                self.assertRaises(BundleResolutionError) as e:
            resolver.resolve_bundle(custom_settings, '/some-cache-dir', '/some-bundle-path')

        self.assertEqual([
            (first_resolver_mock, first_resolver_load_bundle_from_cache_error),
            (second_resolver_mock, second_resolver_load_bundle_from_cache_error),
        ], e.exception.cache_resolution_errors)

        self.assertEqual([
            (second_resolver_mock, second_resolver_resolve_bundle_error),
        ], e.exception.bundle_resolution_errors)

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_from_cache('/some-cache-dir', '/some-bundle-path')
        first_resolver_mock.resolve_bundle.assert_called_with('/some-cache-dir', '/some-bundle-path')

    def test_resolve_bundle_from_cache(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_from_cache = MagicMock(return_value=(True, 'bundle_name', 'mock bundle_file', None))

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
        first_resolver_mock.load_bundle_configuration_from_cache = MagicMock(return_value=(False, None, None, None))
        first_resolver_mock.resolve_bundle_configuration = MagicMock(return_value=(False, None, None, None))

        second_resolver_mock = Mock()
        second_resolver_mock.load_bundle_configuration_from_cache = MagicMock(return_value=(False, None, None, None))
        second_resolver_mock.resolve_bundle_configuration = MagicMock(return_value=(True, 'bundle_name',
                                                                                    'mock bundle_file', None))

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
        first_resolver_mock.load_bundle_configuration_from_cache = MagicMock(return_value=(False, None, None, None))
        first_resolver_mock.resolve_bundle_configuration = MagicMock(return_value=(False, None, None, None))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock), \
                self.assertRaises(BundleResolutionError) as e:
            resolver.resolve_bundle_configuration(custom_settings, '/some-cache-dir', '/some-bundle-path')

        self.assertEqual([], e.exception.cache_resolution_errors)
        self.assertEqual([], e.exception.bundle_resolution_errors)

        resolver_chain_mock.assert_called_with(custom_settings, False)

        first_resolver_mock.load_bundle_configuration_from_cache('/some-cache-dir', '/some-bundle-path')
        first_resolver_mock.resolve_bundle_configuration.assert_called_with('/some-cache-dir', '/some-bundle-path')

    def test_resolve_bundle_configuration_from_cache(self):
        custom_settings = Mock()

        first_resolver_mock = Mock()
        first_resolver_mock.load_bundle_configuration_from_cache = MagicMock(return_value=(True, 'bundle_name',
                                                                                           'mock bundle_file', None))

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
        first_resolver_mock.resolve_bundle_version = MagicMock(return_value=(None, None))

        second_resolver_mock = Mock()
        resolved_version = {'test': 'only'}
        second_resolver_mock.resolve_bundle_version = MagicMock(return_value=(resolved_version, None))

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
        first_resolver_mock.resolve_bundle_version = MagicMock(return_value=(None, None))

        second_resolver_mock = Mock()
        resolved_version = {'test': 'only'}
        second_resolver_mock.resolve_bundle_version = MagicMock(return_value=(resolved_version, None))

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
        first_resolver_mock.resolve_bundle_version = MagicMock(return_value=(None, None))

        resolver_chain_mock = MagicMock(return_value=[first_resolver_mock])
        with patch('conductr_cli.resolver.resolver_chain', resolver_chain_mock),\
                self.assertRaises(BundleResolutionError) as e:
            resolver.resolve_bundle_version(custom_settings, 'bundle')

        self.assertEqual([], e.exception.cache_resolution_errors)
        self.assertEqual([], e.exception.bundle_resolution_errors)
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
