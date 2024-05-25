from aws_authenticator import AWSAuthenticator
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

def main():
    # Initialize the authenticator
    authenticator = AWSAuthenticator('inputs.json')
    session = authenticator.get_session()
    ec2_client = session.client('ec2')

    # Load VPN configuration
    with open('vpnconfig.json', 'r') as f:
        vpn_config = json.load(f)

    # Create Customer Gateway
    customer_gateway_config = vpn_config['customer_gateway']
    customer_gateway = create_customer_gateway(ec2_client, customer_gateway_config)
    print("Customer Gateway Created:", json.dumps(customer_gateway, indent=4))

    # Update VPN configuration with the new Customer Gateway ID
    vpn_config['vpn_connection']['CustomerGatewayId'] = customer_gateway['CustomerGatewayId']

    # Save updated vpnconfig.json
    with open('vpnconfig.json', 'w') as f:
        json.dump(vpn_config, f, indent=4)

    # Create VPN Connection
    vpn_connection_config = vpn_config['vpn_connection']
    vpn_connection = create_vpn_connection(ec2_client, vpn_connection_config)
    print("VPN Connection Created:", json.dumps(vpn_connection, indent=4, default=str))

if __name__ == "__main__":
    main()
