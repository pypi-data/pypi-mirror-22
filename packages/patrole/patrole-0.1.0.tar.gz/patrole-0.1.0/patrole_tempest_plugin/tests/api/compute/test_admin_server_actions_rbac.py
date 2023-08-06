# Copyright 2017 AT&T Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest import config
from tempest.lib import decorators
from tempest import test

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.compute import rbac_base

CONF = config.CONF


class AdminServerActionsRbacTest(rbac_base.BaseV2ComputeRbacTest):

    @classmethod
    def skip_checks(cls):
        super(AdminServerActionsRbacTest, cls).skip_checks()
        if not test.is_extension_enabled('os-admin-actions', 'compute'):
            msg = "%s skipped as os-admin-actions not enabled." % cls.__name__
            raise cls.skipException(msg)

    @classmethod
    def resource_setup(cls):
        super(AdminServerActionsRbacTest, cls).resource_setup()
        cls.server_id = cls.create_test_server(wait_until='ACTIVE')['id']

    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-admin-actions:reset_state")
    @decorators.idempotent_id('ae84dd0b-f364-462e-b565-3457f9c019ef')
    def test_reset_server_state(self):
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.servers_client.reset_state(self.server_id, state='error')
        self.addCleanup(self.servers_client.reset_state,
                        self.server_id,
                        state='active')

    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-admin-actions:inject_network_info")
    @decorators.idempotent_id('ce48c340-51c1-4cff-9b6e-0cc5ef008630')
    def test_inject_network_info(self):
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.servers_client.inject_network_info(self.server_id)

    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-admin-actions:reset_network")
    @decorators.idempotent_id('2911a242-15c4-4fcb-80d5-80a8930661b0')
    def test_reset_network(self):
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.servers_client.reset_network(self.server_id)
