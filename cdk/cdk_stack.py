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

        

        # Create Ec2 Instances
        key_name = "key"  # Replace with your actual key name

        private_server_1 = ec2.Instance(
            self,
            "private-server-1",
            instance_name="server01",
            machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            key_name=key_name,
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Privatewithnat1"),
            security_group=self.server_security_group.ref,
            instance_type=ec2.InstanceType("t2.micro"),
        )

        private_server_2 = ec2.Instance(
            self,
            "private-server-2",
            instance_name="server02",
            machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            key_name=key_name,
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Privatewithnat2"),
            security_group=self.server_security_group,
            instance_type=ec2.InstanceType("t2.micro"),
        )

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
            vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public2"),
            security_group=self.server_security_group.ref,
            instance_type=ec2.InstanceType("t2.micro"),
        )

        

