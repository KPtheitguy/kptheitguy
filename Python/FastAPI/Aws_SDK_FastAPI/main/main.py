from fastapi import FastAPI, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Any
import boto3
import json
from datetime import datetime

app = FastAPI()

class AWSCredentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str

class IKEVersion(BaseModel):
    Value: str

class EncryptionAlgorithm(BaseModel):
    Value: str

class IntegrityAlgorithm(BaseModel):
    Value: str

class DHGroupNumber(BaseModel):
    Value: int

class TunnelOptions(BaseModel):
    TunnelInsideCidr: str
    PreSharedKey: str
    Phase1LifetimeSeconds: int
    Phase2LifetimeSeconds: int
    RekeyFuzzPercentage: int
    RekeyMarginTimeSeconds: int
    StartupAction: str
    DPDTimeoutSeconds: int
    DPDTimeoutAction: str
    IKEVersions: List[IKEVersion]
    Phase1EncryptionAlgorithms: List[EncryptionAlgorithm]
    Phase2EncryptionAlgorithms: List[EncryptionAlgorithm]
    Phase1IntegrityAlgorithms: List[IntegrityAlgorithm]
    Phase2IntegrityAlgorithms: List[IntegrityAlgorithm]
    Phase1DHGroupNumbers: List[DHGroupNumber]
    Phase2DHGroupNumbers: List[DHGroupNumber]

class VPNConnectionOptions(BaseModel):
    StaticRoutesOnly: bool
    TunnelOptions: List[TunnelOptions]

class VPNConnectionConfig(BaseModel):
    CustomerGatewayId: str
    Type: str
    VpnGatewayId: str
    Options: VPNConnectionOptions

class CustomerGatewayConfig(BaseModel):
    BgpAsn: int
    PublicIp: str
    Type: str
    DeviceName: str = "CustomerGatewayDevice"

class VPNConfig(BaseModel):
    aws_credentials: AWSCredentials
    customer_gateway: CustomerGatewayConfig
    vpn_connection: VPNConnectionConfig

class DownloadConfig(BaseModel):
    aws_credentials: AWSCredentials
    vpn_connection_id: str

def create_customer_gateway(ec2_client, config: Dict[str, Any]):
    response = ec2_client.create_customer_gateway(
        BgpAsn=config['BgpAsn'],
        PublicIp=config['PublicIp'],
        Type=config['Type'],
        DeviceName=config.get('DeviceName', 'CustomerGatewayDevice')
    )
    return response['CustomerGateway']

def create_vpn_connection(ec2_client, config: Dict[str, Any]):
    response = ec2_client.create_vpn_connection(
        CustomerGatewayId=config['CustomerGatewayId'],
        Type=config['Type'],
        VpnGatewayId=config['VpnGatewayId'],
        Options=config['Options']
    )
    return response['VpnConnection']

def download_vpn_configuration(ec2_client, vpn_connection_id: str):
    response = ec2_client.describe_vpn_connections(
        VpnConnectionIds=[vpn_connection_id]
    )
    return response['VpnConnections'][0]

def get_vpn_connections(aws_credentials: AWSCredentials):
    session = boto3.Session(
        aws_access_key_id=aws_credentials.aws_access_key_id,
        aws_secret_access_key=aws_credentials.aws_secret_access_key,
        region_name=aws_credentials.region_name
    )
    ec2_client = session.client('ec2')
    response = ec2_client.describe_vpn_connections()
    return response['VpnConnections']

@app.post("/create-vpn")
def create_vpn_endpoint(vpn_config: VPNConfig):
    aws_credentials = vpn_config.aws_credentials
    session = boto3.Session(
        aws_access_key_id=aws_credentials.aws_access_key_id,
        aws_secret_access_key=aws_credentials.aws_secret_access_key,
        region_name=aws_credentials.region_name
    )
    ec2_client = session.client('ec2')

    customer_gateway_config = vpn_config.customer_gateway.dict()
    customer_gateway = create_customer_gateway(ec2_client, customer_gateway_config)
    vpn_config.vpn_connection.CustomerGatewayId = customer_gateway['CustomerGatewayId']

    vpn_connection_config = vpn_config.vpn_connection.dict()
    vpn_connection = create_vpn_connection(ec2_client, vpn_connection_config)
    
    return {
        "message": "VPN connection created successfully",
        "customer_gateway": customer_gateway,
        "vpn_connection": vpn_connection
    }

@app.post("/get-vpn-config")
def get_vpn_config_endpoint(download_config: DownloadConfig):
    aws_credentials = download_config.aws_credentials
    session = boto3.Session(
        aws_access_key_id=aws_credentials.aws_access_key_id,
        aws_secret_access_key=aws_credentials.aws_secret_access_key,
        region_name=aws_credentials.region_name
    )
    ec2_client = session.client('ec2')

    vpn_configuration = download_vpn_configuration(ec2_client, download_config.vpn_connection_id)
    return {
        "message": f"VPN configuration for {download_config.vpn_connection_id} downloaded",
        "vpn_configuration": vpn_configuration
    }

@app.post("/list-vpn-connections")
def list_vpn_connections(aws_credentials: AWSCredentials):
    vpn_connections = get_vpn_connections(aws_credentials)
    return {"message": "VPN connections retrieved successfully", "vpn_connections": vpn_connections}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
