### README.md

#### Introduction

This repository contains scripts for deploying and managing real-time response sessions using FalconPy, along with utilities for handling host lists and session data.

#### Installation

To use these scripts, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Configuration:**
   - Open `config.py` and update the `BASE_URL`, `CLIENT_ID`, and `CLIENT_SECRET` variables with your specific values.

#### Usage

Here's an overview of the main scripts and functions available:

- **read_file(file_path)**: Reads a CSV file containing host information and returns a list of hosts.

- **append_to_deployed_hosts(host)**: Appends a host to the `deployed_hosts.txt` file.

- **parse_session_id(json_dict)**: Parses a JSON dictionary containing session data and retrieves the batch ID.

- **batch_init_rtr_sessions(target_hosts, CLIENT_ID, CLIENT_SECRET)**: Initiates real-time response sessions for a list of target hosts.

- **batch_run_binalyze_deploy_script(target_hosts, batch_id, CLIENT_ID, CLIENT_SECRET)**: Runs a deployment script on specified hosts using the provided batch ID.

- **create_undeployed_hosts_list()**: Creates a list of hosts that have not been deployed yet by comparing `hosts.txt` and `deployed_hosts.txt`.

- **deploy(batch_size)**: Initiates the deployment process for a specified number of hosts, handling session initiation and deployment script execution.

#### Example

To deploy sessions for 1000 hosts:

```python
from deploy_scripts import deploy

deploy(1000)
```

### requirements.txt

```
falconpy
```

---

This README provides an overview of the repository's functionality, installation instructions, usage examples, and dependencies. Adjust the `<repository_url>` and `<repository_directory>` placeholders as appropriate for your actual repository. Ensure you have updated the `config.py` file with your specific Falcon API credentials before running the scripts.