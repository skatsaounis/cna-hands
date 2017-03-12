for d in $(docker ps -a | awk '{print $1}' | sed '1d');
do
    docker rm -f $d
done

docker ps -a
