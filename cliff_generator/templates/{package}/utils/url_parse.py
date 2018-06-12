import os

from six.moves.urllib import parse


def path_join(base, *urls):
    def _path_join(base, url):
        if not base.endswith('/'):
            base += '/'
        return parse.urljoin(base, url)

    urls = (base,) + urls
    return reduce(_path_join, urls)


def query_join(base, **queries):
    return base + '?' + parse.urlencode(queries)


def resource_join(*url):
    testapi_url = os.environ.get('testapi_url')
    return path_join(testapi_url, *url)


def get_queries(queries, parsed_args):
    if not isinstance(queries, list):
        queries = [queries]

    return {query: getattr(parsed_args, query)
            for query in queries
            if hasattr(parsed_args, query) and getattr(parsed_args, query)}


def query_by(base, queries, parsed_args):
    qs = get_queries(queries, parsed_args)
    return query_join(base, **qs) if qs else base


def url_format(base, parsed_args):
    return base.format(**(parsed_args.__dict__))
