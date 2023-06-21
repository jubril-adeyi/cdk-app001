#!/usr/bin/env python3
import os
import aws_cdk as cdk
from aws_cdk import Stack
from constructs import Construct

# from lib import neccesary modules
from lib.vpc_module import VpcModule
from lib.ec2_instance_module import Ec2Module

# Main appStack that calls other modules 
class CdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_module = VpcModule(self, "VpcModule")

        ec2_instance_module=Ec2Module(self,"Ec2Module", vpc_module.vpc)






app = cdk.App()
CdkAppStack(app, "CdkAppStack")

app.synth()
