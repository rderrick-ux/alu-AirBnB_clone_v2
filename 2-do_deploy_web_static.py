#!/usr/bin/python3
"""Fabric script that distributes an archive to the web servers."""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['35.173.213.123', '44.203.196.106']


def do_deploy(archive_path):
    """Distribute an archive to the web servers.

    Args:
        archive_path: Path to the archive to deploy.

    Returns:
        True if all operations succeed, otherwise False.
    """
    if not exists(archive_path):
        return False
    try:
        filename = archive_path.split("/")[-1]
        name = filename.split(".")[0]
        release = "/data/web_static/releases/{}/".format(name)

        # Upload the archive to /tmp/ on the web server
        put(archive_path, "/tmp/{}".format(filename))

        # Uncompress the archive into the release folder
        run("mkdir -p {}".format(release))
        run("tar -xzf /tmp/{} -C {}".format(filename, release))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move contents out of the web_static subfolder
        run("mv {0}web_static/* {0}".format(release))
        run("rm -rf {}web_static".format(release))

        # Delete the old symbolic link and create a new one
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release))

        print("New version deployed!")
        return True
    except Exception:
        return False
