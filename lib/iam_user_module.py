from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from constructs import Construct

class IamUserStack(Stack):
    def __init__(self, scope:  Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM user
        user = iam.User(self, "AdminUser", user_name="mainAdmin")

        user.add_to_group("admin")

        # Add IAM user policies
        user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        user.attach_inline_policy(
            iam.Policy(
                self,
                "MyInlinePolicy",
                statements=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=["s3:ListBucket"],
                        resources=["arn:aws:s3:::my-bucket"]
                    )
                ]
            )
        )
