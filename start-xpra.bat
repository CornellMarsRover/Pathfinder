@echo off

SET BASEDIR=%dp0
"C:\Program Files\Xpra\Xpra_cmd.exe" attach "--ssh="ssh -p 2222 -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o IdentityFile=%BASEDIR%.vagrant\machines\pathfinder\vmware_fusion\private_key"" ssh:vagrant@localhost:0