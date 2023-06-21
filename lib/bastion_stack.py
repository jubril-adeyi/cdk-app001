from constructs import Construct
from aws_cdk import (Duration, 
    Stack, 
    aws_ec2 as ec2,
    )

class BastionStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, lb_security_group, server_security_group, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##Set up bastion Host for private instances 

        key_name="key"

        ## Create bastion Ec2 instance 
        bastion_host = ec2.Instance(
            self,
            "bastion-host",
            instance_name="server05",
            machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            key_name=key_name,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public1"),
            security_group=lb_security_group,
            instance_type=ec2.InstanceType("t2.micro"),
        )

        ## create Private instance 

        private_bastion = ec2.Instance(
            self,
            "private-server-1",
            instance_name="privatebastionserver06",
            machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            key_name=key_name,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Privatewithnat1"),
            security_group=server_security_group,
            instance_type=ec2.InstanceType("t2.micro"),
        )
