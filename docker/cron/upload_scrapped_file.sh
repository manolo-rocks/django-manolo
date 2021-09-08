#!/bin/bash

# run using a cronjob in local computer
# 0 */3 * * * bash /Users/carlosp420/projects/manolo.rocks-ani/docker/cron/upload_scrapped_file.sh pcm

output_path=/tmp/

cd $output_path
scp -i /Users/carlosp420/.ssh/id_rsa $1.jl manolo@198.199.109.199:/tmp/. 2> /tmp/updload_err.log

# setup a cronjob in the host server (not docker containers) to copy the pcm.jl file
# inside the containers and store using save_items -i