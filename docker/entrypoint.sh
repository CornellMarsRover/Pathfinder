#!/bin/bash

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback

USER_ID=${LOCAL_USER_ID:-9001}

echo "Starting with UID : $USER_ID"
useradd --shell /bin/bash -u $USER_ID -o -c "" cmr
export HOME=/home/cmr

echo "cmr ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

chown -R cmr:cmr /home/cmr

exec /usr/local/bin/gosu cmr "$@"
