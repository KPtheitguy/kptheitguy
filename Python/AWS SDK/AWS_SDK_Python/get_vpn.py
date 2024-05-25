from aws_authenticator import AWSAuthenticator
import json
from datetime import datetime

def convert_datetime(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def get_vpn_connections():
    try:
        # Initialize the authenticator with the path to the credentials file
        authenticator = AWSAuthenticator('inputs.json')
        
        # Get a boto3 session
        session = authenticator.get_session()
        
        # Use the session to create an EC2 client
        ec2_client = session.client('ec2')

        # Describe VPN connections
        response = ec2_client.describe_vpn_connections()
        return response['VpnConnections']
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    vpn_connections = get_vpn_connections()
    # Beautify and print the JSON
    print(json.dumps(vpn_connections, indent=4, default=convert_datetime))
