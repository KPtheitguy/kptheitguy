from .aws_authenticator import AWSAuthenticator
import json

def download_vpn_configuration(ec2_client, vpn_connection_id):
    response = ec2_client.describe_vpn_connections(
        VpnConnectionIds=[vpn_connection_id]
    )
    return response['VpnConnections'][0]

def download_vpn(vpn_connection_id):
    try:
        # Initialize the authenticator
        authenticator = AWSAuthenticator('inputs.json')
        session = authenticator.get_session()
        ec2_client = session.client('ec2')

        # Download VPN Configuration
        vpn_configuration = download_vpn_configuration(ec2_client, vpn_connection_id)
        
        # Save VPN configuration to file
        with open(f'{vpn_connection_id}_config.json', 'w') as f:
            json.dump(vpn_configuration, f, indent=4, default=str)
        
        return {
            "message": f"VPN configuration for {vpn_connection_id} downloaded and saved",
            "vpn_configuration": vpn_configuration
        }
    except Exception as e:
        return {
            "message": "Error downloading VPN configuration",
            "error": str(e)
        }

if __name__ == "__main__":
    with open('downloadvpn.json', 'r') as f:
        download_config = json.load(f)
    vpn_connection_id = download_config['vpn_connection_id']
    result = download_vpn(vpn_connection_id)
    print(json.dumps(result, indent=4, default=str))
