import subprocess

from fixtures import script_path, exec_create_file


def test_file(script_path, exec_create_file):
    """Use the file command to get the contents of our fixture-created file"""
    result = subprocess.run(
        ['python', script_path, '--disable_stream', '--disable_spinner', 'my-container', 'file', exec_create_file['path']],
        capture_output=True, text=True
    )

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    assert stdout == exec_create_file['contents'], f"Unexpected stdout: {stdout}"
    assert stderr == "", f"Unexpected stderr: {stderr}"
