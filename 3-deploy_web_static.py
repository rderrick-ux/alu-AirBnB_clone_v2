#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to the web servers."""
from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists

env.hosts = ['35.173.213.123', '44.203.196.106']


def do_pack():
    """Generate a .tgz archive from the contents of web_static.

    Returns:
        The archive path if generated correctly, otherwise None.
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


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

        put(archive_path, "/tmp/{}".format(filename))
        run("mkdir -p {}".format(release))
        run("tar -xzf /tmp/{} -C {}".format(filename, release))
        run("rm /tmp/{}".format(filename))
        run("mv {0}web_static/* {0}".format(release))
        run("rm -rf {}web_static".format(release))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute an archive to the web servers.

    Returns:
        The return value of do_deploy, or False if no archive was created.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
