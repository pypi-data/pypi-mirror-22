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


class ResourceGroup(Model):
    """Resource group information.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: The ID of the resource group.
    :vartype id: str
    :param name: The Name of the resource group.
    :type name: str
    :param properties:
    :type properties: :class:`ResourceGroupProperties
     <azure.mgmt.resource.resources.v2016_02_01.models.ResourceGroupProperties>`
    :param location: The location of the resource group. It cannot be changed
     after the resource group has been created. Has to be one of the supported
     Azure Locations, such as West US, East US, West Europe, East Asia, etc.
    :type location: str
    :param tags: The tags attached to the resource group.
    :type tags: dict
    """

    _validation = {
        'id': {'readonly': True},
        'location': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'ResourceGroupProperties'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
    }

    def __init__(self, location, name=None, properties=None, tags=None):
        self.id = None
        self.name = name
        self.properties = properties
        self.location = location
        self.tags = tags
