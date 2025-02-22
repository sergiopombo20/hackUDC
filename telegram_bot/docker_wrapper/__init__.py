import subprocess

def copy_to_container(source_path, container_name, dest_path):
    cmd = ["docker", "cp", source_path, f"{container_name}:{dest_path}"]
    subprocess.run(cmd, check=True, capture_output=True, text=True)

def remove_container(container_name):
    remove_command = ["docker", "rm", "-f", container_name]
    subprocess.run(remove_command, check=True)

def compose_up_service(compose_path, service_name):
    compose_command = [
        "docker", "compose", "-f", compose_path, "up", "-d", service_name
    ]
    subprocess.run(compose_command, check=True)