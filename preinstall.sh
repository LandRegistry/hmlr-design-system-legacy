#!/bin/bash

yes_or_no() {
    while true; do
        read -rp "$* [y/n]: " yn
        case $yn in
            [Yy]*) return 0  ;;
            [Nn]*) echo "Aborted" ; exit 1 ;;
        esac
    done
}

BOLD=$(printf '\033[1m')
NORMAL=$(printf '\033[0m')

MESSAGE=$(cat <<-END
/  \\        ________________________
|  |       |                        |
@  @       | You appear to be doing |
|| ||      | an ${BOLD}npm install${NORMAL} outside |
|| ||   <--| of the container       |
|\\_/|      |________________________|
\\___/

${NORMAL}You appear to be doing an ${BOLD}npm install${NORMAL} outside of the
docker container. node_modules are managed inside the container at NODE_PATH in order
to avoid conflicts with the host.

If you are:

${BOLD}1)${NORMAL} Trying to install a new package:
  * Abort this command now by pressing '${BOLD}n${NORMAL}'
  * From the host, run ${BOLD}npm install --package-lock-only packageName${NORMAL}
  * Inside the virtual machine, run ${BOLD}rebuild hmlr-design-system${NORMAL}
    to fetch the new modules


${BOLD}2)${NORMAL} Trying to npm install *everything*, because "that's what you normally do"
  * ${BOLD}At the risk of making a sweeping statement, you probably don't want to do this.${NORMAL}
    node_modules are managed inside the container at the location specified
    by NODE_PATH (See your friendly local Dockerfile for more info)

    node_modules folders are not portable between environments, so installing on your host Mac
    will render the Docker based build process broken until you delete your local node_modules again

    If you are really sure this is what you want, then:
  * Press '${BOLD}y${NORMAL}' to continue and install node_modules on your host
  * Be aware that these will take precedeNORMALe over those housed in the
    container and so should be used with caution as it may cause confusion and fires.


${BOLD}3)${NORMAL} Trying to ${BOLD}npm link${NORMAL} a module you are developing:
  * You can't! Because Docker volumes do not support symlinks.
    Unfortunately, npm link just does not work inside docker volumes.
    The way to work around this is to actually check out a copy of the module you
    are working on into the local node_modules folder and work on it there (I.e. /src/node_modules).
    Things inside node_modules will take precedeNORMALe over those installed inside
    the container.


${BOLD}Now you've read all this, do you still want to continue?${NORMAL}
END
)

yes_or_no "$MESSAGE"
