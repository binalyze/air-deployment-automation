# Import standard libraries for CSV and JSON operations
import csv, json

# Import FalconPy RealTimeResponse module for interacting with Falcon RTR APIs
from falconpy import RealTimeResponse

# CrowdStrike Falcon API credentials (should ideally be stored in a secure secrets manager)
BASE_URL = ""
CLIENT_ID = ""
CLIENT_SECRET = ""

# Reads a CSV file and returns a list of host IDs
def read_file(file_path):
    hosts_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Ignore empty rows
                hosts_list.append(row[0])  # Assuming each row contains a single host ID
    return hosts_list

# Appends a host ID to the 'deployed_hosts.txt' log after successful deployment
def append_to_deployed_hosts(host):
    with open('deployed_hosts.txt', 'a') as f:
        f.write(host + '\n')
    print(f"Appended '{host}' to deployed_hosts.txt")

# Extracts and returns the session (batch) ID from the Falcon RTR batch_init_sessions() response
def parse_session_id(json_dict):
    # Clean and normalize JSON for parsing, in case of malformed or loosely formatted input
    json_string = json.dumps(json_dict)
    json_string = json_string.replace("'", '"')
    json_string = json_string.replace("True", '"True"')
    json_string = json_string.replace("true", '"true"')    
    json_string = json_string.replace("False", '"False"')
    json_string = json_string.replace("false", '"false"')
    
    print("Modified JSON string:")
    print(json_string)
    
    try:
        data = json.loads(json_string)
        print("Parsed JSON data:")
        print(data)
        session_id = data['body']['batch_id']  # Extract session ID from API response
        return session_id
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing session_id: {e}")
        return None

# Initializes RTR batch sessions for a given list of host IDs
def batch_init_rtr_sessions(target_hosts, CLIENT_ID, CLIENT_SECRET):
    falcon = RealTimeResponse(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    response = falcon.batch_init_sessions(
        host_ids=target_hosts,
        timeout=45,
        timeout_duration="30s"
    )
    return response

# Executes the "Deploy Binalyze" script on the batch of hosts using Active Responder
def batch_run_binalyze_deploy_script(target_hosts, batch_id, CLIENT_ID, CLIENT_SECRET):
    falcon = RealTimeResponse(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    response = falcon.BatchActiveResponderCmd(
        base_command="runscript",
        batch_id=batch_id,
        command_string="runscript -CloudFile='Deploy Binalzye'  -CommandLine=''",
        optional_hosts=target_hosts,
        timeout=45,
        timeout_duration="60s"
    )
    print(response)

# Builds a list of hosts that have not yet had the deployment script executed
def create_undeployed_hosts_list():
    all_hosts = read_file('hosts.txt')  # Master list of all target hosts
    deployed_hosts = read_file('deployed_hosts.txt')  # Hosts already deployed to

    deployed_set = set(deployed_hosts)  # Use set for O(1) lookups
    target_hosts = [host for host in all_hosts if host not in deployed_set]  # Filter out already-deployed hosts

    # Write the list of pending deployment targets to file
    with open('target_hosts.txt', 'w') as f:
        for host in target_hosts:
            f.write(host + '\n')

    return target_hosts  # Note: 'print()' after return is unreachable

# Orchestrates the full deployment flow for a batch of hosts
def deploy(batch_size):
    undeployed_hosts = create_undeployed_hosts_list()  # Get the latest list of undeployed hosts
    target_hosts = undeployed_hosts[:batch_size]  # Slice based on batch size limit
    init_string = batch_init_rtr_sessions(target_hosts, CLIENT_ID, CLIENT_SECRET)  # Start RTR session
    batch_id = parse_session_id(init_string)  # Extract session ID
    print("Batch ID: ", batch_id)
    print("Target Hosts: ", target_hosts)
    batch_run_binalyze_deploy_script(target_hosts, batch_id, CLIENT_ID, CLIENT_SECRET)  # Deploy the script

    # Log each successfully deployed host
    for i in target_hosts:
        append_to_deployed_hosts(i)

# Execute deployment for a batch of up to 1000 hosts
if __name__ == '__main__':
    deploy(1000)
