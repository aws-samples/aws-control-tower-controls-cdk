# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# List of Control Tower Guardrails
# https://docs.aws.amazon.com/controltower/latest/userguide/controltower-ug.pdf

# Organizational Unit Identifier

# The pattern for an organizational unit ID string requires "ou-" followed by
# from 4 to 32 lowercase letters or digits
# (the ID of the root that contains the OU).
# This string is followed by a second "-" dash and from 8 to 32
# additional lowercase letters or digits.


ACCOUNT_ID = "111111111111"
ROLE_ARN = ""
AWS_CONTROL_TOWER_REGION = "eu-west-1"

# pylint: disable=duplicate-code
GUARDRAILS_CONFIGURATION = [
    {
        "Enable-Control": {
            "AWS-GR_ENCRYPTED_VOLUMES",
            "AWS-GR_EBS_OPTIMIZED_INSTANCE",
            "AWS-GR_EC2_VOLUME_INUSE_CHECK",
            "AWS-GR_RDS_INSTANCE_PUBLIC_ACCESS_CHECK",
            "AWS-GR_RDS_SNAPSHOTS_PUBLIC_PROHIBITED",
            "AWS-GR_RDS_STORAGE_ENCRYPTED",
            "AWS-GR_RESTRICTED_COMMON_PORTS",
            "AWS-GR_RESTRICTED_SSH",
            "AWS-GR_RESTRICT_ROOT_USER",
            "AWS-GR_RESTRICT_ROOT_USER_ACCESS_KEYS",
            "AWS-GR_ROOT_ACCOUNT_MFA_ENABLED",
            "AWS-GR_S3_BUCKET_PUBLIC_READ_PROHIBITED",
            "AWS-GR_S3_BUCKET_PUBLIC_WRITE_PROHIBITED",
        },
        "OrganizationalUnitIds": ["ou-1111-11111111"],
    },
    {
        "Enable-Control": {
            "AWS-GR_SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED",
            "AWS-GR_AUTOSCALING_LAUNCH_CONFIG_PUBLIC_IP_DISABLED",
            "AWS-GR_DISALLOW_CROSS_REGION_NETWORKING",
            "AWS-GR_DISALLOW_VPC_INTERNET_ACCESS",
            "AWS-GR_DISALLOW_VPN_CONNECTIONS",
            "AWS-GR_DMS_REPLICATION_NOT_PUBLIC",
            "AWS-GR_EBS_SNAPSHOT_PUBLIC_RESTORABLE_CHECK",
            "AWS-GR_EC2_INSTANCE_NO_PUBLIC_IP",
            "AWS-GR_EKS_ENDPOINT_NO_PUBLIC_ACCESS",
            "AWS-GR_ELASTICSEARCH_IN_VPC_ONLY",
            "AWS-GR_EMR_MASTER_NO_PUBLIC_IP",
            "AWS-GR_LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED",
            "AWS-GR_NO_UNRESTRICTED_ROUTE_TO_IGW",
            "AWS-GR_REDSHIFT_CLUSTER_PUBLIC_ACCESS_CHECK",
            "AWS-GR_S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC",
            "AWS-GR_SAGEMAKER_NOTEBOOK_NO_DIRECT_INTERNET_ACCESS",
            "AWS-GR_SSM_DOCUMENT_NOT_PUBLIC",
        },
        "OrganizationalUnitIds": ["ou-2222-22222222"],
    },
]
