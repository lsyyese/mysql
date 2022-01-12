一、消息库目前信息：

读写VIP:10.215.84.213(读写) --->10.215.84.20
只读VIP:10.215.84.214(只读) --->10.215.84.154

原主库(读写):10.215.84.20(读写)
原从库(只读):10.215.84.154(只读)
备库(只读):10.215.84.21(备份)


keepalived配置信息
10.215.84.20：
读写VIP 10.215.84.213 priority 100 非抢占模式 
只读VIP 10.215.84.214 priority 90 非抢占模式
10.215.84.154：
读写VIP 10.215.84.213 priority 90 非抢占模式
只读VIP 10.215.84.214 priority 100 抢占模式


二、模拟故障演练

1、在10.215.84.20、10.215.84.154 /etc/keepalived/master.sh 中添加flush logs;使切换后得到一个新的binlog文件

2、模拟故障
10.215.84.20> service notice stop
              service keepalived stop
   
检查VIP漂移状态 确保10.215.84.213飘逸到10.215.84.154
此时 10.215.84.213 10.215.84.214 均在10.215.84.154 ,且10.215.84.154数据库为可写状态,说明飘逸正常。

3、搭建主从10.215.84.154到10.215.84.20的复制
重新启动10.215.84.20
10.215.84.20> service notice start
主从都设只读
10.215.84.20>
mysql> set global read_only = 1;    
10.215.84.154>
mysql> set global read_only = 1; 

10.215.84.20>
stop slave;reset slave;reset slave all;

change master to \
    master_host='10.215.84.154', \
    master_port=3307, \
    master_user='repl', \
    master_password='', \
    master_log_file='bin.008598', \
    master_log_pos=123;
start slave;

检查复制状态,show slave status\G
position 从10.215.84.154binlog文件取
此时搭建好10.215.84.154到10.215.84.20的复制


##########################################################################

三、恢复到演练前
1、VIP切换
原主库
10.215.84.20> service keepalived start
原从库
10.215.84.154> service keepalived stop

此时 10.215.84.213 10.215.84.214 均在10.215.84.20 ,且10.215.84.20数据库为可写状态,说明飘逸正常。
演练导致的数据库不可写、业务不可用现在恢复

2、搭建主从10.215.84.20到10.215.84.154的复制

10.215.84.154>
reset master;stop slave;reset slave;reset slave all;

change master to \
    master_host='10.215.84.20', \
    master_port=3307, \
    master_user='repl', \
    master_password='', \
    master_log_file='bin.019781', \
    master_log_pos=123;
start slave;

检查复制状态,show slave status\G
position 从10.215.84.20binlog文件取
此时搭建好10.215.84.20到10.215.84.154的复制

3、10.215.84.154> service keepalived start  抢占模式 且优先级高
此时 10.215.84.214 飘回到10.215.84.154 ,10.215.84.213在10.215.84.20 回到演练前

4、检查只读状态
110.215.84.154>
mysql> set global read_only = 1;    
10.215.84.20>
mysql> set global read_only = 0; 

########################################
四、数据校验

1、校验主从一致，优维工具10.215.84.20和10.215.84.154

2、数据修复
pt-table-sync --replicate=percona.checksums h=主库,u=percona,p=,P=3307,D=smartwatch,t=t_watch_app_version_new_100 h=从库,u=percona,p=p3O#6Oberc_66on,P=3307 --verbose --execute
