#!/bin/bash
IFS=$'\n'			#以换行为分隔符取变量 
j=0
i=1
current_time=`date +%H-%M`
echo "行号	应用名		域名    	PING平均延时		PING最大延时		丢包率"
echo "行号	应用名		域名    	PING平均延时		PING最大延时		丢包率" > result-"$current_time".txt
for line in `cat $1`	#使用循环按顺序读取/opt/iptest/ip中的IP
do
  let j=i++		#循环次数
  #echo "第'$j'次获取"		 #打印并输出显示
  appname=`echo $line | awk '{print $1}'`		 
  domain=`echo $line | awk '{print $2}'`
  #echo $domain
  #echo $appname
  echo "" >> log-"$current_time".txt
  echo "第$j行：$line" >> log-"$current_time".txt		 #打印并输出显示
  ping -i 1 -c 60 $domain> output.txt
  echo "执行结果：" >> log-"$current_time".txt
  cat output.txt >> log-"$current_time".txt

  for row in `cat output.txt`
  do
     if [[ $row == *loss* ]]
     then
	 loss_rate=`echo $row | awk -F "," '{print $3}' |awk '{print $1}'`
     fi
     if [[ $row == rtt* ]]
     then
	  average_delay=`echo $row | awk '{print $4}' | awk -F "/" '{print $2}'`
	  max_delay=`echo $row | awk '{print $4}' | awk -F "/" '{print $3}'`
     fi
  done
  
  #echo "=================result=============="
  echo "$j	$appname	$domain		$average_delay		$max_delay		$loss_rate"
  echo "$j	$appname	$domain		$average_delay		$max_delay		$loss_rate" >> result-"$current_time".txt
  echo "====================================================================" >> log-"$current_time".txt
done

