#    Copyright 2017 AT&T Corporation.
#    All Rights Reserved.
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

from oslo_config import cfg

rbac_group = cfg.OptGroup(name='rbac',
                          title='RBAC testing options')

RbacGroup = [
    cfg.StrOpt('rbac_test_role',
               default='admin',
               help="The current RBAC role against which to run"
                    " Patrole tests."),
    cfg.BoolOpt('enable_rbac',
                default=True,
                help="Enables RBAC tests."),
    cfg.BoolOpt('strict_policy_check',
                default=False,
                help="If true, throws RbacParsingException for"
                     " policies which don't exist. If false, "
                     "throws skipException."),
    cfg.StrOpt('cinder_policy_file',
               default='/etc/cinder/policy.json',
               help="Location of the neutron policy file."),
    cfg.StrOpt('glance_policy_file',
               default='/etc/glance/policy.json',
               help="Location of the glance policy file."),
    cfg.StrOpt('keystone_policy_file',
               default='/etc/keystone/policy.json',
               help="Location of the keystone policy file."),
    cfg.StrOpt('neutron_policy_file',
               default='/etc/neutron/policy.json',
               help="Location of the neutron policy file."),
    cfg.StrOpt('nova_policy_file',
               default='/etc/nova/policy.json',
               help="Location of the nova policy file.")
]
