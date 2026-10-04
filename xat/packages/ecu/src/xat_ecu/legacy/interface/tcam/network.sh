if [ $1 -eq 1 ];then 
   cat /dev/smd8 & echo -en "AT+COPS?\r\n" > /dev/smd8
elif [ $1 -eq 2 ];then
   cat /dev/smd8 & echo -en "AT+CIMI\r\n" > /dev/smd8
elif [ $1 -eq 3 ];then
   cat /dev/smd8 & echo -en "AT+CFUN=0\r\n" > /dev/smd8
elif [ $1 -eq 4 ];then
   cat /dev/smd8 & echo -en "AT+CFUN=1\r\n" > /dev/smd8
elif [ $1 -eq 5 ];then
  cat /dev/smd8 & echo -en "AT+csq\r\n" > /dev/smd8
elif [ $1 -eq 6 ];then
  cat /dev/smd8 & echo -en "at+creg?\r\n" > /dev/smd8
else echo "false"
fi
