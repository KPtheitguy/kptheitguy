from aws_authenticator import AWSAuthenticator
import json

def download_vpn_configuration(ec2_client, vpn_connection_id):
    response = ec2_client.describe_vpn_connections(
        VpnConnectionIds=[vpn_connection_id]
    )
    return response['VpnConnections'][0]

def main():
    # Initialize the authenticator
    authenticator = AWSAuthenticator('inputs.json')
    session = authenticator.get_session()
    ec2_client = session.client('ec2')

    # Load VPN configuration input
    with open('downloadvpn.json', 'r') as f:
        download_config = json.load(f)

    region_name = download_config['region_name']
    vpn_connection_id = download_config['vpn_connection_id']

    # Download VPN Configuration
    vpn_configuration = download_vpn_configuration(ec2_client, vpn_connection_id)
    
    # Save VPN configuration to file
    with open(f'{vpn_connection_id}_config.json', 'w') as f:
        json.dump(vpn_configuration, f, indent=4, default=str)
    
    print(f"VPN Configuration downloaded and saved to {vpn_connection_id}_config.json")

if __name__ == "__main__":
    main()
