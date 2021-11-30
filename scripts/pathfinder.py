# This file is the entrypoint into the Pathfinder Shell.
# It'll start up a Docker container with a bash session.
# The container is set up with X11 forwarding, has the "/Pathfinder" directory mapped to
# the project directory, and will automatically remove itself and its volumes upon termination.

import subprocess
import sys
from pathlib import Path
from os import getuid, path, environ

PATHFINDER_DIR = path.join(path.dirname(path.realpath(__file__)), "..")


def running_in_docker():
    '''
    Returns true if this script is running inside a Docker container.
    Only Docker containers should have a ".dockerenv" file automatically at their roots.
    '''
    return path.isfile('/.dockerenv')


def boot_docker(args):
    volumes = []
    volumes += ['-v', f'{path.abspath(PATHFINDER_DIR)}:/Pathfinder']

    # Set up XForwarding
    XSOCK = Path("/tmp/.X11-unix")
    XAUTH = Path("/tmp/.docker.xauth")

    XAUTH.touch()
    cmd = path.join(PATHFINDER_DIR, 'scripts', 'cmr-xauth-config')
    subprocess.check_call([cmd, str(XAUTH)])

    volumes += ['-v', "{0}:{0}:rw".format(XAUTH)]
    volumes += ['-v', "{0}:{0}:rw".format(XSOCK)]
    volumes += ['-v', "/home/vagrant/.Xauthority:/home/cmr/.Xauthority:rw"]

    env = []
    env += ["--env", "LOCAL_USER_ID=" + str(getuid())]
    env += ["--env", "XAUTH=" + str(XAUTH)]
    env += ["--env", "DISPLAY=" + environ.get("DISPLAY")]
    env += ["--env", "QT_X11_NO_MITSHM=1"]

    cmd = ["docker", "run", "--rm"]
    cmd += volumes
    cmd += ['--net', 'host']
    cmd += env
    cmd += ['-it']
    cmd += ['cornellmarsrover/pathfinder']
    cmd += ['bash']

    subprocess.check_call(cmd, universal_newlines=True)


def main(args):
    if running_in_docker():
        if len(args):
            subprocess.call(args)
    else:
        boot_docker(args)

if __name__ == "__main__":
    main(sys.argv)
