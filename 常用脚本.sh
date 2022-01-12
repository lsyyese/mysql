while read line
do
_IP=`echo $line |awk '{print $1}'`
_PORT=`echo $line |awk '{print $2}'`

mysql -h$_IP -udevops_bbk -p'' -P$_PORT mysql -e "show slave status\G; show variables like '%read_onl%';"


done <list.txt
