import paramiko
from os.path import expanduser
from user_definition import *
import sys


def ssh_client():
    """Return SSH client object."""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    """
    Makes SSH connection using the EC2 address,
    username, and the key file (.pem).
    """
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    """
    Creates the environment from the environment.yml file.
    If the environment already exists,
    it will just update the environment.
    """
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
            print("ERROR in update environment: ", stdout.read())
        else:
            print("UPDATE ENVIRONMENT SUCCESS")
    else:
        print("CREATE ENVIRONMENT SUCCESS")


def git_clone(ssh):
    """
    Clones the GIT repository,
    otherwise pulls if already exists.
    """
    stdin, stdout, stderr = ssh.exec_command("git --version")
    if (b"" is stderr.read()):
        git_clone_command = "git clone https://" + git_user_id +\
                            "@github.com/" + git_repo_owner + "/" +\
                            git_repo_name + ".git"
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)
        if (b'already exists' in stderr.read()):
            change_dir = "cd " + git_repo_name +\
                     "/; git reset --hard origin; git pull"
            stdin, stdout, stderr = ssh.exec_command(change_dir)
            if (stderr.read() is not b""):
                print("ERROR in update git repo: ", stdout.read())
            else:
                print("UPDATE GIT REPO SUCCESS")
        else:
            print("CLONE GIT REPO SUCCESS")


def streaming_data(ssh):
    """Get streaming data from Webhose API source."""
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


def download_data_from_s3(ssh):
    """Download data from S3 bucket to EC2/local machine."""
    download_data = "source activate msds603;" + \
                    " cd ~/" + git_repo_name + "/code/data/;" + \
                    " python day" + \
                    " model_output_data/topic_name_num_sentiment.csv" + \
                    " model_output/"
    stdin, stdout, stderr = ssh.exec_command(download_data)
    if stderr.read():
        print("ERROR in download data: ", stdout.read())
    else:
        print("DOWNLOAD DATA SUCCESS")


def load_data_to_rds(ssh):
    """Import data to RDS tables."""
    load_output = "cd " + git_repo_name + \
                  "/code/backend/postgresql/;" + \
                  " python preprocess.py" + \
                  " ../../data/model_output/topic_name_num_sentiment.csv" + \
                  " sample_data.csv;" + \
                  " python import.py" + \
                  " sample_data.csv" + \
                  " newsphi.news_articles"
    stdin, stdout, stderr = ssh.exec_command(load_output)
    if (stderr.read() is not b""):
        print("ERROR in import data: ", stdout.read())
    else:
        print("IMPORT DATA SUCCESS")


if __name__ == '__main__':
    """
    The command to run in bash.
    Connects to EC2;
    Clones the git repo;
    Creates the environment;
    Set crontab for getting streaming data daily;
    Run the model;
    Import new model output to RDS;
    Run the server.
    """
    # create ssh connection
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)

    # update git repo
    boolean = input('Update git repo (Y/N):')
    if boolean == 'Y':
        git_clone(ssh)
    else:
        print('skip')

    # update env
    boolean = input('Update environment (Y/N):')
    if boolean == 'Y':
        create_or_update_environment(ssh)
    else:
        print('skip')

    # set crontab
    boolean = input('Set crontab for streaming data (Y/N):')
    if boolean == 'Y':
        streaming_data(ssh)
    else:
        print('skip')

    # running model

    # get output data from s3
    boolean = input('Download data from S3 (Y/N):')
    if boolean == 'Y':
        download_data_from_s3(ssh)
    else:
        print('skip')

    # load output data to RDS
    boolean = input('Upload data to RDS (Y/N):')
    if boolean == 'Y':
        load_data_to_rds(ssh)
    else:
        print('skip')

    # open a screen session
    transport = ssh.get_transport()
    channel = transport.open_session()

    # Launch the RESTful API
    boolean = input('Set RESTful API (Y/N):')
    if boolean == 'Y':
        set_api = "cd " + git_repo_name + \
                "/code/backend/postgrest/;" + \
                " ./postgrest postgrest.conf >> log 2>&1 &"
        stdin, stdout, stderr = ssh.exec_command(set_api)
        if (stderr.read() is not b""):
            print("ERROR in run RESTful api: ", stdout.read())
        else:
            print("API SET SUCCESS")
    else:
        print('skip')

    # Launch the application
    boolean = input('Launch website (Y/N):')
    if boolean == 'Y':
        run_server = "source activate msds603;" + \
                    " cd " + git_repo_name +\
                    "/code/server/; flask run >> log 2>&1 &"
        stdin, stdout, stderr = ssh.exec_command(run_server)
        if (stderr.read() is not b""):
            print("ERROR in running server: ", stderr.read())
        else:
            print("SERVER RUN SUCCESS")
    else:
        print('skip')

    # Disable the application
    boolean = input('Disable website (Y/N):')
    if boolean == 'Y':
        check_pid = "pgrep flask"
        stdin, stdout, stderr = ssh.exec_command(check_pid)
        pid = stdout
        kill_server = "kill -9 " + str(pid)
        stdin, stdout, stderr = ssh.exec_command(kill_server)
        if (stderr.read() is not b""):
            print("ERROR in killing server: ", stderr.read())
        else:
            print("KILL SERVER SUCCESS")
    else:
        print('skip')

    # exit
    ssh.exec_command("exit")
