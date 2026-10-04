#!/usr/bin/sh
ip link add link enx68da73ad4664 name eth0.5 type vlan id 5;ip addr add 172.16.5.31/24 dev eth0.5;ifconfig eth0.5 up;ifconfig eth0.5 hw ether 02:00:00:00:10:31;
ip link add link enx68da73ad4664 name eth0.32 type vlan id 32;ip addr add 172.16.32.23/24 dev eth0.32;ifconfig eth0.32 up;ifconfig eth0.32 hw ether 02:00:00:00:10:23;
ip link add link enx68da73ad4664 name eth0.21 type vlan id 21;ip addr add 172.16.21.21/24 dev eth0.21;ifconfig eth0.21 up;ifconfig eth0.21 hw ether 02:00:00:00:10:21;
ip link add link enx68da73ad4664 name eth0.22 type vlan id 22;ip addr add 172.16.22.21/24 dev eth0.22;ifconfig eth0.22 up;ifconfig eth0.22 hw ether 02:00:00:00:10:21;
ip link add link enx68da73ad4664 name eth0.9 type vlan id 9;ip addr add 172.16.9.31/24 dev eth0.9;ifconfig eth0.9 up;ifconfig eth0.9 hw ether 02:00:00:00:10:31