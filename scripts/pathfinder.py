# This file is the entrypoint into the Pathfinder CLI.
# It's responsible for first ensuring that we're running inside the Docker container before passing on the
# input to the CLI commands, which you'll define in cli.py. If we're not running ignside the Docker container,
# we'll run one and enter it. We're implementing our CLI like this because it's very similar to the CMR CLI.

import docker
import subprocess
import sys
from pathlib import Path
from os import getuid, path

# TODO: Make it run the Pathfinder container (or create one if it doesn't exist) and then pass it onto the CLI.

PATHFINDER_DIR = path.join(path.dirname(path.realpath(__file__)), "..")


def running_in_docker():
    '''
    Returns true if this script is running inside a Docker container.
    Only Docker containers should have a ".dockerenv" file automatically at their roots.
    '''
    return path.isfile('/.dockerenv')


def create_container(docker_client):
    '''
    Creates a container running the "cornellmarsrover/pathfinder" image.

    Args:
        docker_client: DockerClient instance to use

    Returns:
        the Container object for the new container.
    '''

    volumes = [f'{path.join(PATHFINDER_DIR)}:/Pathfinder']
    env = dict(LOCAL_USER_ID=getuid())

    # Set up XForwarding
    XSOCK = Path("/tmp/.X11-unix")
    XAUTH = Path("/tmp/.docker.xauth")

    XAUTH.touch()
    cmd = path.join(PATHFINDER_DIR, 'scripts', 'cmr-xauth-config')
    subprocess.check_call([cmd, str(XAUTH)])

    volumes += ["{0}:{0}:rw".format(XAUTH)]
    volumes += ["{0}:{0}:rw".format(XSOCK)]

    # The double braces so that they are escaped, as this is the same
    # format as a Python 3 format string
    env["XAUTHORITY"] = str(XAUTH)
    env["DISPLAY"] = "host.docker.internal:0"
    env["QT_X11_NO_MITSHM"] = "1"

    return docker_client.containers.run(
        "cornellmarsrover/pathfinder", 
        command=['tail', '-f', '/dev/null'], 
        tty=True, 
        detach=True,
        volumes=volumes,
        environment=env)


def boot_docker(args):
    # docker_client is how we interact with the running Docker daemon
    docker_client = None
    try:
        docker_client = docker.from_env()
    except:
        print("❌  Make sure you have a Docker daemon running first.")
        print("To install the Docker daemon: https://docs.docker.com/get-docker/")
        return

    # List all the containers that are running our Pathfinder image, if any.
    candidates = docker_client.containers.list(filters={"ancestor": "cornellmarsrover/pathfinder"})
    if len(candidates) == 0:
        # There are no containers on the system that run our image.
        candidates = [create_container(docker_client=docker_client)]

    # At this point, we have some containers to run on, but we need to make sure we pick one that's actually running.
    # container = next(filter(lambda c: c.status == "running", candidates), None)
    container = candidates[0]

    cmd = ["docker", "exec", "-u", str(getuid()), "-it", container.id, 
        "bash"]
    subprocess.check_call(cmd, universal_newlines=True)


def main(args):
    if running_in_docker():
        if len(args):
            subprocess.call(args)
    else:
        boot_docker(args)

if __name__ == "__main__":
    main(sys.argv)
