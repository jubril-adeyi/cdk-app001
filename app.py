#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk import Stack

# from lib.cdk_stack import CdkAppStack
from lib.vpc_module import VpcModule

# Main appStack that calls other modules 


class CdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_module = VpcModule(self, "VpcModule")


app = cdk.App()
CdkAppStack(app, "CdkAppStack")

app.synth()
