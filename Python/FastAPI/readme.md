






 _  ______    _____ _   _ _____   ___ _____    ____ _   ___   __
| |/ /  _ \  |_   _| | | | ____| |_ _|_   _|  / ___| | | \ \ / /
| ' /| |_) |   | | | |_| |  _|    | |  | |   | |  _| | | |\ V / 
| . \|  __/    | | |  _  | |___   | |  | |   | |_| | |_| | | |  
|_|\_\_|       |_| |_| |_|_____| |___| |_|    \____|\___/  |_|  
                                                                



################################################################################################
#   MIT License                                                                                #
#                                                                                              #
#    Copyright (c) [2024] [Koushik Polsana]                                                    #
#                                                                                              #
#    Permission is hereby granted, free of charge, to any person obtaining a copy              #
#    of this software and associated documentation files (the "Software"), to deal             #
#    in the Software without restriction, including without limitation the rights              #
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell                 #
#    copies of the Software, and to permit persons to whom the Software is                     #
#    furnished to do so, subject to the following conditions:                                  #
#                                                                                              #
#    The above copyright notice and this permission notice shall be included in all            #
#    copies or substantial portions of the Software.                                           #
#                                                                                              #
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR                #
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,                  #
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE               #
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER                    #
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,             #
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE             #
#    SOFTWARE.                                                                                 #
#                                                                                              #
################################################################################################

# AWS VPN Management API

This project provides a FastAPI application to manage AWS VPN connections. The API includes endpoints to create VPN connections, list existing VPN connections, and download VPN configurations.

## Prerequisites

- Python 3.6+
- AWS account credentials with permissions to manage VPN connections
- `pip` package manager

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repository/aws-vpn-management-api.git
    cd aws-vpn-management-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## AWS IAM Role and Policy

You need to create an IAM role with the necessary permissions to manage VPN connections.

### IAM Policy

Create an IAM policy with the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVpnConnections",
                "ec2:DescribeVpnGateways",
                "ec2:DescribeCustomerGateways",
                "ec2:CreateCustomerGateway",
                "ec2:CreateVpnConnection",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeInstances",
                "ec2:DescribeVpcs"
            ],
            "Resource": "*"
        }
    ]
}

# Steps to Create IAM Role

Sign in to the AWS Management Console.
Go to the IAM service.
In the navigation pane, choose Policies and then Create policy.
Choose the JSON tab and paste the policy JSON above.
Choose Review policy.
Enter a name and description for the policy and choose Create policy.
In the navigation pane, choose Roles and then Create role.
Choose EC2 as the trusted entity and choose Next: Permissions.
Attach the policy you just created and choose Next: Tags.
(Optional) Add metadata to the role by attaching tags as key–value pairs and choose Next: Review.
Enter a role name and description, then choose Create role.
Running the Application

Navigate to the main directory: 
cd main

Start the FastAPI application:
uvicorn main:app --reload

Access the API documentation at http://127.0.0.1:8000/docs. 

API Endpoints

1. Create VPN
URL: /create-vpn

Method: POST

Request Body: 

{
    "aws_credentials": {
        "aws_access_key_id": "your_access_key_id",
        "aws_secret_access_key": "your_secret_access_key",
        "region_name": "us-east-1"
    },
    "customer_gateway": {
        "BgpAsn": 65000,
        "PublicIp": "203.0.113.12",
        "Type": "ipsec.1",
        "DeviceName": "CustomerGatewayDevice"
    },
    "vpn_connection": {
        "CustomerGatewayId": "cgw-0b89624cf2c557249",
        "Type": "ipsec.1",
        "VpnGatewayId": "vgw-9daaf4d8",
        "Options": {
            "StaticRoutesOnly": true,
            "TunnelOptions": [
                {
                    "TunnelInsideCidr": "169.254.10.0/30",
                    "PreSharedKey": "presharedkey1",
                    "Phase1LifetimeSeconds": 28800,
                    "Phase2LifetimeSeconds": 3600,
                    "RekeyFuzzPercentage": 100,
                    "RekeyMarginTimeSeconds": 540,
                    "StartupAction": "add",
                    "DPDTimeoutSeconds": 30,
                    "DPDTimeoutAction": "clear",
                    "IKEVersions": [
                        {
                            "Value": "ikev1"
                        },
                        {
                            "Value": "ikev2"
                        }
                    ],
                    "Phase1EncryptionAlgorithms": [
                        {
                            "Value": "AES256"
                        }
                    ],
                    "Phase2EncryptionAlgorithms": [
                        {
                            "Value": "AES256"
                        }
                    ],
                    "Phase1IntegrityAlgorithms": [
                        {
                            "Value": "SHA2-256"
                        }
                    ],
                    "Phase2IntegrityAlgorithms": [
                        {
                            "Value": "SHA2-256"
                        }
                    ],
                    "Phase1DHGroupNumbers": [
                        {
                            "Value": 2
                        }
                    ],
                    "Phase2DHGroupNumbers": [
                        {
                            "Value": 2
                        }
                    ]
                }
            ]
        }
    }
}

Response: 

{
    "message": "VPN connection created successfully",
    "customer_gateway": {
        "CustomerGatewayId": "string",
        ...
    },
    "vpn_connection": {
        "VpnConnectionId": "string",
        ...
    }
}

2. List VPN Connections
URL: /list-vpn-connections

Method: POST

Request Body: 

{
    "aws_credentials": {
        "aws_access_key_id": "your_access_key_id",
        "aws_secret_access_key": "your_secret_access_key",
        "region_name": "us-east-1"
    }
}

Response: 

{
    "message": "VPN connections retrieved successfully",
    "vpn_connections": [
        {
            "VpnConnectionId": "string",
            
        },
        
    ]
}

Get VPN Configuration
URL: /get-vpn-config

Method: POST

Request Body:

{
    "aws_credentials": {
        "aws_access_key_id": "your_access_key_id",
        "aws_secret_access_key": "your_secret_access_key",
        "region_name": "us-east-1"
    },
    "vpn_connection_id": "your_vpn_connection_id"
}


Response:

{
    "message": "VPN configuration for your_vpn_connection_id downloaded",
    "vpn_configuration": {
        "VpnConnectionId": "string",
        
    }
}


