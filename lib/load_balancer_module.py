from constructs import Construct
from aws_cdk import (Duration, 
    Stack, 
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elb,
    aws_elasticloadbalancingv2_targets as elb_targets
    )

class LoadbalancerModule(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, public_server_1, public_server_2, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    lb_port=80
    
    lb = elb.ApplicationLoadBalancer(
            self,
            "load-balancer2227",
            load_balancer_name="server-lb",
            vpc=vpc,
            internet_facing=True,
            security_group=self.lb_security_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            deletion_protection=None
        )

    ## target group creation

    server_tg = elb.ApplicationTargetGroup(self, 
        "server-tg",
        target_group_name= "server-tg",
        target_type=elb.TargetType.INSTANCE,
        port=lb_port,
        protocol=elb.ApplicationProtocol.HTTP,
        vpc=vpc,
        stickiness_cookie_duration=Duration.seconds(30),
        targets=[
            elb_targets.InstanceIdTarget(public_server_1.instance_id, port=80),
            elb_targets.InstanceIdTarget(public_server_2.instance_id, port=80),
            ]
    )

# Configure health checks for the target group
    server_tg.configure_health_check(
        path="/",  
        interval=Duration.seconds(300),
        timeout=Duration.seconds(60),
        healthy_threshold_count=5,
        unhealthy_threshold_count=5
    )

    # # Set listener to listen to tg

    listener= lb.add_listener("listener",
        port=lb_port,
            protocol=elb.ApplicationProtocol.HTTP,
            default_target_groups=[server_tg]
    )









        