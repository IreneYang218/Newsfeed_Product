import paramiko
from os.path import expanduser
from user_definition import *


# ## Assumption : Anaconda, Git (configured)

def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    stdin, stdout, stderr = \
        ssh.exec_command("conda env create -f "
                         "~/product-analytics-group-project-team1/venv/environment.yml")
    if (b'already exists' in stderr.read()):
        stdin, stdout, stderr = \
            ssh.exec_command("conda env update -f "
                             "~/product-analytics-group-project-team1/venv/environment.yml")


def git_clone(ssh):
    stdin, stdout, stderr = ssh.exec_command("git --version")
    if (b"" is stderr.read()):
        git_clone_command = "git clone https://github.com/" + \
                            git_user_id + "/" + git_repo_name + ".git"
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)
        if ('b"fatal: destination path \'product-analytics-group-project-team1\' already exists and is not an empty directory.\n\"' is stderr.read()):
            git_clone_command = "git pull https://github.com/" + \
                                git_user_id + "/" + git_repo_name + ".git"
            stdin, stdout, stderr = ssh.exec_command(git_clone_command)
    ssh.exec_command(git_clone_command)
        print(stdout.read())
        print(stderr.read())

        # ---- HOMEWORK ----- #
        cron_command = 'crontab -e'
        vi_input = 'i'
        vi_edit = '01 * * * * ~/.conda/envs/MSDS603/bin/python \
                    /home/ec2-user/msds603_week1/Week1/driving_time_example/calculate_driving_time.py'


def main():
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    create_or_update_environment(ssh)
    git_clone(ssh)


if __name__ == '__main__':
    main()
