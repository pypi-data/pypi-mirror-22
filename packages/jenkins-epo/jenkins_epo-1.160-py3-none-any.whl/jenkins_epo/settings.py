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

import logging
import os

from .utils import Bunch


logger = logging.getLogger(__name__)


class EnvironmentSettings(Bunch):
    def __init__(self, defaults):
        logger.debug("Global settings:")
        self.load(defaults)
        logger.debug("Environment loaded.")

    def load(self, defaults):
        for k, v in sorted(defaults.items()):
            needles = [k, 'GHP_' + k, 'EPO_' + k]
            for needle in needles:
                v = os.environ.get(needle, v)

            try:
                v = int(v)
            except (TypeError, ValueError):
                pass
            self[k] = v

            if 'TOKEN' in k:
                v = v[:8] if v and len(v) > 8 else 'X' * 8

            logger.debug("%s=%r", k, v)


DEFAULTS = {
    # Max item count in queue to enqueue new.
    'QUEUE_MAX': 32,
    'CACHE_PATH': '.epo-cache',
    'CACHE_LIFE': 30,
    # Size of worker pool
    'CONCURRENCY': 4,
    # Drop into Pdb on unhandled exception
    'DEBUG': False,
    # Do not trigger jobs nor touch GitHub statuses.
    'DRY_RUN': False,
    'EXTENSIONS': '*',
    # Whether to touch GitHub statuses or not
    'GITHUB_RO': False,
    # Webhook HMAC secret
    'GITHUB_SECRET': None,
    'GITHUB_TOKEN': None,
    'HEADS': '*',
    'HOST': '0.0.0.0',
    'IGNORE_STATUSES': '',
    'JOBS': '',
    # When commenting on PR
    'NAME': 'Jenkins EPO',
    'POLL_INTERVAL': 600,
    'PORT': 2819,
    'RATE_LIMIT_THRESHOLD': 50,
    # List repositories: owner/repo1,owner/repo2
    'REPOSITORIES': '',
    'SERVER_URL': 'http://localhost:2819',
    'URGENT': '[urgent*,[hotfix*,hotfix*',
    'VERBOSE': '',
    # Jenkins baseurl, like http://jenkins.lan:8080/.
    'JENKINS_URL': '',
    'JENKINS_QUEUE': '*',
}

SETTINGS = EnvironmentSettings(defaults=DEFAULTS)
