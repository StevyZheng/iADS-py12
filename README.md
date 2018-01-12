# iADS
iads 1.0.0
iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg.
Please makesure these tools are installed.

help menu list:
+-----------------------------+------------------------------------------------------------------+
| Command                     | Help text                                                        |
+-----------------------------+------------------------------------------------------------------+
| iads show help              | Show this help menu.                                             |
+-----------------------------+------------------------------------------------------------------+
| iads show bios-info         | Show BIOS all info.                                              |
+-----------------------------+------------------------------------------------------------------+
| iads show bios-ver          | Show BIOS date version.                                          |
+-----------------------------+------------------------------------------------------------------+
| iads show bios-date         | Show BIOS date date.                                             |
+-----------------------------+------------------------------------------------------------------+
| iads show mem-model         | Show memory model.                                               |
+-----------------------------+------------------------------------------------------------------+
| iads show cpu-info          | Show CPU info.                                                   |
+-----------------------------+------------------------------------------------------------------+
| iads show err-phy           | Show phys which have error.                                      |
+-----------------------------+------------------------------------------------------------------+
| iads show err-disk          | Show disks which have errors.                                    |
+-----------------------------+------------------------------------------------------------------+
| iads monitor gpu            | Monitor the temperature of GPUs and adjust the speed of the fan. |
+-----------------------------+------------------------------------------------------------------+
| iads logging all            | Logging all the log.                                             |
+-----------------------------+------------------------------------------------------------------+
| iads logging upload         | Upload the log to server, only used in product line.             |
+-----------------------------+------------------------------------------------------------------+
| iads run linpack <minutes>  | Run python linpack cpu and memory stress program.  o_o           |
| iads run paoyali <minutes>  | no param <minutes> means that always running.                    |
+-----------------------------+------------------------------------------------------------------+
stevy@stevy:~/PycharmProjects/iADS$ sudo python iads.py show help
iads 1.0.0
iads require dmidecode, smartctl, lsscsi, lsblk, sas3ircu, sas2ircu, ipmicfg.
Please makesure these tools are installed.

help menu list:
+-----------------------------+------------------------------------------------------------------+
| Command                     | Help text                                                        |
+-----------------------------+------------------------------------------------------------------+
| iads show help              | Show this help menu.                                             |
+-----------------------------+------------------------------------------------------------------+
| iads show bios-info         | Show BIOS all info.                                              |
+-----------------------------+------------------------------------------------------------------+
| iads show bios-ver          | Show BIOS date version.                                          |
+-----------------------------+------------------------------------------------------------------+
| iads show bios-date         | Show BIOS date date.                                             |
+-----------------------------+------------------------------------------------------------------+
| iads show mem-model         | Show memory model.                                               |
+-----------------------------+------------------------------------------------------------------+
| iads show cpu-info          | Show CPU info.                                                   |
+-----------------------------+------------------------------------------------------------------+
| iads show err-phy           | Show phys which have error.                                      |
+-----------------------------+------------------------------------------------------------------+
| iads show err-disk          | Show disks which have errors.                                    |
+-----------------------------+------------------------------------------------------------------+
| iads monitor gpu            | Monitor the temperature of GPUs and adjust the speed of the fan. |
+-----------------------------+------------------------------------------------------------------+
| iads logging all            | Logging all the log.                                             |
+-----------------------------+------------------------------------------------------------------+
| iads logging upload         | Upload the log to server, only used in product line.             |
+-----------------------------+------------------------------------------------------------------+
| iads run linpack <minutes>  | Run python linpack cpu and memory stress program,                |
| iads run paoyali <minutes>  | no param <minutes> means that always running. o_o                |
+-----------------------------+------------------------------------------------------------------+


    