import winreg as reg
import os
import subprocess
from time import sleep

print("Setting Up Zed...")

print("Checking For LLVM")
sleep(2)
Results = subprocess.run(["llvm-config", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if(Results.returncode != 0):
    Y_N = input("It Seems LLVM Is Not Installed Would You Like To Install It(y/n)")
    if(Y_N == "y"):
        subprocess.run(["winget", "install", "LLVM.LLVM"])
        print("LLVM Installed!")
    else:
        print("Not Installing LLVM May Cause Errors With The Compiling Phase")
else:
    print("LLVM Installed!")

print("Setting Up Path..")
sleep(2)
Reg_Key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Environment", 0, reg.KEY_READ | reg.KEY_WRITE)
CurrentPath, RegType = reg.QueryValueEx(Reg_Key, "Path")

if os.getcwd() not in CurrentPath:
    NewPathVal = CurrentPath + ";" + os.getcwd()
    reg.SetValueEx(Reg_Key, "Path", 0, reg.REG_EXPAND_SZ, NewPathVal)
    print("Path Set Up!")
else:
    print("Path Already Added Skipping Step")

reg.CloseKey(Reg_Key)  



#SetUp Some Libs If Needed


print("Done!, You Can Delete This File!")