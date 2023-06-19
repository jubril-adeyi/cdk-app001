from aws_cdk import Duration, Stack, aws_ec2 as ec2
from constructs import Construct

class CdkAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnet_mask = 24
        vpc_cidr = "10.0.0.0/16"

        vpc = ec2.Vpc(
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

        ## Create IGW in VPC that was created

        igw = ec2.CfnInternetGateway(self, "MyInternetGateway")

        # Attach the Internet Gateway to the VPC
        vpc.add_gateway_attachment(
            "MyGatewayAttachment",
            gateway_id=igw.ref
        )

        
        # Create a Route Table
        route_table = ec2.CfnRouteTable(self, "MyRouteTable", vpc_id=vpc.vpc_id)

        # Create a Route for the IGW
        ec2.CfnRoute(
            self,
            "MyRoute",
            route_table_id=route_table.ref,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=igw.ref
        )

        # Associate subnets with the Route Table
        for subnet in vpc.public_subnets:
            ec2.CfnSubnetRouteTableAssociation(
                self,
                f"{subnet.node.id}RouteTableAssociation",
                subnet_id=subnet.subnet_id,
                route_table_id=route_table.ref
            )
