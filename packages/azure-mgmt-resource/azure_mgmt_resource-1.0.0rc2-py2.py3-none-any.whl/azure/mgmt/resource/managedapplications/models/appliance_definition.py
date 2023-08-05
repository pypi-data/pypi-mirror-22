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

from .generic_resource import GenericResource


class ApplianceDefinition(GenericResource):
    """Information about appliance definition.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: Resource ID
    :vartype id: str
    :ivar name: Resource name
    :vartype name: str
    :ivar type: Resource type
    :vartype type: str
    :param location: Resource location
    :type location: str
    :param tags: Resource tags
    :type tags: dict
    :param managed_by: ID of the resource that manages this resource.
    :type managed_by: str
    :param sku: The SKU of the resource.
    :type sku: :class:`Sku
     <azure.mgmt.resource.managedapplications.models.Sku>`
    :param identity: The identity of the resource.
    :type identity: :class:`Identity
     <azure.mgmt.resource.managedapplications.models.Identity>`
    :param lock_level: The appliance lock level. Possible values include:
     'CanNotDelete', 'ReadOnly', 'None'
    :type lock_level: str or :class:`ApplianceLockLevel
     <azure.mgmt.resource.managedapplications.models.ApplianceLockLevel>`
    :param display_name: The appliance definition display name.
    :type display_name: str
    :param authorizations: The appliance provider authorizations.
    :type authorizations: list of :class:`ApplianceProviderAuthorization
     <azure.mgmt.resource.managedapplications.models.ApplianceProviderAuthorization>`
    :param artifacts: The collection of appliance artifacts. The portal will
     use the files specified as artifacts to construct the user experience of
     creating an appliance from an appliance definition.
    :type artifacts: list of :class:`ApplianceArtifact
     <azure.mgmt.resource.managedapplications.models.ApplianceArtifact>`
    :param description: The appliance definition description.
    :type description: str
    :param package_file_uri: The appliance definition package file Uri.
    :type package_file_uri: str
    """

    _validation = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'type': {'readonly': True},
        'lock_level': {'required': True},
        'authorizations': {'required': True},
        'package_file_uri': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'managed_by': {'key': 'managedBy', 'type': 'str'},
        'sku': {'key': 'sku', 'type': 'Sku'},
        'identity': {'key': 'identity', 'type': 'Identity'},
        'lock_level': {'key': 'properties.lockLevel', 'type': 'ApplianceLockLevel'},
        'display_name': {'key': 'properties.displayName', 'type': 'str'},
        'authorizations': {'key': 'properties.authorizations', 'type': '[ApplianceProviderAuthorization]'},
        'artifacts': {'key': 'properties.artifacts', 'type': '[ApplianceArtifact]'},
        'description': {'key': 'properties.description', 'type': 'str'},
        'package_file_uri': {'key': 'properties.packageFileUri', 'type': 'str'},
    }

    def __init__(self, lock_level, authorizations, package_file_uri, location=None, tags=None, managed_by=None, sku=None, identity=None, display_name=None, artifacts=None, description=None):
        super(ApplianceDefinition, self).__init__(location=location, tags=tags, managed_by=managed_by, sku=sku, identity=identity)
        self.lock_level = lock_level
        self.display_name = display_name
        self.authorizations = authorizations
        self.artifacts = artifacts
        self.description = description
        self.package_file_uri = package_file_uri
