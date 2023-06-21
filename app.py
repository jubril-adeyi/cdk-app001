#!/usr/bin/env python3
import os
import aws_cdk as cdk
# from aws_cdk import Stack
# from constructs import Construct

# from lib import neccesary modules
from lib.vpc_module import VpcStack
from lib.ec2_instance_module import Ec2InstanceStack
from lib.load_balancer_module import AppLoadBalancerStack
from lib.bastion_stack import BastionStack
from lib.iam_user_module import IamUserStack

app = cdk.App()

# Instantiate VpcStack
vpc_stack = VpcStack(app, "VpcStack")

# Instantiate Ec2InstanceStack and pass the VPC and server security group
ec2_stack = Ec2InstanceStack(app, "Ec2InstanceStack",
     vpc=vpc_stack.vpc,
     server_security_group=vpc_stack.server_security_group
     )
ec2_stack.add_dependency(vpc_stack)

# Instantiate AppLoadBalancerStack pass the VPC and server security group
load_balancer_stack=AppLoadBalancerStack(app,"AppLoadBalancerStack", 
     vpc=vpc_stack.vpc,
     lb_security_group=vpc_stack.lb_security_group,
     public_server_1=ec2_stack.public_server_1, 
     public_server_2=ec2_stack.public_server_2
     )

load_balancer_stack.add_dependency(ec2_stack)

bastion_stack = BastionStack(app, "BastionStack", 
    vpc=vpc_stack.vpc,
    lb_security_group=vpc_stack.lb_security_group,
    server_security_group=vpc_stack.server_security_group
    )

# # Add more modules/stacks as needed
app.synth()
