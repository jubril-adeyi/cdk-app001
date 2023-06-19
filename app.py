#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkAppStack


app = cdk.App()
CdkAppStack(app, "CdkAppStack")

app.synth()
