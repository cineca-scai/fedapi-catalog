#!/bin/bash

docker_volumes_prefix="fedapi"

echo "# ############################################ #"
echo -e "\t\tHTTP API development"
echo "# ############################################ #"
echo ""

if [ "$1" == "help" -o -z "$1" ]; then
    echo "Available commands:"
    echo ""
    echo -e "init:\t\tStartup your repository code, containers and volumes"
    echo -e "training:\tLaunch the environment for training on GraphDB"
    # echo -e "addiuser:\tAdd a new certificated user to irods"
    echo ""
    echo -e "check:\tCheck the stack status"
    echo -e "stop:\tFreeze your containers stack"
    echo -e "remove:\tRemove all containers"
    echo -e "clean:\tRemove containers and volumes (BE CAREFUL!)"
    echo ""
    echo -e "irestart:\tRestart the main iRODS iCAT service instance"
    echo -e "irods_shell:\tOpen a shell inside the iRODS iCAT server container"
    echo -e "server_shell:\tOpen a shell inside the Flask server container"
    echo -e "client_shell:\tOpen a shell to test API endpoints"
    echo -e "api_test:\tRun tests with nose (+ coverage)"
    echo ""
    echo -e "push:\tPush code to github"
    echo -e "update:\tPull updated code and images"
    echo ""
    echo -e "***Modes***:"
    echo -e "DEBUG:\tREST API server should be launched using container shell"
    echo -e "DEVELOPMENT:\tREST API server with Flask WSGI and Debug"
    echo -e "PRODUCTION:\tREST API server with Gunicorn behind nginx proxy"
    echo ""
    echo -e "[Mode] restart:\t(Re)Launch the Docker stack"
    echo -e "logs:\tAttach to all container logs"
    exit 0
fi

#####################
# Confs
subdir="backend"
submodule_tracking="submodules.current.commit"
irodscontainer="icat"
restcontainer="rest"
proxycontainer="proxy"
clientcontainer="apitests"
vcom="docker volume"
compose_base="docker-compose -f docker-compose.yml"


# Check the prefix
if [ "$docker_volumes_prefix" == "httpapitemplate" ]; then
    echo '$docker_volumes_prefix: "httpapitemplate"'
    echo ""
    echo "Please consider changing the main docker volume prefix"
    echo "(Line 3 of the './do' file)"
    echo ""
    exit 1
else
    export VOLUMES_PREFIX="$docker_volumes_prefix"
fi

# Init mode
if [ "$1" == "init" ]; then
    compose_run="$compose_base -f composers/init.yml"

# Production mode
elif [ "$1" == "PRODUCTION" ]; then
    compose_run="$compose_base -f composers/production.yml"

# Development mode
elif [ "$1" == "DEVELOPMENT" ]; then
    compose_run="$compose_base -f composers/development.yml"

# Training mode
elif [ "$1" == "training" ]; then
    compose_run="$compose_base -f composers/training.yml"

# Normal / debug mode
else
    compose_run="$compose_base -f composers/debug.yml"

fi

make_tests="$compose_run exec rest ./tests.sh"
#####################

# Check prerequisites
coms="docker $compose"
for com in $coms;
do
    dcheck=`which $com`
    if [ "$dcheck" == "" ]; then
        echo "Please install $com to use this project"
        exit 1
    fi

    dcheck=`$com ps 2>&1 | grep -i "cannot connect"`
    if [ "$dcheck" != "" ]; then
        echo "Please check if your Docker daemon is running"
        exit 1
    fi
done

if [ "$(ls -A $subdir)" ]; then
    echo "Submodule already exists" > /dev/null
else
    echo "Inizialitazion for the http-api-base submodule"
    git clone https://github.com/EUDAT-B2STAGE/http-api-base.git $subdir
    # git submodule init
    # git submodule update --remote
    cd $subdir
    git checkout master
    cd ..
fi

# Update the remote github repos
if [ "$1" == "push" ]; then

    check_container=`$compose_run ps rest | grep -i exit`
    if [ "$check_container" != "" ]; then
        echo "Please make sure that Flask container server is running"
        echo "You may try with the command:"
        echo "$0 DEBUG"
        echo ""
        exit 1
    fi

    if [ "$2" != "force" ]; then
        testlogs="/tmp/tests.log"
        echo "Running tests before pushing..."
        $make_tests > $testlogs
        if [ "$?" == "0" ]; then
            echo "Test are fine!"
        else
            echo "Failed, to test... (see $testlogs file)"
            echo "Fix errors before pushing, or run again with:"
            echo "$0 $1 force"
            exit 1
        fi
    fi

    echo "Pushing submodule"
    cd $subdir
    git push
    cd ..

    # Save a snapshot of current submodule
    echo "Save submodule status"
    echo -e \
        $(cd $subdir && git log -n 1 --oneline --no-color)"\n"$(cd $subdir && git branch --no-color) \
        > $submodule_tracking

    echo "Pushing main repo"
    git add $submodule_tracking
    git commit
    git push
    echo "Completed"
    exit 0
fi

# Update your code
if [ "$1" == "update" ]; then
    echo "Updating docker images to latest release"
    $compose_run pull
    echo "Pulling main repo"
    git pull
    echo "Pulling submodule"
    cd $subdir
    git pull
    echo "Done"
    exit 0
fi

#######################################

## // TO FIX: make this parametric:
# https://github.com/pdonorio/restapi-template/issues/1

# # Check if init has been executed

volumes=`$vcom ls | awk '{print $NF}' | grep "^${docker_volumes_prefix}_"`

# #echo -e "VOLUMES are\n*$volumes*"
# if [ "$volumes"  == "" ]; then
#     if [ "$1" != "init" ]; then
#         echo ""
#         echo "Docker volumes are missing."
#         echo "You must *init* this project:"
#         echo ""
#         echo "\$ $0 init"
#         echo ""
#         exit 1
#     fi
# fi

################################
# EXECUTE OPTIONS

# Init your stack
if [ "$1" == "init" ]; then
    echo "WARNING: Removing old containers/volumes if any"
    echo "(Sleeping some seconds to let you stop in case you made a mistake)"
    sleep 7
    echo "Containers stopping"
    $compose_run stop
    echo "Containers deletion"
    $compose_run rm -f
    if [ "$volumes"  != "" ]; then
        echo "Destroy volumes:"
        docker volume rm $volumes
    fi
    echo "READY TO INIT"
    $compose_run up icat rest
    if [ "$?" == "0" ]; then
        echo ""
        echo "Your project is ready to be used."
        echo "Everytime you need to start just run:"
        echo "\$ $0 DEBUG"
        echo ""
    fi
    exit 0

# training
elif [ "$1" == "training" ]; then
    container="training"
    $compose_run rm -f $container
    $compose_run up -d $container
    $compose_run exec --user root $container chown -R root /opt/certificates
    echo ""
    echo "Please edit the python file with path'./training/custom.py',"
    echo "then execute your code within the container:"
    echo "$ ./training.py"
    echo ""
    $compose_run exec --user root $container bash
    exit 0

# Verify the status
elif [ "$1" == "check" ]; then
    echo "Stack status:"
    $compose_run ps
    exit 0

# Freeze containers
elif [ "$1" == "stop" ]; then
    echo "Freezing the stack"
    $compose_run stop
    exit 0

# Remove all containers
elif [ "$1" == "remove" ]; then
    echo "REMOVE CONTAINERS"
    $compose_run stop
    $compose_run rm -f
    exit 0

# Destroy everything: containers and data saved so far
elif [ "$1" == "clean" ]; then
    echo "REMOVE DATA"
    echo "are you really sure?"
    sleep 5

## // TO FIX:
# does it really work?

    # From docker-compose man:
    # > "down": Stop and remove containers, networks, images, and volumes
    $compose_run down

    # $compose_run stop
    # $compose_run rm -f
    for volume in $volumes;
    do
        echo "Remove $volume volume"
        $vcom rm $volume
        sleep 1
    done
    exit 0

elif [ "$1" == "addiuser" ]; then
    echo "Adding a new certificated iRODS user:"
    $compose_run exec $irodscontainer /addusercert $2
    exit 0

elif [ "$1" == "irestart" ]; then
    $compose_run exec $irodscontainer /bin/bash /irestart
    exit 0

elif [ "$1" == "irods_shell" ]; then
    $compose_run exec $irodscontainer bash
    exit 0

elif [ "$1" == "server_shell" ]; then
    $compose_run exec $restcontainer bash
    exit 0

elif [ "$1" == "api_test" ]; then
    echo "Opening a shell for nose2 tests"
    $make_tests
    exit 0

elif [ "$1" == "client_shell" ]; then
    echo "Opening a client shell"
    # $compose_run up --no-deps -d $clientcontainer
    $compose_run exec $clientcontainer ash
    exit 0

# Handle the right logs
elif [ "$1" == "logs" ]; then
    $compose_run logs -f -t --tail="10"
    exit 0
fi

# Boot up
if [ "$1" == "DEBUG" -o "$1" == "DEVELOPMENT" -o "$1" == "PRODUCTION" ];
then

    echo "Docker stack: booting"

    if [ "$2" == "restart" ]; then
        echo "Clean previous containers"
        $compose_run stop
        $compose_run rm -f
    fi

    case $2 in
        ''|*[!0-9]*) ;;
        *)
            service="worker"
            echo "Setting $2 $service(s)"
            # Make sure we bring up the containers and all of its links
            $compose_run up -d $service
            # Scale to the number of requested workers
            $compose_run scale $service=$2
            ;;
    esac

    # Check certificates
    if [ "$1" == "PRODUCTION" ]; then
        if [ ! -f "./certs/nginx-selfsigned.key" -o ! -f "./certs/nginx-selfsigned.crt" ];
        then
            echo "Missing certificates."
            echo "To create self_signed files you may use:"
            echo "./confs/create_self_signed_ssl.sh"
            exit 1
        fi
    fi

    # The client container always has the best link to access the server
    $compose_run up -d $clientcontainer
    status="$?"

    echo "Stack processes:"
    $compose_run ps

    if [ "$status" == "0" ]; then
        $compose_run exec --user root rest update-ca-certificates
        echo ""
        echo "To access the flask api container:"
        echo "$0 server_shell"
        echo ""
        echo "To query the api server (if running) use the client container:"
        echo "$0 client_shell"

        path="/api/status"

        if [ "$1" == "PRODUCTION" ]; then
            echo "/ # http --follow --verify /tmp/cert.crt awesome.docker$path"
        elif [ "$1" == "DEVELOPMENT" ]; then
            echo "/ # http GET http://apiserver$path"
        else
            echo "/ # http GET apiserver:5000$path"
        fi
        echo ""
    fi

    echo "Boot completed"
    exit 0

fi

echo "Unknown operation '$1'!"
echo "Use \"$0 help\" to see available commands "
exit 1
