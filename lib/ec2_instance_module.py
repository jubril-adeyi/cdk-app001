from constructs import Construct
from aws_cdk import (Stack, 
    aws_ec2 as ec2,
    )
from lib.vpc_module import VpcModule

class Ec2Module(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc_module: VpcModule, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

  # Create Ec2 Instances
        key_name = "key" 

        public_server_1 = ec2.Instance(
            self,
            "public-server-1",
            instance_name="server03",
            machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            key_name=key_name,
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public1"),
            security_group=self.server_security_group,
            instance_type=ec2.InstanceType("t2.micro"), 
        )

        public_server_2 = ec2.Instance(
            self,
            "public-server-2",
            instance_name="server04",
            machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            key_name=key_name,
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public1"),
            security_group=self.server_security_group,
            instance_type=ec2.InstanceType("t2.micro"),
        )


