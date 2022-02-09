while read line
do
_IP=`echo $line |awk '{print $1}'`
_PORT=`echo $line |awk '{print $2}'`

mysql -h$_IP -udevops_bbk -p'' -P$_PORT mysql -e "show slave status\G; show variables like '%read_onl%';"


done <list.txt
#########################

function autossh()
{       filepath="$1"
        expect -c "
                set timeout -1
                spawn  scp -P 44422  $filepath dbatmp@10.35.185.8:/tmp
                expect {
                          \"(yes/no)?\"                         {send \"yes\r\";exp_continue}
                          \"password:\"                        {send \"$remotePwd\r\";exp_continue}
						  \"wish to overwrite\"                 {send \"y\r\";exp_continue}
                          \"FATAL\"                             {exit 2;exp_continue}
                          timeout                               {exit 2;exp_continue}
                          \"No route to host\"                  {exit 2;exp_continue}
                          \"Connection Refused\"                {exit 2;exp_continue}
                          \"Connection refused\"                {exit 2;exp_continue}
                          \"Host key verification failed\"      {exit 2;exp_continue}
                          \"Illegal host key\"                  {exit 2;exp_continue}
                          \"Connection Timed Out\"              {exit 2;exp_continue}
                          \"Connection timed out\"              {exit 2;exp_continue}
                          \"Interrupted system call\"           {exit 2;exp_continue}
                          \"Disconnected; connection lost\"     {exit 2;exp_continue}
                          \"Authentication failed\"             {exit 2;exp_continue}
                          \"File exists\"                       {exit 2;exp_continue}
                          \"Error\"                             {exit 2;exp_continue}
                          \"ERROR\"                             {exit 2;exp_continue}
                          \"error\"                             {exit 2;exp_continue}
                          \"No such file\"                      {exit 2;exp_continue}
                          \"Permission denied\"                 {exit 2;exp_continue}
                          \"Destination Unreachable\"           {exit 2}
                       }
        "
		if [[ $? -ne 0 ]];then
           echo "scp执行错误退出"
           exit 1

        fi
}

remotePwd='MKJJSabc2343434'
filepath=$1  
autossh  $filepath
