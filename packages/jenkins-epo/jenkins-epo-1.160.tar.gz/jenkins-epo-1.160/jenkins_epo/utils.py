# This file is part of jenkins-epo
#
# jenkins-epo is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# jenkins-epo is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# jenkins-epo.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import asyncio
import aiohttp.errors
import pdb
import collections
from concurrent.futures import TimeoutError
from datetime import datetime, timedelta, timezone
import fnmatch
import logging
import re
import sys

from github import ApiError
from http.client import HTTPException
import tenacity
from requests import HTTPError


logger = logging.getLogger(__name__)


def utcnow():
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def retry(callable_):
    defaults = dict(
        retry=tenacity.retry_if_exception(filter_exception_for_retry),
        wait=tenacity.wait_exponential(max=300),
    )
    return tenacity.retry(**defaults)(callable_)


_retryable_exception = (
    IOError,
    HTTPException,
    HTTPError,
    TimeoutError,
)


def filter_exception_for_retry(exception):
    from .github import wait_rate_limit_reset

    if isinstance(exception, ApiError):
        try:
            message = exception.response['json']['message']
        except KeyError:
            # Don't retry on ApiError by default. Things like 1000 status
            # update must be managed by code.
            return False
        if 'API rate limit exceeded for' in message:
            wait_rate_limit_reset(utcnow())
            return True
        # If not a rate limit error, don't retry.
        return False

    if isinstance(exception.__cause__, aiohttp.errors.ServerDisconnectedError):
        logger.debug("Retrying on server disconnect.")
        return True

    if not isinstance(exception, _retryable_exception):
        return False

    if isinstance(exception, HTTPError):
        if exception.response.status_code < 500:
            return False

    logger.warn(
        "Retrying on %r: %s",
        type(exception), str(exception) or repr(exception)
    )
    return True


def log_context(instance):
    task = asyncio.Task.current_task()
    if not task:
        return

    if hasattr(instance, 'sha'):
        task.logging_id = str(instance.sha)[:4]
        return


def format_duration(duration):
    duration = timedelta(seconds=duration / 1000.)
    h, m, s = str(duration).split(':')
    h, m, s = int(h), int(m), float(s)
    duration = '%.1f sec' % s
    if h or m:
        duration = '%d min %s' % (m, duration)
    if h:
        duration = '%d h %s' % (h, duration)
    return duration.replace('.0', '')


def match(item, patterns):
    matched = not patterns
    for pattern in filter(None, patterns):
        negate = False
        if pattern.startswith('-') or pattern.startswith('!'):
            negate = True
            pattern = pattern[1:]
        if pattern.startswith('+'):
            pattern = pattern[1:]

        local_matched = fnmatch.fnmatch(item, pattern)
        if negate:
            matched = matched and not local_matched
        else:
            matched = matched or local_matched

    return matched


def parse_datetime(formatted):
    return datetime.strptime(formatted, '%Y-%m-%dT%H:%M:%SZ')


_link_re = re.compile(r'<(?P<url>.*?)>; rel="(?P<rel>.*?)"')


def parse_links(data):
    return {
        m.group('rel'): m.group('url')
        for m in
        _link_re.finditer(data)
    }


def parse_patterns(raw):
    return [p for p in str(raw).split(',') if p]


def post_mortem():
    pdb.post_mortem(sys.exc_info()[2])
    logger.debug('Graceful exit from debugger.')


class Bunch(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def deepupdate(self, other):
    for k, v in other.items():
        if isinstance(v, collections.Mapping):
            r = deepupdate(self.get(k, {}), v)
            self[k] = r
        else:
            self[k] = other[k]
    return self


@asyncio.coroutine
def switch_coro(_seconds=.005):
    """Tiny helper lettting loop switch to another coroutine."""
    yield from asyncio.sleep(_seconds)
