from .aws_authenticator import AWSAuthenticator
import json

def create_customer_gateway(ec2_client, config):
    response = ec2_client.create_customer_gateway(
        BgpAsn=config['BgpAsn'],
        PublicIp=config['PublicIp'],
        Type=config['Type'],
        DeviceName=config.get('DeviceName', 'CustomerGatewayDevice')
    )
    return response['CustomerGateway']

def create_vpn_connection(ec2_client, config):
    response = ec2_client.create_vpn_connection(
        CustomerGatewayId=config['CustomerGatewayId'],
        Type=config['Type'],
        VpnGatewayId=config['VpnGatewayId'],
        Options=config['Options']
    )
    return response['VpnConnection']

def create_vpn(vpn_config):
    try:
        # Initialize the authenticator
        authenticator = AWSAuthenticator('inputs.json')
        session = authenticator.get_session()
        ec2_client = session.client('ec2')

        # Create Customer Gateway
        customer_gateway_config = vpn_config['customer_gateway']
        customer_gateway = create_customer_gateway(ec2_client, customer_gateway_config)
        vpn_config['vpn_connection']['CustomerGatewayId'] = customer_gateway['CustomerGatewayId']

        # Create VPN Connection
        vpn_connection_config = vpn_config['vpn_connection']
        vpn_connection = create_vpn_connection(ec2_client, vpn_connection_config)
        
        return {
            "message": "VPN connection created successfully",
            "customer_gateway": customer_gateway,
            "vpn_connection": vpn_connection
        }
    except Exception as e:
        return {
            "message": "Error creating VPN connection",
            "error": str(e)
        }

if __name__ == "__main__":
    with open('vpnconfig.json', 'r') as f:
        vpn_config = json.load(f)
    result = create_vpn(vpn_config)
    print(json.dumps(result, indent=4, default=str))
