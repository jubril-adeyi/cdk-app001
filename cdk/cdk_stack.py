from constructs import Construct
from aws_cdk import (Duration, 
    Stack, 
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling , 
    aws_elasticloadbalancingv2 as elb)

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
                # ec2.SubnetConfiguration(
                #     subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                #     name="Privatewithnat1",
                #     cidr_mask=subnet_mask
                # ),
                # ec2.SubnetConfiguration(
                #     subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                #     name="Privatewithnat2",
                #     cidr_mask=subnet_mask
                # )
            ]
        )

        # Create a security group server-sg


        self.server_security_group = ec2.SecurityGroup(
            self, "ServerSecurityGroup",
            security_group_name="server-sg",
            description="server security group",
            vpc=self.vpc
        )

        self.server_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(80),
        )

        self.server_security_group.add_ingress_rule(
        peer=ec2.Peer.ipv4("0.0.0.0/0"),
        connection=ec2.Port.tcp(443),
        )   

        self.server_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(22),
        )

        self.server_security_group.add_egress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.all_traffic(),
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

        self.lb_security_group.add_egress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.all_traffic(),
        )       


        # Create a security group server-sg using CfnSecurityGroup

        # self.server_security_group = ec2.CfnSecurityGroup(
        #     self, "ServerSecurityGroup",
        #     group_description="server security group",
        #     group_name="server-sg",
        #     vpc_id=self.vpc.vpc_id,
        #     security_group_ingress=[
        #         {
        #             "ipProtocol": "tcp",
        #             "fromPort": 80,
        #             "toPort": 80,
        #             "cidrIp": "0.0.0.0/0"
        #         },
        #         {
        #             "ipProtocol": "tcp",
        #             "fromPort": 443,
        #             "toPort": 443,
        #             "cidrIp": "0.0.0.0/0"
        #         },
        #         {
        #             "ipProtocol": "tcp",
        #             "fromPort": 22,
        #             "toPort": 22,
        #             "cidrIp": "0.0.0.0/0"
        #         }
        #     ],
        #     security_group_egress=[
        #         {
        #             "ipProtocol": "-1",
        #             "cidrIp": "0.0.0.0/0"
        #         }
        #     ]
        # )

        # # Create a security group lb-sg using CfnSecurityGroup
        
        # self.lb_security_group = ec2.CfnSecurityGroup(
        #     self, "LbSecurityGroup",
        #     group_description="lb security group",
        #     group_name="lb-sg",
        #     vpc_id=self.vpc.vpc_id,
        #     security_group_ingress=[
        #         {
        #             "ipProtocol": "tcp",
        #             "fromPort": 80,
        #             "toPort": 80,
        #             "cidrIp": "0.0.0.0/0"
        #         },
        #         {
        #             "ipProtocol": "tcp",
        #             "fromPort": 22,
        #             "toPort": 22,
        #             "cidrIp": "0.0.0.0/0"
        #         }
        #     ],
        #     security_group_egress=[
        #         {
        #             "ipProtocol": "-1",
        #             "cidrIp": "0.0.0.0/0"
        #         }
        #     ]
        # )

        

        # Create Ec2 Instances
        key_name = "key"  # Replace with your actual key name

        # private_server_1 = ec2.Instance(
        #     self,
        #     "private-server-1",
        #     instance_name="server01",
        #     machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
        #     key_name=key_name,
        #     vpc=self.vpc,
        #     vpc_subnets=ec2.SubnetSelection(subnet_group_name="Privatewithnat1"),
        #     security_group=self.server_security_group,
        #     instance_type=ec2.InstanceType("t2.micro"),
        # )

        # private_server_2 = ec2.Instance(
        #     self,
        #     "private-server-2",
        #     instance_name="server02",
        #     machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
        #     key_name=key_name,
        #     vpc=self.vpc,
        #     vpc_subnets=ec2.SubnetSelection(subnet_group_name="Privatewithnat2"),
        #     security_group=self.server_security_group,
        #     instance_type=ec2.InstanceType("t2.micro"),
        # )

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
            security_group=self.server_security_group,
            instance_type=ec2.InstanceType("t2.micro"),
        )





        ##Set up bastion Host for private instances 

        # # Create a security group bastion-sg
        # self.bastion_sg = ec2.SecurityGroup(
        #     self, "BastionSecurityGroup",
        #     security_group_name="bastion-sg",
        #     description="bastion security group",
        #     vpc=self.vpc
        # )

        # self.bastion_sg.add_ingress_rule(
        #     peer=ec2.Peer.ipv4("0.0.0.0/0"),
        #     connection=ec2.Port.tcp(80),
        # )

        # self.bastion_sg.add_ingress_rule(
        #     peer=ec2.Peer.ipv4("0.0.0.0/0"),
        #     connection=ec2.Port.tcp(22),
        # )   

        # self.bastion_sg.add_egress_rule(
        #     peer=ec2.Peer.ipv4("0.0.0.0/0"),
        #     connection=ec2.Port.all_traffic(),
        # )    
        # ## Create bastion Ec2 instance 
        # bastion_host = ec2.Instance(
        #     self,
        #     "bastion-host",
        #     instance_name="server05",
        #     machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
        #     key_name=key_name,
        #     vpc=self.vpc,
        #     vpc_subnets=ec2.SubnetSelection(subnet_group_name="Public2"),
        #     security_group=self.bastion_sg,
        #     instance_type=ec2.InstanceType("t2.micro"),
        # )

        # ## Create sg for private Instance for bastion access 

        # self.private_bastion_sg = ec2.SecurityGroup(
        #     self, "PrivateBastionSecurityGroup",
        #     security_group_name="private-bastion-sg",
        #     description="private bastion security group",
        #     vpc=self.vpc
        # )

        # self.private_bastion_sg.add_ingress_rule(
        #     peer=self.bastion_sg,
        #     connection=ec2.Port.tcp(22),
        # )   

        # self.private_bastion_sg.add_egress_rule(
        #     peer=ec2.Peer.ipv4("0.0.0.0/0"),
        #     connection=ec2.Port.all_traffic(),
        # )  

        # ## create Private instance 

        # private_bastion = ec2.Instance(
        #     self,
        #     "private-server-3",
        #     instance_name="server06",
        #     machine_image=ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
        #     key_name=key_name,
        #     vpc=self.vpc,
        #     vpc_subnets=ec2.SubnetSelection(subnet_group_name="Privatewithnat2"),
        #     security_group=self.private_bastion_sg,
        #     instance_type=ec2.InstanceType("t2.micro"),
        # )


        ## Setting Up Load Balancer 
        lb = elb.ApplicationLoadBalancer(
            self,
            "load-balancer2227",
            load_balancer_name="server-lb",
            vpc=self.vpc,
            internet_facing=True,
            security_group=self.lb_security_group,
            # vpc_subnets=ec2.SubnetSelection(subnet_group_name=public_subnets_names)
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )






