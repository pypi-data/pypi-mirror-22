# Copyright 2015 - Alcatel-Lucent
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from oslo_config import cfg
from oslo_log import log
from oslo_policy import opts as policy_opts
from vitrage import keystone_client
from vitrage import messaging
from vitrage import opts
from vitrage.opts import register_opts

LOG = log.getLogger(__name__)


def prepare_service(args=None, conf=None, config_files=None):
    if conf is None:
        conf = cfg.ConfigOpts()
    log.register_options(conf)
    policy_opts.set_defaults(conf)

    for group, options in opts.list_opts():
        conf.register_opts(list(options),
                           group=None if group == 'DEFAULT' else group)

    conf(args, project='vitrage', validate_default_values=True,
         default_config_files=config_files)

    for datasource in conf.datasources.types:
        register_opts(conf, datasource, conf.datasources.path)

    keystone_client.register_keystoneauth_opts(conf)

    keystone_client.setup_keystoneauth(conf)
    log.setup(conf, 'vitrage')
    log_levels = [level.replace('keystoneauth=WARN', 'keystoneauth=DEBUG')
                  for level in log.get_default_log_levels()]
    log.set_defaults(default_log_levels=log_levels)
    conf.log_opt_values(LOG, logging.DEBUG)
    messaging.setup()

    return conf
