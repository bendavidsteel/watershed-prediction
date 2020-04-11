#!/bin/bash

# setup script for ec2 linux ami
# Install our public GPG key
rpm --import https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc

# Add the Anaconda repository
cat <<EOF > /etc/yum.repos.d/conda.repo
[conda]
name=Conda
baseurl=https://repo.anaconda.com/pkgs/misc/rpmrepo/conda
enabled=1
gpgcheck=1
gpgkey=https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc
EOF

# install conda
yum -y install conda

source /opt/conda/etc/profile.d/conda.sh

# install required packages
conda install --yes python=3.7
conda install --yes numpy pandas tensorflow scikit-image
