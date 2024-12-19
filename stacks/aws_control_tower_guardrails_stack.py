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

import importlib
from typing import Dict, Generator, List

import boto3
from aws_cdk import Stack
from aws_cdk.aws_controltower import CfnEnabledControl
from constructs import Construct

from constants import AWS_CONTROL_TOWER_REGION
from constants import GUARDRAILS_CONFIGURATION

ROLE_ARN = getattr(importlib.import_module("constants"), "ROLE_ARN", None)


class AwsControlTowerGuardrailsStack(Stack):
    """
    This stack manages AWS Control Tower Guardrails from
    the configuration GUARDRAILS_CONFIGURATION.
    Guardrails format arn:aws:controlcatalog:::control/<CONTROL_CATALOG_OPAQUE_ID>.
    """

    def __init__(  # type: ignore
        self, scope: Construct, construct_id: str, **kwargs
    ) -> None:
        """
        Initialize the stack that manages AWS Control Tower Guardrails.

        Args:
            scope (Construct): CDK construct
            construct_id (str): construct id
        """
        super().__init__(scope, construct_id, **kwargs)

        self.enable_guardrails()
        self.add_dependencies()

    def chunks(
        self, input_list: List[CfnEnabledControl], num: int
    ) -> Generator[List[CfnEnabledControl], None, None]:
        """
        Yield successive n-sized chunks from an input list.

        Args:
            input_list (List[CfnEnabledControl]): List of CDK construcs CfnEnabledControl
            num (int): Number of chunks

        Yields:
            Generator[List[CfnEnabledControl], None, None]: Generator for the chunked List
                of CDK construcs CfnEnabledControl
        """

        for i in range(0, len(input_list), num):
            yield input_list[i : i + num]

    def get_organizational_unit_arns(
        self, organizational_units_ids: List[str]
    ) -> Dict[str, str]:
        """
        Get organizational unit arn from the id.

        Args:
            organizational_units_ids (List[str]): List of organizational unit ids

        Returns:
            Dict[str, str]: map from organizational unit arn to organizational id
        """

        if ROLE_ARN is not None and ROLE_ARN != "":
            session_name = ROLE_ARN.split("/")[-1][0:64]
            response = boto3.client("sts").assume_role(
                RoleArn=ROLE_ARN, RoleSessionName=session_name
            )
            boto3_session = boto3.session.Session(
                aws_access_key_id=response["Credentials"]["AccessKeyId"],
                aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
                aws_session_token=response["Credentials"]["SessionToken"],
            )
            client = boto3_session.client(
                "organizations", region_name=AWS_CONTROL_TOWER_REGION
            )
        else:
            client = boto3.client("organizations")

        organizational_units_arns = {}

        for organizational_unit_id in organizational_units_ids:

            response = client.describe_organizational_unit(
                OrganizationalUnitId=organizational_unit_id
            )
            organizational_units_arns[response["OrganizationalUnit"]["Arn"]] = (
                organizational_unit_id
            )

        return organizational_units_arns

    def enable_guardrails(self) -> None:
        """
        Construct list of L1 CKD constructs to enable guardrails.

        Raises:
            Exception: Invalid / unsupported guardrail name from the configuration file.
        """

        self.cfn_enabled_controls = []

        for guardrails in GUARDRAILS_CONFIGURATION:

            enable_guardrails = guardrails["Enable-Control"]

            organizational_units_ids = list(guardrails["OrganizationalUnitIds"])
            organizational_units_arns = self.get_organizational_unit_arns(
                organizational_units_ids
            )

            for (
                organizational_unit_arn,
                ou_id,
            ) in organizational_units_arns.items():
                for control_name in enable_guardrails:
                    cfn_enabled_control = CfnEnabledControl(
                        self,
                        f"CfnEnabledControl-{control_name}-{ou_id}",
                        control_identifier=(
                            f"arn:aws:controlcatalog:::control/{control_name}"
                        ),
                        target_identifier=organizational_unit_arn,
                    )
                    self.cfn_enabled_controls.append(cfn_enabled_control)

    def add_dependencies(self) -> None:
        """
        Add resource dependencies to deploy only ten guardrails in parallel
        because of the conncurrency limit in the API.
        """

        # Split the API calls in concurrent chunks
        if len(self.cfn_enabled_controls) % 10 == 0:
            num_chunks = len(self.cfn_enabled_controls) // 10
        else:
            num_chunks = len(self.cfn_enabled_controls) // 10 + 1

        for chunk in self.chunks(self.cfn_enabled_controls, num_chunks):

            # Deploy sequencially each element in the chunk
            for control_i, control_j in zip(chunk, chunk[1:]):
                control_j.node.add_dependency(control_i)
