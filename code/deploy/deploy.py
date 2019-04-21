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
        if (stderr.read() is not b""):
            print("ERROR in update environment: ", stderr.read())
        else:
            print("UPDATE ENVIRONMENT SUCCESS")
    elif (stderr.read() is not b''):
        print("ERROR in create environment: ", stderr.read())
    else:
        print("CREATE ENVIRONMENT SUCCESS")


def git_clone(ssh):
    """Clones the git repository, otherwise pulls
    if already exists."""
    stdin, stdout, stderr = ssh.exec_command("git --version")
    if (b"" is stderr.read()):
        git_clone_command = "git clone https:/" + git_user +\
                            "@github.com/" + git_repo_owner + "/" +\
                            git_repo_name + ".git"
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)
        print(stderr.read())
        print(stdout.read())
        if (b'already exists' in stderr.read()):
            change_dir = "cd " + git_repo_name +\
                     "/; git reset --hard origin; git pull"
            stdin, stdout, stderr = ssh.exec_command(change_dir)
            if (stderr.read() is not b""):
                print("ERROR in update git repo: ", stderr.read())
            else:
                print("UPDATE GIT REPO SUCCESS")
        elif (b'fatal' in stderr.read()):
            print("ERROR in clone git repo: ", stdout.read())
        else:
            print("CLONE GIT REPO SUCCESS")
        


def main():
    """The command to run in bash. Connects to EC2, clones the git repo,
    creates the environment, and runs crontab."""
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    git_clone(ssh)
    create_or_update_environment(ssh)

    # Launch the application
    change_dir = "cd " + git_repo_name +\
                 "/code/backend/server/; pwd"
    stdin, stdout, stderr = ssh.exec_command(change_dir)
    print(stdout.read())

    # set crontab
    # get streaming data everyday
    stdin, stdout, stderr = \
        ssh.exec_command("echo '0 0 * * * ~/.conda/envs/MSDS603/bin/python "
                         "/home/ec2-user/" + git_repo_name +
                         "/code/data/api_to_df.py'"
                         " > order.cron")
    stdin, stdout, stderr = \
        ssh.exec_command("crontab order.cron")
    if (stderr.read() is not b""):
        print("ERROR in crontab: ", stdout.read())
    else:
        print("SET UP CRONTAB SUCCESS")

    # running model
    # upload output to rds
    # running server
    ssh.exec_command("exit")


if __name__ == '__main__':
    main()
