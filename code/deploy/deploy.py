import paramiko
from os.path import expanduser
from user_definition import *


def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    """Makes SSH connection using the ec2 address,
    username, and the key file (.pem)."""
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    """Creates the environment from the environment.yml file.
    If the environment already exists, it will just update the environment."""
    stdin, stdout, stderr = \
        ssh.exec_command("conda env create -f "
                         "~/" + git_repo_name +
                         "/venv/environment.yml")
    if (b'already exists' in stderr.read()):
        stdin, stdout, stderr = \
            ssh.exec_command("conda env update -f "
                             "~/" + git_repo_name +
                             "/venv/environment.yml")
        print("ERROR in update environment: ", stdout.read())


def git_clone(ssh):
    """Clones the git repository, otherwise pulls
    if already exists."""
    stdin, stdout, stderr = ssh.exec_command("git --version")
    if (b"" is stderr.read()):
        git_clone_command = "git clone https://" + git_user + ":" +\
                            git_user_password + "@github.com/MSDS689/" +\
                            git_repo_name + ".git"
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)
        change_dir = "cd " + git_repo_name + "/; git pull"
        stdin, stdout, stderr = ssh.exec_command(change_dir)
        print("ERROR in update git repo: ", stdout.read())


def main():
    """The command to run in bash. Connects to EC2, clones the git repo,
    creates the environment, and runs crontab."""
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    git_clone(ssh)
    create_or_update_environment(ssh)

    # Launch the application
    # change_dir = "cd " + git_repo_name +\
    #              "/code/backend/server/; flask run"
    # stdin, stdout, stderr = ssh.exec_command(change_dir)
    # print(stdout.read())

    # set crontab
    stdin, stdout, stderr = \
        ssh.exec_command("echo '0 0 * * * ~/.conda/envs/MSDS603/bin/python "
                         "/home/ec2-user/" + git_repo_name +
                         "/code/backend/postgresql/import.py'"
                         " > order.cron")
    stdin, stdout, stderr = \
        ssh.exec_command("crontab order.cron")

    ssh.exec_command("exit")


if __name__ == '__main__':
    main()
