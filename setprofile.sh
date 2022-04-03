#!/bin/bash
alias pull="git pull origin main"
alias movehome="cd /home/quickly-project/"
alias down="docker-compose down"
alias build="docker-compose up -d --no-deps --build"
alias dockerclear="docker image prune --all"



# sudo nano /etc/ssh/sshd_config
# sudo systemctl reload sshd.service

# ClientAliveInterval 300
# ClientAliveCountMax 1200
