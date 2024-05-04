import subprocess

def run_locust(script_name, host, users, spawn_rate, run_time, name):
    """
    Function to run a locust file with specified parameters.
    """
    command = [
        "locust",
        "-f", script_name,
        "--headless",
        "--users", str(users),
        "--spawn-rate", str(spawn_rate),
        "--run-time", run_time,
        "--host", host,
        "--csv", f"./results/{name}-{users}-users"
    ]
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Running {script_name} finished with output:\n{result.stdout}")

# names = ["(ruby-no-cache)", "(ruby-cache)", "(python-no-cache)", "(python-cache)"]
# hosts = ["http://localhost", "http://localhost:82", "http://localhost:83", "http://localhost:84"]
names = ["(python-no-cache)"]
hosts = ["http://localhost:84"]
usersRange = [1, 10, 100]
spawnRateRange = 1
duration = "5m"
script = "locustfile.py"

# List of scripts and their parameters
locust_scripts = []

# Generate the list of scripts and their parameters
for id, host in enumerate(hosts):
    for users in usersRange:
        locust_scripts.append((script, host, users, spawnRateRange, duration, names[id]))
        print()



# Run each Locust script in order
for script, host, users, rate, duration, name in locust_scripts:
    print(f"Starting {name} with {users} users on {host} for {duration}...")
    run_locust(script, host, users, rate, duration, name)
