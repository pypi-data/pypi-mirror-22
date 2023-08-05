# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PolicyDefinition(Model):
    """The policy definition.

    :param policy_type: The type of policy definition. Possible values are
     NotSpecified, BuiltIn, and Custom. Possible values include:
     'NotSpecified', 'BuiltIn', 'Custom'
    :type policy_type: str or :class:`PolicyType
     <azure.mgmt.resource.policy.v2016_12_01.models.PolicyType>`
    :param display_name: The display name of the policy definition.
    :type display_name: str
    :param description: The policy definition description.
    :type description: str
    :param policy_rule: The policy rule.
    :type policy_rule: object
    :param parameters: Required if a parameter is used in policy rule.
    :type parameters: object
    :param id: The ID of the policy definition.
    :type id: str
    :param name: The name of the policy definition. If you do not specify a
     value for name, the value is inferred from the name value in the request
     URI.
    :type name: str
    """

    _attribute_map = {
        'policy_type': {'key': 'properties.policyType', 'type': 'str'},
        'display_name': {'key': 'properties.displayName', 'type': 'str'},
        'description': {'key': 'properties.description', 'type': 'str'},
        'policy_rule': {'key': 'properties.policyRule', 'type': 'object'},
        'parameters': {'key': 'properties.parameters', 'type': 'object'},
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
    }

    def __init__(self, policy_type=None, display_name=None, description=None, policy_rule=None, parameters=None, id=None, name=None):
        self.policy_type = policy_type
        self.display_name = display_name
        self.description = description
        self.policy_rule = policy_rule
        self.parameters = parameters
        self.id = id
        self.name = name
