from aws_cdk import Duration, Stack, aws_ec2 as ec2, CfnOutput
from constructs import Construct

class CdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ## Create Vpc 

        subnet_mask = 24
        vpc_cidr = "10.0.0.0/16"

        self.vpc = ec2.Vpc(
            self,
            "MyVpc",
            vpc_name="server-vpc",
            max_azs=2,
            cidr=vpc_cidr,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public1",
                    cidr_mask=subnet_mask
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public2",
                    cidr_mask=subnet_mask
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Privatewithnat1",
                    cidr_mask=subnet_mask
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Privatewithnat2",
                    cidr_mask=subnet_mask
                )
            ]
        )

        # Create a security group server-sg

        self.server_security_group = ec2.CfnSecurityGroup(
            self, "ServerSecurityGroup",
            group_description="server security group",
            group_name="server-sg",
            vpc_id=self.vpc.vpc_id,
            security_group_ingress=[
                {
                    "ipProtocol": "tcp",
                    "fromPort": 80,
                    "toPort": 80,
                    "cidrIp": "0.0.0.0/0"
                },
                {
                    "ipProtocol": "tcp",
                    "fromPort": 443,
                    "toPort": 443,
                    "cidrIp": "0.0.0.0/0"
                },
                {
                    "ipProtocol": "tcp",
                    "fromPort": 22,
                    "toPort": 22,
                    "cidrIp": "0.0.0.0/0"
                }
            ],
            security_group_egress=[
                {
                    "ipProtocol": "-1",
                    "cidrIp": "0.0.0.0/0"
                }
            ]
        )

        # Create a security group lb-sg
        
        self.lb_security_group = ec2.CfnSecurityGroup(
            self, "LbSecurityGroup",
            group_description="lb security group",
            group_name="lb-sg",
            vpc_id=self.vpc.vpc_id,
            security_group_ingress=[
                {
                    "ipProtocol": "tcp",
                    "fromPort": 80,
                    "toPort": 80,
                    "cidrIp": "0.0.0.0/0"
                },
                {
                    "ipProtocol": "tcp",
                    "fromPort": 22,
                    "toPort": 22,
                    "cidrIp": "0.0.0.0/0"
                }
            ],
            security_group_egress=[
                {
                    "ipProtocol": "-1",
                    "cidrIp": "0.0.0.0/0"
                }
            ]
        )

        

        ## Create Ec2 Instance 

        key_name= "key"

        private_server = ec2.Instance(
            self,
            "private-server",
            instance_name="server01",
            key_name=key_name,
            vpc=self.vpc,
            # vpc_subnets={"subnetId": self.vpc.private_subnets[0].subnet_id},
            security_group=self.server_security_group.ref,
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            
        )

        public_server = ec2.Instance(
            self,
            "public-server",
            instance_name="server02",
            key_name=key_name,
            vpc=self.vpc,
            # vpc_subnets={"subnetId": self.vpc.public_subnets[0].subnet_id},
            security_group=self.server_security_group.ref,
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            
        )

        

