import boto3
import os

####### Phase 1 #######
############# Mark as comment all the code on Phase 2 before running this section #############

# Using Environment Variables From User Input
vpc_name = os.environ['VPC_NAME']

# Create new VPC & assign a name to our VPC from user input
ec2 = boto3.resource('ec2')
vpc = ec2.create_vpc(CidrBlock='10.1.1.0/24')
vpc.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])
vpc.wait_until_available()

# Enable public dns hostname so that we can SSH into it later
ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )

# Create an internet gateway and attach it to VPC
internetgateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)
internetgateway.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])

# Creating new VPC also automatically creates a route table so I don't need to create an additional
for route_table in vpc.route_tables.all():  # There should only be one route table to start with
        route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)
        route_table.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])

# Create subnet and associate it with the new route table
subnet = ec2.create_subnet(CidrBlock='10.1.1.0/28', VpcId=vpc.id)
subnet.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])
for route_table in vpc.route_tables.all():
        route_table.associate_with_subnet(SubnetId=subnet.id)

# Create a security group for ec2 VPN_Server ec2 and allow SSH inbound rule through the VPC
vpn_srv_securitygroup = ec2.create_security_group(GroupName='vpn_srv_sg', Description='only allow SSH traffic', VpcId=vpc.id)
vpn_srv_securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
vpn_srv_securitygroup.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])

# Create a security group for ec2 APP_Server ec2 and allow SSH inbound rule through the VPC
app_srv_securitygroup = ec2.create_security_group(GroupName='app_srv_sg', Description='only allow SSH traffic', VpcId=vpc.id)
app_srv_securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
app_srv_securitygroup.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])


# Create a file to store the key locally
outfile_vpn = open('VPN-ec2-keypair.pem', 'w')

# Call the boto ec2 function to create a key pair
key_pair_vpn = ec2.create_key_pair(KeyName='VPN-ec2-keypair')

# Capture the key and store it in a file
KeyPairOut_vpn = str(key_pair_vpn.key_material)
outfile_vpn.write(KeyPairOut_vpn)

# Create a ubuntu instance in the subnet- OpenVPN SERVER CREATION
openvpn_server_instance = ec2.create_instances(
        ImageId='ami-0fc970315c2d38f01',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[{
        'SubnetId': subnet.id,
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [vpn_srv_securitygroup.group_id]
        }],
        KeyName='VPN-ec2-keypair')


# Create a file to store the key locally
outfile_app = open('APP-ec2-keypair.pem', 'w')

# Call the boto ec2 function to create a key pair
key_pair_app = ec2.create_key_pair(KeyName='APP-ec2-keypair')

# Capture the key and store it in a file
KeyPairOut_app = str(key_pair_app.key_material)
outfile_app.write(KeyPairOut_app)

# Create a ubuntu instance in the subnet- APP SERVER CREATION
app_server_instance = ec2.create_instances(
        ImageId='ami-0fc970315c2d38f01',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[{
        'SubnetId': subnet.id,
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [app_srv_securitygroup.group_id]
        }],
        KeyName='APP-ec2-keypair')

#######################################################################################################################

####### Phase 2 - After instances were created, we can create Instance Tags #######
############# Mark as comment all the Code on Phase 1 before running this section #############

ec2_client = boto3.client('ec2')
vpn_srv_name = os.environ['VPN_SRV_NAME']
app_srv_name = os.environ['APP_SRV_NAME']

#VPN Server Tag
ec2_client.create_tags(Resources=['i-066f9b75833e40672'], Tags=[{'Key':'name', 'Value':vpn_srv_name}])
#APP Server Tag
ec2_client.create_tags(Resources=['i-077e291e66f1c72b0'], Tags=[{'Key':'name', 'Value':app_srv_name}])
