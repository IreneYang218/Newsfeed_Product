import paramiko
from os.path import expanduser
from user_definition import *


def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    """
    Makes SSH connection using the ec2 address,
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
            print("ERROR in update environment: ", stderr.read())
        else:
            print("UPDATE ENVIRONMENT SUCCESS")
    else:
        print("CREATE ENVIRONMENT SUCCESS")


def git_clone(ssh):
    """
    Clones the git repository,
    Otherwise pulls if already exists.
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
                print("ERROR in update git repo: ", stderr.read())
            else:
                print("UPDATE GIT REPO SUCCESS")
        else:
            print("CLONE GIT REPO SUCCESS")


def main():
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

    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    # git_clone(ssh)
    # create_or_update_environment(ssh)

    # Launch the application
    # run_server = "cd " + git_repo_name +\
    #              "/code/server/; nohup flask run > /dev/null 2>&1 &"
    # stdin, stdout, stderr = ssh.exec_command(run_server)
    # if (stderr.read() is not b""):
    #     print("ERROR in running server: ", stderr.read())
    # else:
    #     print("SERVER RUN SUCCESS")
    # transport = client.get_transport()
    # channel = transport.open_session()
    # channel.exec_command('python script.py > /dev/null 2>&1 &')

    # set crontab
    # get streaming data everyday
    # stdin, stdout, stderr = \
    #     ssh.exec_command("echo '0 0 * * * ~/.conda/envs/MSDS603/bin/python "
    #                      "/home/ec2-user/" + git_repo_name +
    #                      "/code/data/api_to_df.py'"
    #                      " > order.cron")
    # stdin, stdout, stderr = \
    #     ssh.exec_command("crontab order.cron")
    # if (stderr.read() is not b""):
    #     print("ERROR in crontab: ", stdout.read())
    # else:
    #     print("SET UP CRONTAB SUCCESS")

    # running model

    # get output data from s3
    download_data = "source activate msds603;" + \
                    " cd ~/" + git_repo_name + "/code/data/;" + \
                    " python download.py" + \
                    " model_output_data/result_sorted.csv model_output/"
    stdin, stdout, stderr = ssh.exec_command(download_data)
    print(stdout.read())
    print(stderr.read())
    if stderr.read():
        print("ERROR in download data: ", stderr.read())
    else:
        print("DOWNLOAD DATA SUCCESS")
        print(stdout.read())

    # load output data to RDS
    load_output = "cd " + git_repo_name + \
                  "/code/backend/postgresql/;" + \
                  " python preprocess.py" + \
                  " ../data/model_output/result_sorted.csv" + \
                  " ../data/cleaned/sample_data.csv" + \
                  " python import.py" + \
                  " ../data/cleaned/sample_data.csv" + \
                  " newsphi.news_articles"
    stdin, stdout, stderr = ssh.exec_command(load_output)
    if (stderr.read() is not b""):
        print("ERROR in import data: ", stderr.read())
    else:
        print("IMPORT DATA SUCCESS")

    # exit
    ssh.exec_command("exit")


if __name__ == '__main__':
    main()
