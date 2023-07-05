# Deploying a Kubernetes Application on AWS EKS using terraform

## NTRODUCTION 

In today's software development landscape, containerization has transformed the way applications are managed and deployed. By utilizing the microservices architecture and breaking down applications into independent and lightweight units called containers, developers now have enhanced flexibility and control over different components of their applications. 
Kubernetes, a container orchestration tool, is designed to efficiently manage, modify, and orchestrate containerized applications. It helps with automating various aspects of container management, allowing developers to focus on application logic rather than infrastructure concerns. However, as the complexity of Kubernetes configurations grows, manually managing, modifying, and reproducing them can become bulky and error-prone. This is where infrastructure as code (IaC) tools like Terraform come into play.

Terraform offers a declarative approach to provisioning and managing infrastructure, including Kubernetes configurations. By defining Kubernetes resources and their configurations in Terraform configuration files, developers can version, automate, and easily reproduce these configurations consistently.

This article will delve into the process of provisioning a Kubernetes-based application on AWS EKS using Terraform. 
Combining Container orchestration and infrastructure-as-code to provide a seamlessly automated process for deploying applications with the micro-services approach. 

## Prerequisites 

* An AWS account. 
* IAM user with necessary privileges. 
* Terraform. 
* Some experience with Terraform and Kubernetes. 

## Provisioning Infrastructure on AWS using terraform 

This section is a step-by-step walkthrough of provisioning infrastructure required to deploy applications on Kubernetes using Terraform. 

The steps involved in this walkthrough include: 

* Initializing Terraform 
* Creating S3 bucket and DynamoDB Table as Remote Backend 
* Provisioning Infrastructure for Kubernetes Deployment

###  Initializing terraform 

Initializing terraform includes defining the cloud provider, specifying the IAM credentials in a terraform configuration file and executing the `terraform init` command. 

To Initialize terraform and set up your terraform script follow these steps: 


  1. <b>Create a Terraform Configuration File</b>: Start by creating a new file with the '.tf' extension, such as 'provider.tf' . This file will contain the Terraform configuration code for defining your cloud provider and IAM credentials to initialize Terraform. 
  Specify Cloud Provider: In your Terraform configuration file (provider.tf), specify the cloud provider that will be used.  in this case, you will define AWS as the cloud provider. 

        `provider "aws" {
  region = "us-west-2"  # Replace with your desired AWS region
}
`

  2. <b>Configure IAM Credentials</b> : To authenticate and authorize Terraform to interact with AWS and provision resources, you need to provide IAM credentials. The credentials include an IAM access key ID and a secret access key. 
  There are two standard ways to configure IAM credentials: 
  * <b>Using Provider Configuration Block</b>: Although not recommended as best security practices, You can directly include IAM credentials in the provider configuration block. However, avoid committing such sensitive information to version control or hosting it openly on GitHub.
    `provider "aws" {
  region     = "us-west-2"  # Replace with your desired AWS region
  access_key = "your-access-key-id"
  secret_key = "your-secret-access-key"
    }
        `
   * <b>Using Environment Variables</b>: To set your AWS IAM credentials as environmental variables, open your terminal and execute the following commands:
 ` export AWS_ACCESS_KEY_ID="your-access-key-id"
   export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
    `
    By setting these environmental variables, Terraform will automatically use them for authentication without needing to include 'access_key' and 'secret_key' parameters in your Terraform provider block.

  3. Initializing terraform : Navigate to the directory containing your provider configuration file (provider.tf), open your terminal and and execute the following command: ` terraform init `. This command initialized terraform, downloads all required plugins, preparing your environment for managing infrastructure using terraform.

With  Initialization completed, you can now proceed to creating necessary resources with terraform. 


