from conductr_cli.exceptions import MalformedBundleUriError


DEFAULT_ORG = 'typesafe'
DEFAULT_REPO_BUNDLE = 'bundle'
DEFAULT_REPO_BUNDLE_CONFIGURATION = 'bundle-configuration'


def parse_bundle(uri):
    urn, rest = split_to_urn_and_rest(uri)
    org, repo, package = split_to_org_repo_package(rest, default_repo=DEFAULT_REPO_BUNDLE)
    package_name, tag, digest = split_package_to_parts(package)
    return urn, org, repo, package_name, tag, digest


def parse_bundle_configuration(uri):
    urn, rest = split_to_urn_and_rest(uri)
    org, repo, package = split_to_org_repo_package(rest, default_repo=DEFAULT_REPO_BUNDLE_CONFIGURATION)
    package_name, tag, digest = split_package_to_parts(package)
    return urn, org, repo, package_name, tag, digest


def split_to_urn_and_rest(uri):
    if uri.startswith('urn:'):
        if uri.startswith('urn:x-bundle:'):
            return 'urn:x-bundle:', uri.replace('urn:x-bundle:', '')
        else:
            raise MalformedBundleUriError('{} is not a valid bundle uri'.format(uri))
    else:
        return 'urn:x-bundle:', uri


def split_to_org_repo_package(uri, default_repo):
    parts = uri.split('/')
    if len(parts) == 3:
        return parts
    elif len(parts) == 2:
        return DEFAULT_ORG, parts[0], parts[1]
    elif len(parts) == 1:
        return DEFAULT_ORG, default_repo, parts[0]
    else:
        raise MalformedBundleUriError('{} is not a valid bundle uri'.format(uri))


def split_package_to_parts(package):
    if ':' in package:
        package_name, version = package.split(':')
        if '-' in version:
            tag, digest = version.rsplit('-', 1)
            return package_name, tag, digest
        else:
            return package_name, version, None
    else:
        return package, None, None
