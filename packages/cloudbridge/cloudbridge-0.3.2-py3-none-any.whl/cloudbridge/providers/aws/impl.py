"""
Provider implementation based on boto library for AWS-compatible clouds.
"""

import os

import boto
from boto.ec2.regioninfo import RegionInfo
from moto.ec2 import mock_ec2
from moto.s3 import mock_s3

from cloudbridge.providers.base import BaseCloudProvider

from .services import AWSBlockStoreService
from .services import AWSComputeService
from .services import AWSImageService
from .services import AWSObjectStoreService
from .services import AWSSecurityService


@mock_ec2
class AWSCloudProviderV1(BaseCloudProvider):

    def __init__(self, config):
        super(AWSCloudProviderV1, self).__init__(config)
        self.cloud_type = 'aws'

        # Initialize cloud connection fields
        self.a_key = self._get_config_value(
            'access_key', os.environ.get('AWS_ACCESS_KEY', None))
        self.s_key = self._get_config_value(
            'secret_key', os.environ.get('AWS_SECRET_KEY', None))
        self.is_secure = self._get_config_value('is_secure', True)
        self.region_name = self._get_config_value('region_name', 'us-east-1')
        self.region_endpoint = self._get_config_value(
            'region_endpoint', 'ec2.us-east-1.amazonaws.com')
        self.ec2_port = self._get_config_value('ec2_port', '')
        self.ec2_conn_path = self._get_config_value('ec2_port', '/')

        # Create a connection object
        self.ec2_conn = self._connect_ec2()
        self.s3_conn = self._connect_s3()

        # Initialize provider services
        self._compute = AWSComputeService(self)
        self._images = AWSImageService(self)
        self._security = AWSSecurityService(self)
        self._block_store = AWSBlockStoreService(self)
        self._object_store = AWSObjectStoreService(self)

    @property
    def compute(self):
        return self._compute

    @property
    def images(self):
        return self._images

    @property
    def security(self):
        return self._security

    @property
    def block_store(self):
        return self._block_store

    @property
    def object_store(self):
        return self._object_store

    def _connect_ec2(self):
        """
        Get a boto ec2 connection object.
        """
        r = RegionInfo(name=self.region_name, endpoint=self.region_endpoint)
        ec2_conn = boto.connect_ec2(
            aws_access_key_id=self.a_key,
            aws_secret_access_key=self.s_key,
            # api_version is needed for availability
            # zone support for EC2
            api_version='2012-06-01' if self.cloud_type == 'aws' else None,
            is_secure=self.is_secure,
            region=r,
            port=self.ec2_port,
            path=self.ec2_conn_path,
            validate_certs=False)
        return ec2_conn

    def _connect_s3(self):
        """
        Get a boto S3 connection object.
        """
        s3_conn = boto.connect_s3(aws_access_key_id=self.a_key,
                                  aws_secret_access_key=self.s_key)
        return s3_conn


class MockAWSCloudProvider(AWSCloudProviderV1):

    def __init__(self, config):
        ec2mock = mock_ec2()
        ec2mock.start()
        s3mock = mock_s3()
        s3mock.start()
        super(MockAWSCloudProvider, self).__init__(config)
