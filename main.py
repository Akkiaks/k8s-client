
import os
import platform
import subprocess
import sys
import getopt

"""checking if all dependecies are installed..."""
os.system("pip install -r requirements.txt")

if platform.system() == "Windows":
    try:
        os.system("where minikube")
    except:
        os.system("which minikube")
    try:
        if sys.argv[1]:
            argument = str(sys.argv[1])
            os.system("python package.py"+' '+  argument)
    except:
        os.system("python package.py")
else:
    print( "Minikube is not installed")
    print("\n\n Please install the minikube and try again") 

