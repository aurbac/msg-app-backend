# Use ECS CLI to deploy the backend application

Work inside your AWS Cloud9 or local environment.

## Configure your environment

``` bash
aws configure
```

- In AWS Cloud9 configure the AWS CLI as follows. 
    - AWS Access Key ID: **(Use default)**
    - AWS Secret Access Key: **(Use default)**
    - Default region name [us-east-1]: **us-east-1**
    - Default output format [json]: **json**
- In your local environment [configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration) with your own IAM credentials.

## Install the Amazon ECS CLI

Install the Amazon ECS CLI on your Linux or macOS environment.

``` bash
sudo curl -o /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
sudo chmod +x /usr/local/bin/ecs-cli
ecs-cli --version
```

Reference: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html

## Clone the project

``` bash
git clone https://github.com/aurbac/msg-app-backend.git
cd msg-app-backend/
```

Install JQ command.

``` bash
sudo yum install jq
```

## Create an Amazon VPC with AWS CloudFormation

Create a simple DynamoDB table to store the messages for our application, by executing the following command the table is created using AWS CloudFormation.

``` bash
aws cloudformation create-stack --stack-name MsgApp --template-body file://db/msg-app-dynamodb.json --parameters ParameterKey=BillOnDemand,ParameterValue=true ParameterKey=ReadCapacityUnits,ParameterValue=5 ParameterKey=WriteCapacityUnits,ParameterValue=10
```

``` bash
export MY_TABLE_NAME=`aws cloudformation describe-stacks --stack-name MsgApp | jq '.Stacks[0].Outputs[0].OutputValue' | tr -d \"`
echo $MY_TABLE_NAME
```

``` bash
python db/batch_writing.py
```

## Create an Amazon VPC with AWS CloudFormation

``` bash
aws cloudformation create-stack --stack-name MyVPC --template-body file://vpc/AURBAC-VPC-Public-And-Private.json --parameters ParameterKey=VpcCidrBlock,ParameterValue=10.1.0.0/16 ParameterKey=VpcCidrBlockPrivateSubnet01,ParameterValue=10.1.2.0/24 ParameterKey=VpcCidrBlockPrivateSubnet02,ParameterValue=10.1.3.0/24 ParameterKey=VpcCidrBlockPublicSubnet01,ParameterValue=10.1.0.0/24 ParameterKey=VpcCidrBlockPublicSubnet02,ParameterValue=10.1.1.0/24
```

!!! info
    Wait about 5 minutes until the CloufFormation Stack status is **CREATE_COMPLETE**, got to your AWS CloudFormation console https://console.aws.amazon.com/cloudformation.

``` bash
export VPC_ID=`aws cloudformation describe-stack-resources --stack-name MyVPC --logical-resource-id Vpc | jq '.StackResources[0].PhysicalResourceId' | tr -d \"`
export PRIVATE_SUBNET_01=`aws cloudformation describe-stack-resources --stack-name MyVPC --logical-resource-id PrivateSubnet01 | jq '.StackResources[0].PhysicalResourceId' | tr -d \"`
export PRIVATE_SUBNET_02=`aws cloudformation describe-stack-resources --stack-name MyVPC --logical-resource-id PrivateSubnet02 | jq '.StackResources[0].PhysicalResourceId' | tr -d \"`
export PUBLIC_SUBNET_01=`aws cloudformation describe-stack-resources --stack-name MyVPC --logical-resource-id PublicSubnet01 | jq '.StackResources[0].PhysicalResourceId' | tr -d \"`
export PUBLIC_SUBNET_02=`aws cloudformation describe-stack-resources --stack-name MyVPC --logical-resource-id PublicSubnet02 | jq '.StackResources[0].PhysicalResourceId' | tr -d \"`
echo $VPC_ID
echo $PRIVATE_SUBNET_01
echo $PRIVATE_SUBNET_02
echo $PUBLIC_SUBNET_01
echo $PUBLIC_SUBNET_02
```

## Create the Application Load Balancer using the AWS CLI

### Create a Security Group for your Application Load Balancer

``` bash
export SG_API_ALB=`aws ec2 create-security-group --group-name "api-alb" --description "ALB Security Group" --vpc-id $VPC_ID | jq '.GroupId' | tr -d \"`
aws ec2 authorize-security-group-ingress --group-id $SG_API_ALB --protocol tcp --port 80 --cidr 0.0.0.0/0
```

### Create an Application Load Balancer

``` bash
export LOAD_BALANCER_ARN=`aws elbv2 create-load-balancer --name backend-api --type application --security-groups $SG_API_ALB --subnets $PUBLIC_SUBNET_01 $PUBLIC_SUBNET_02 | jq '.LoadBalancers[0].LoadBalancerArn' | tr -d \"`
```

### Create a Target Group for your Application Load Balancer

``` bash
export TARGET_GROUP_ARN=`aws elbv2 create-target-group --name my-target-alb --protocol HTTP --port 80 --health-check-protocol HTTP --health-check-path /api --vpc-id $VPC_ID --target-type ip | jq '.TargetGroups[0].TargetGroupArn' | tr -d \"`
```

### Create a Listener for your Application Load Balancer

``` bash
export LISTENER_ARN=`aws elbv2 create-listener --load-balancer-arn $LOAD_BALANCER_ARN --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=$TARGET_GROUP_ARN | jq '.Listeners[0].ListenerArn' | tr -d \"`
```

## Create ECS Cluster and configure ECS CLI

``` bash
ecs-cli up --cluster myCluster --launch-type FARGATE --vpc $VPC_ID --subnets $PRIVATE_SUBNET_01,$PRIVATE_SUBNET_02
ecs-cli configure --cluster myCluster --region us-east-1 --default-launch-type FARGATE --config-name myCluster
```

### Elastic Container Registry

``` bash
aws ecr create-repository --repository-name my-api
docker build -t my-api .
ecs-cli push my-api --cluster-config myCluster
```

## Create Security Group for my ECS Service

``` bash
export SG_SERVICE_API=`aws ec2 create-security-group --group-name "service-api" --description "My security group for API" --vpc-id $VPC_ID | jq '.GroupId' | tr -d \"`
aws ec2 authorize-security-group-ingress --group-id $SG_SERVICE_API --protocol tcp --port 3000 --cidr 0.0.0.0/0
echo $SG_SERVICE_API
```

## Create a Role for your Service Task



## Create my ECS Service

``` bash
ecs-cli compose --project-name tutorial2 service up \
--deployment-min-healthy-percent 0 \
--target-group-arn $TARGET_GROUP_ARN \
--container-name api \
--container-port 3000 \
--cluster-config myCluster \
--create-log-groups
```
