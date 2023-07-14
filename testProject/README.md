# **SETUP INTSTRUCTIONS**

## **Source Code Compilation** 
After you installed ALT linux download files(clipp.py, packetparcer.py) to the directory you want let it be home/'username'/Загрузки swich your current work directory to home/'username'/Загрузки than you have to install *pip* to have opportunity to install outer modules. use this command:
**apt-get install pip**:
Soon after that install *pyinstaller*, *requests* and *binutils* to compile source code into executable file. use this commands:
**apt-get install binutils**;
**pip install pyinstaller**;
**pip install requests**;
Than compile it. use this command:
**pyinstaller --onefile clipp.py**;
After process completed your utility would be at home/'username'/Загрузки/dist

## **Installation** ##
Soon after you get your utility in any directory switch it's RWX-bytes make it executable (you have to be in utility's directory). use this command:
**chmod -c 0755 clipp**
Than switch it's path to path from PATH. use this command:
**echo $PATH** -> path0:path1:path2
**mv clipp 'path0'**
Now you can use installed util as linux CLI util. To start use this command:
**clipp** OR **./clipp**


