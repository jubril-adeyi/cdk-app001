#!/usr/bin/env python3
import os
import aws_cdk as cdk
# from aws_cdk import Stack
# from constructs import Construct

# from lib import neccesary modules
from lib.vpc_module import VpcModule
from lib.ec2_instance_module import Ec2Module
from lib.load_balancer_module import LoadBalancerModule


app = cdk.App()

# Instantiate VpcModule
vpc_module = VpcModule(app, "VpcModule")

# Instantiate Ec2Module and pass the VPC and server security group
ec2_module = Ec2Module(app, "Ec2Module", vpc=vpc_module.vpc, server_security_group=vpc_module.server_security_group)
ec2_module.add_dependency(vpc_module)

# Instantiate LoadBalancerModule pass the VPC and server security group
load_balancer_module=LoadBalancerModule(app,"LbModule", 
     vpc=vpc_module.vpc,
     lb_security_group=vpc_module.lb_security_group,
     public_server_1=ec2_module.public_server_1, 
     public_server_2=ec2_module.public_server_2)

load_balancer_modulee.add_dependency(ec2_module)


# # Add more modules/stacks as needed
app.synth()
