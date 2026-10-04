#!/usr/bin/env bash

DEVICENAME=xat_device
LOCKDIR=/var/lock/xat/
RLOCKFILENAME=$DEVICENAME.rlock
LOCKFILENAME=$DEVICENAME.lock

# any user must creat workspace folder in /root/<ws>/....
USERNAME=$(pwd |awk -F/ '{print $3}')

help()
{
  	Usage="This script supports you take device resource lock and release it after using.\n \
	Usage: sh $0 [OPTION]\n\
	Options:\n\
        -f\t seizing resource lock, must run as root. \n \
        -l\t show resource locks info. \n \
        -t\t take temporary lock, used by sat, release by sat automatcally.  \n \
        -r\t release all owned resource locks.  \n \
        -rr\t release owned resource rlock.  \n \
        -rt\t release owned resource lock.  \n \
        -h\t show this help information.  \n \
        "
  	echo -e ${green} $Usage
  	exit 2
}

show_lock_info()
{
	printf "%-15s %-15s %-13s %-22s %-10s\n" device_name  owner  locktype  time  workspace
	printf "%-15s %-15s %-13s %-22s %-10s\n" $(grep -v '^#' $1)
}

show_lock_info_noheader()
{
	printf "%-15s %-15s %-13s %-22s %-10s\n" $(grep -v '^#' $1)
}

get_lock_info()
{
  	lock_content=$(grep -v '^#' $1)
	lock_info=($lock_content)
	# echo ${lock_info[@]}
	read DEVICENAME OWNER LOCKTYPE LOCKTIME OWNERWS <<< "${lock_info[@]}"
}

write_lock()
{
	if [ ! -d $LOCKDIR ]; then
		mkdir $LOCKDIR
		chmod a+w $LOCKDIR
	fi
	# write_lock <lock_file_path> <device_name> <owner> <locktype> <time> <pid> <workspace>
	echo "# device_name  owner  locktype  time   workspace" > $1
	echo ${@:2} >> $1
	echo "$2 locked, owned by $3 now!"
}

list_all_locks()
{
	if [[ -f "$LOCKDIR$RLOCKFILENAME" && -f "$LOCKDIR$LOCKFILENAME" ]]; then
		show_lock_info $LOCKDIR$RLOCKFILENAME
		show_lock_info_noheader $LOCKDIR$LOCKFILENAME
	elif [[ -f "$LOCKDIR$RLOCKFILENAME" && ! -f "$LOCKDIR$LOCKFILENAME" ]]; then
		show_lock_info $LOCKDIR$RLOCKFILENAME
	elif [[ ! -f "$LOCKDIR$RLOCKFILENAME" && -f "$LOCKDIR$LOCKFILENAME" ]]; then
		show_lock_info $LOCKDIR$LOCKFILENAME
	else
		echo "No lock exists!"
	fi
}

release_owned_rlock()
{
	if [[ -f "$LOCKDIR$RLOCKFILENAME" ]]; then
		get_lock_info "$LOCKDIR$RLOCKFILENAME"
		if [[ $OWNER == $USERNAME ]]; then
			rm $LOCKDIR$RLOCKFILENAME
			echo "$RLOCKFILENAME owned by $OWNER released!"
		else
			echo "rlock exists but not owned by you, No permission!"
		fi
	else
		echo "No rlock exists!"
	fi
}

release_owned_lock()
{
	if [[ -f "$LOCKDIR$LOCKFILENAME" ]]; then
		get_lock_info "$LOCKDIR$LOCKFILENAME"
		if [[ $OWNER == $USERNAME ]]; then
			rm $LOCKDIR$LOCKFILENAME
			echo "$LOCKFILENAME owned by $OWNER released!"
		else
			echo "lock exists but not owned by you, No permission!"
		fi
	else
		echo "No lock exists!"
	fi
}

seizing_lock()
{
	MYUID=`id -u`
	MYGID=`id -g`
	if [ $MYUID -eq 0 ] || [ $MYGID -eq 0 ]; then
		if [[ -f "$LOCKDIR$RLOCKFILENAME" ]]; then
			rm $LOCKDIR$RLOCKFILENAME
			write_lock $LOCKDIR$RLOCKFILENAME $DEVICENAME $USERNAME retain $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
			# chown $SUDO_USER:$SUDO_USER $LOCKDIR$RLOCKFILENAME
			# chmod u+w $LOCKDIR$RLOCKFILENAME
		fi
		if [[ -f "$LOCKDIR$LOCKFILENAME" ]]; then
			rm $LOCKDIR$LOCKFILENAME
			write_lock $LOCKDIR$LOCKFILENAME $DEVICENAME $USERNAME temp $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
			# chown $SUDO_USER:$SUDO_USER $LOCKDIR$LOCKFILENAME
			# chmod u+w $LOCKDIR$LOCKFILENAME
		fi
	else
		echo "this script must be run as root if -f option followd."
		exit 1
	fi
}


# temporary lock
if [ $# -eq 0 ]; then
	# if [[ $(whoami) == root ]]; then
	# 	echo "Warning: Please do not run this script as root, except with '-f' option."
	# 	exit 1
	# fi
  	# create lock
	LOCKFILE=$LOCKDIR$RLOCKFILENAME
	if [[ ! -f "$LOCKDIR$RLOCKFILENAME" && ! -f "$LOCKDIR$LOCKFILENAME" ]]; then
		# no lock exists, create it directly.
		write_lock $LOCKFILE $DEVICENAME $USERNAME retain $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
	elif [[ -f "$LOCKDIR$RLOCKFILENAME" ]]; then
	    # rlock exists, check owner and create lock if owned.
		get_lock_info "$LOCKDIR$RLOCKFILENAME"
		if [[ $OWNER == $USERNAME ]]; then
			write_lock $LOCKFILE $DEVICENAME $USERNAME retain $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
		else
			echo "Get lock fail, device occupied by $OWNER."
			exit 1
		fi
	elif [[ ! -f "$LOCKDIR$RLOCKFILENAME" && -f "$LOCKDIR$LOCKFILENAME" ]]; then
		get_lock_info "$LOCKDIR$LOCKFILENAME"
		if [[ $OWNER == $USERNAME ]]; then
			write_lock $LOCKFILE $DEVICENAME $USERNAME retain $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
		else
			echo "Device occupied by $OWNER. wait for release[Y|n]?"
			read answer # 读取用户输入并赋值给answer变量
			if [ -z $answer ]; then # 判断answer是否为空
				answer=y # 如果为空，给answer赋值为y
			fi
			case $answer in # 根据answer的值进行判断
				y|Y) # 如果是y或Y，执行以下操作
					echo "waiting for release..."
					until [ ! -f "$LOCKDIR$LOCKFILENAME" ]; do # start a loop until lock file does not exist
						sleep 1 # wait for 5 seconds
					done
					write_lock $LOCKFILE $DEVICENAME $USERNAME retain $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
					exit 0
					;;
				n|N) # 如果是n或N，执行以下操作
					exit 1 # 异常退出
					;;
				*) # 如果是其他任何值，执行以下操作
					exit 2 # 异常退出
					;;
			esac
		fi
	fi
elif [ "$1" == "-t" ]; then
	# if [[ $(whoami) == root ]]; then
	# 	echo "Warning: Please do not run this script as root, except with '-f' option."
	# 	exit 1
	# fi
    LOCKFILE=$LOCKDIR$LOCKFILENAME
	if [[ ! -f "$LOCKDIR$RLOCKFILENAME" && ! -f "$LOCKDIR$LOCKFILENAME" ]]; then
		# no lock exists, create it directly.
		write_lock $LOCKFILE $DEVICENAME $USERNAME temp $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
	elif [[ -f "$LOCKDIR$RLOCKFILENAME" && ! -f "$LOCKDIR$LOCKFILENAME" ]]; then
	    # rlock exists, check owner and create lock if owned.
		get_lock_info "$LOCKDIR$RLOCKFILENAME"
		if [[ $OWNER == $USERNAME ]]; then
			write_lock $LOCKFILE $DEVICENAME $USERNAME temp $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
		else
      echo "Device occupied by $OWNER."
			list_all_locks
			exit 1
		fi
	elif [[ ! -f "$LOCKDIR$RLOCKFILENAME" && -f "$LOCKDIR$LOCKFILENAME" ]]; then
		get_lock_info "$LOCKDIR$LOCKFILENAME"
		if [[ $OWNER == $USERNAME ]]; then
			write_lock $LOCKFILE $DEVICENAME $USERNAME temp $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
		else
			echo "Device occupied by $OWNER. waiting for release..."
      # 如果有pytest进程，则等待，直到锁文件不存在，否则，手动释放锁
      let count_pytest
      count_pytest=$(ps -ef | grep pytest| grep -v distributed=true | grep -v "/bin/sh -c" |wc -l)
      if [ $count_pytest -eq 2 ];then
         echo "2、No pytest process found in current host, so delete lockfile by manual"
         rm $LOCKFILE
         write_lock $LOCKFILE $DEVICENAME $USERNAME temp $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
         exit 0
      fi
			until [ ! -f "$LOCKFILE" ]; do # start a loop until lock file does not exist
			  sleep 3 # wait for 5 seconds
			  # 程序异常退出时，会出现没有执行pytest但是锁文件存在的情况
        let count_pytest
        count_pytest=$(ps -ef | grep pytest| grep -v distributed=true | grep -v "/bin/sh -c" |wc -l)
        if [ $count_pytest -eq 2 ];then
           echo "No pytest process found in current host, so delete lockfile by manual"
           rm $LOCKFILE
        fi
			done
			write_lock $LOCKFILE $DEVICENAME $USERNAME temp $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
			exit 0
		fi
	else
		get_lock_info "$LOCKDIR$RLOCKFILENAME"
		if [[ $OWNER == $USERNAME ]]; then
			get_lock_info "$LOCKDIR$LOCKFILENAME"
			if [[ $OWNER == $USERNAME ]]; then
				write_lock $LOCKFILE $DEVICENAME $USERNAME temp $(date '+%Y-%m-%d_%H:%M:%S') $(pwd)
			else
				echo "The information in rlock is not consistent with lock, please clear lock files forcely."
				list_all_locks
				exit 2
			fi
		else
			echo "get lock failed, it is occupied by $OWNER."
			exit 1
		fi
	fi
elif [ "$1" == "-l" ]; then
	list_all_locks
	exit 0
elif [ "$1" == "-r" ]; then
	# if [[ $(whoami) == root ]]; then
	# 	echo "Warning: Please do not run this script as root, except with '-f' option."
	# 	exit 1
	# fi
	release_owned_rlock
	release_owned_lock
elif [ "$1" == "-rr" ]; then
	# if [[ $(whoami) == root ]]; then
	# 	echo "Warning: Please do not run this script as root, except with '-f' option."
	# 	exit 1
	# fi
	release_owned_rlock
elif [ "$1" == "-rt" ]; then
	# if [[ $(whoami) == root ]]; then
	# 	echo "Warning: Please do not run this script as root, except with '-f' option."
	# 	exit 1
	# fi
	release_owned_lock
elif [ "$1" == "-f" ]; then
	seizing_lock
else
	help
fi
