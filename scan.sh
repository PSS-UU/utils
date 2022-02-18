#!/usr/local/bin/zsh
PROJECTS=(aubon padelbuddy nationsguiden stickling vegify-1 vegify-2)

for host in $PROJECTS
do
  echo $host.platform-spanning.systems 
done | xargs nmap --script=mysql-info
