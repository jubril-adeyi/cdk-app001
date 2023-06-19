from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,


)
from constructs import Construct

class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        subnet_mask= 24
        vpc_cidr= "10.0.0.0/16"


        vpc = ec2.Vpc(
            self,
            "MyVpc",
            vpc_name= "server-vpc",
            cidr='vpc_cidr',
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public1",
                    cidr_mask=subnet_mask
                )]
        )