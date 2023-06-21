from constructs import Construct
from aws_cdk import (Stack, 
    aws_ec2 as ec2,
    )

class VpcStack(Stack):
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
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Privatewithnat1",
                    cidr_mask=subnet_mask
                )
            ]
        )

        # Create a security group lb-sg
        self.lb_security_group = ec2.SecurityGroup(
            self, "LbSecurityGroup",
            security_group_name="lb-sg",
            description="lb security group",
            vpc=self.vpc
        )

        self.lb_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(80),
        )

        self.lb_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(22),
        )

        self.lb_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(443),
        )      

        self.lb_security_group.add_egress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.all_traffic(),
        )       


        # Create a security group server-sg


        self.server_security_group = ec2.SecurityGroup(
            self, "ServerSecurityGroup",
            security_group_name="server-sg",
            description="server security group",
            vpc=self.vpc
        )

        self.server_security_group.add_ingress_rule(
            peer=self.lb_security_group,
            connection=ec2.Port.tcp(80),
        )
        self.server_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(22),
        )

        self.server_security_group.add_egress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.all_traffic(),
        )

       