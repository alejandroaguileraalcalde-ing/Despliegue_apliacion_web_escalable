#!/usr/bin/python
import sys
import subprocess
import os
import time 

from subprocess import call
from lxml import etree

numservidores = 4
#orden = sys.argv[1]



def inicioEscenario(): #apt-get install
 
 call(["cp", "/home/alejandro.aguilera.alcalde/Desktop/labCDPSCreativa2/haproxy.cfg", "."])
 call(["cp", "/home/alejandro.aguilera.alcalde/Desktop/labCDPSCreativa2/fw.fw", "."])
 call(["cp", "/home/alejandro.aguilera.alcalde/Desktop/labCDPSCreativa2/fw80.fw", "."])
 call(["sudo", "lxc-attach", "--clear-env", "-n", "lb", "--", "apt-get", "-y", "install", "haproxy"])
 
 return

def create(): #
 call(["cp", "/home/alejandro.aguilera.alcalde/Desktop/labCDPSCreativa2/pc2.xml", "."])
 call("sudo vnx -f pc2.xml --create", shell=True)
 
 return


def balanceador(numservidores):

   # echo "linea que se pone al final" >> nombrefichero

   
   call(["sudo", "lxc-attach", "--clear-env", "-n", "lb", "--", "service", "apache2", "stop"])

   
   return

   
def escribirHaproxy(numservidores):
   my_file = open("haproxy.cfg")
   string_list = my_file.readlines()
   my_file.close()
  
   
    
  # string_list[36] = "\t"+"errorfile 504 /etc/haproxy/errors/504.http"+"\n"+"frontend lb "+"\n"+"bind *:80"+"\n"+"mode http"+"\n"+"default_backend webservers"+"\n"+"backend webservers"+"\n"+"mode http"+"\n"+"balance roundrobin"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"
   
   string_list[36] = "\t"+"errorfile 504 /etc/haproxy/errors/504.http"+"\n"+"frontend lb "+"\n"+"bind *:80"+"\n"+"mode http"+"\n"+"default_backend webservers"+"\n"+"backend webservers"+"\n"+"mode http"+"\n"+"balance leastconn"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"+"\n"
   
   #igual mejor roundroubin con pesos

   my_file = open("haproxy.cfg", "w")
   new_file_contents = "".join(string_list)
   my_file.write(new_file_contents)
   my_file.close()

   for x in range (0, numservidores): 
    x1= str(x)
    xaux= str(x +1)

    my_file = open("haproxy.cfg")
    string_list = my_file.readlines()
    my_file.close()
  
   
    
    string_list[45+x] = "server s"+xaux+" 20.20.3.1"+xaux+":3000 check"+"\n"
     
    my_file = open("haproxy.cfg", "w")
    new_file_contents = "".join(string_list)
    my_file.write(new_file_contents)
    my_file.close()
    
    #añadirmos comprobacion para internet
   my_file = open("haproxy.cfg")
   string_list = my_file.readlines()
   my_file.close()
  
   
    
   string_list[50] = "listen stats"+"\n"+"bind :8001"+"\n"+"stats enable"+"\n"+"stats uri /"+"\n"+"stats hide-version"+"\n"+"stats auth admin:cdps"
   
   

   my_file = open("haproxy.cfg", "w")
   new_file_contents = "".join(string_list)
   my_file.write(new_file_contents)
   my_file.close()

   call(["sudo", "/lab/cdps/bin/cp2lxc", "haproxy.cfg", "/var/lib/lxc/lb/rootfs/etc/haproxy"])

   call(["sudo", "lxc-attach", "--clear-env", "-n", "lb", "--", "sudo", "service", "haproxy", "restart"])
   return

def firewall():
       
   call(["cp", "/home/alejandro.aguilera.alcalde/Desktop/labCDPSCreativa2/fw.fw", "."])
   call(["chmod", "777", "fw.fw"])
   call(["sudo", "/lab/cdps/bin/cp2lxc", "fw.fw", "/var/lib/lxc/fw/rootfs"])


   call(["sudo", "lxc-attach", "--clear-env", "-n", "fw", "--", "chmod", "777", "fw.fw"])
   call(["sudo", "lxc-attach", "--clear-env", "-n", "fw", "--", "./fw.fw"])
   return

def firewallextra():
       
   call(["cp", "/home/alejandro.aguilera.alcalde/Desktop/labCDPSCreativa2/fw80.fw", "."])
   call(["chmod", "777", "fw80.fw"])
   call(["sudo", "/lab/cdps/bin/cp2lxc", "fw80.fw", "/var/lib/lxc/fw/rootfs"])


   call(["sudo", "lxc-attach", "--clear-env", "-n", "fw", "--", "chmod", "777", "fw80.fw"])
   call(["sudo", "lxc-attach", "--clear-env", "-n", "fw", "--", "./fw80.fw"])
   return

def database():

 #Configuración de la Base de Datos(BBDD)
 print("Configuración de la Base de Datos(BBDD)")
 call("sudo lxc-attach --clear-env -n bbdd -- apt update", shell=True)
 call("sudo lxc-attach --clear-env -n bbdd -- apt -y install mariadb-server", shell=True)
    # Tenemos que modificar el archivo de configuración(50-server.cnf):
 call("sudo lxc-attach --clear-env -n bbdd -- sed -i -e 's/bind-address.*/bind-address=0.0.0.0/' -e 's/utf8mb4/utf8/' /etc/mysql/mariadb.conf.d/50-server.cnf", shell=True)
    # Reiniciamos mySQL para guardar la configuración
 call("sudo lxc-attach --clear-env -n bbdd -- systemctl restart mysql", shell=True)
    # Hacemos la configuración pertinente de mySQL, (creamos usuario, base de datos y configuramos permisos):
 call("sudo lxc-attach --clear-env -n bbdd -- mysqladmin -u root password xxxx", shell=True)
 call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"CREATE USER 'quiz' IDENTIFIED BY 'xxxx';\"", shell=True)
 call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"CREATE DATABASE quiz ;\"",  shell=True)
 call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'localhost' IDENTIFIED by 'xxxx';\"", shell=True)
 call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED by 'xxxx';\"", shell=True)
 call("sudo lxc-attach --clear-env -n bbdd -- mysql -u root --password='xxxx' -e \"FLUSH PRIVILEGES;\"", shell=True)
 return  
  
def glusters():
 
 
 
 call("sudo lxc-attach --clear-env -n nas1 -- apt update", shell=True)
 #call("sudo lxc-attach --clear-env -n nas1 -- gluster peer probe 20.20.4.21", shell=True)
 call("sudo lxc-attach --clear-env -n nas1 -- gluster peer probe 20.20.4.22", shell=True)
 call("sudo lxc-attach --clear-env -n nas1 -- gluster peer probe 20.20.4.23", shell=True)
 call("sudo lxc-attach --clear-env -n nas1 -- gluster peer status", shell=True)
 time.sleep(4)
 call("sudo lxc-attach --clear-env -n nas1 -- gluster volume create nas replica 3 20.20.4.21:/nas 20.20.4.22:/nas 20.20.4.23:/nas force", shell=True)
 call("sudo lxc-attach --clear-env -n nas1 -- gluster volume start nas", shell=True)
 call("sudo lxc-attach --clear-env -n nas1 -- gluster volume info", shell=True)
 call("sudo lxc-attach --clear-env -n nas1 -- gluster volume set nas network.ping-timeout 5", shell=True)

 call("sudo lxc-attach --clear-env -n s1 -- mkdir /mnt/nas", shell=True)
 call("sudo lxc-attach --clear-env -n s1 -- mount -t glusterfs 20.20.4.21:/nas /mnt/nas", shell=True)

 call("sudo lxc-attach --clear-env -n s2 -- mkdir /mnt/nas", shell=True)
 call("sudo lxc-attach --clear-env -n s2 -- mount -t glusterfs 20.20.4.22:/nas /mnt/nas", shell=True)

 call("sudo lxc-attach --clear-env -n s3 -- mkdir /mnt/nas", shell=True)
 call("sudo lxc-attach --clear-env -n s3 -- mount -t glusterfs 20.20.4.23:/nas /mnt/nas", shell=True)
 #duda de si va
 call("sudo lxc-attach --clear-env -n s4 -- mkdir /mnt/nas", shell=True)
 call("sudo lxc-attach --clear-env -n s4 -- mount -t glusterfs 20.20.4.22:/nas /mnt/nas", shell=True)
 return

def quiz():
#s1
 call("sudo lxc-attach --clear-env -n s1 -- bash -c \"cd /root; git clone https://github.com/CORE-UPM/quiz_2021.git\" ", shell=True)
 
 #mkdir -p public/uploads;

 call("sudo lxc-attach --clear-env -n s1 -- bash -c \"cd /root/quiz_2021; sed \'29 d\' app.js > app2.js; cp app2.js app.js; mkdir -p public/uploads; cd /root; ln -s /mnt/nas quiz_2021/public/uploads; cd /root/quiz_2021; npm install;npm install forever; npm install mysql2; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz; npm run-script migrate_env; npm run-script seed_env; ./node_modules/forever/bin/forever start ./bin/www\" ", shell=True) 

#s2

 call("sudo lxc-attach --clear-env -n s2 -- bash -c \"cd /root; git clone https://github.com/CORE-UPM/quiz_2021.git\" ", shell=True)
 

 call("sudo lxc-attach --clear-env -n s2 -- bash -c \"cd /root/quiz_2021; sed \'29 d\' app.js > app2.js; cp app2.js app.js; mkdir -p public/uploads;  cd /root; ln -s /mnt/nas quiz_2021/public/uploads; cd /root/quiz_2021; npm install;npm install forever; npm install mysql2; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www\" ", shell=True)

#s3

 call("sudo lxc-attach --clear-env -n s3 -- bash -c \"cd /root; git clone https://github.com/CORE-UPM/quiz_2021.git\" ", shell=True)
 

 call("sudo lxc-attach --clear-env -n s3 -- bash -c \"cd /root/quiz_2021; sed \'29 d\' app.js > app2.js; cp app2.js app.js; mkdir -p public/uploads; cd /root; ln -s /mnt/nas quiz_2021/public/uploads; cd /root/quiz_2021; npm install;npm install forever; npm install mysql2; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www\" ", shell=True)

#s4

 call("sudo lxc-attach --clear-env -n s4 -- bash -c \"cd /root; git clone https://github.com/CORE-UPM/quiz_2021.git\" ", shell=True)
 

 call("sudo lxc-attach --clear-env -n s4 -- bash -c \"cd /root/quiz_2021; sed \'29 d\' app.js > app2.js; cp app2.js app.js; mkdir -p public/uploads; cd /root; ln -s /mnt/nas quiz_2021/public/uploads; cd /root/quiz_2021; npm install;npm install forever; npm install mysql2; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www\" ", shell=True)
 return

   
create()
inicioEscenario()
balanceador(numservidores)
escribirHaproxy(numservidores)
#firewall()
firewallextra()
database()
glusters()
#glusters()
quiz()



