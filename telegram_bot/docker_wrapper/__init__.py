import subprocess

def copy_to_container(source_path, container_name, dest_path):
    cmd = ["docker", "cp", source_path, f"{container_name}:{dest_path}"]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
