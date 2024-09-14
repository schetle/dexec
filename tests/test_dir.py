import subprocess

from fixtures import script_path, exec_create_file


def test_dir(script_path, exec_create_file):
    """Use the ls command to see if our tmp file exists in the path we created in our fixture"""
    result = subprocess.run(
        ['python', script_path, '--disable_stream', '--disable_spinner', 'my-container', 'ls', exec_create_file['path']],
        capture_output=True, text=True
    )

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    assert f"{exec_create_file['path']}" in stdout, f"Unexpected stdout: {stdout}"
    assert stderr == "", f"Unexpected stderr: {stderr}"
