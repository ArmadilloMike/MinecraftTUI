import minecraft_launcher_lib
import subprocess
from mine_utils import *


minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()


# version stuff
versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
use_version = input("What minecraft version do you want to install? ")
version_ids = [v["id"] for v in versions]
while not(use_version in version_ids):
    print("could not find it")
    use_version = input("What minecraft version do you want to install? ")
print("found it!")
use_version.replace(".","-")


# installing
minecraft_directory = f"installations/minecraft-{use_version}"
print(f"Installing minecraft at {minecraft_directory}")
callback = show_progress()
minecraft_launcher_lib.install.install_minecraft_version(use_version, minecraft_directory, callback=callback)
print(f"Minecraft version {use_version} installed!")

options = minecraft_launcher_lib.utils.generate_test_options()
options["demo"] = True


play = input("Do you want to play minecraft now? (Y/n)").lower()
if play == "y" or play == "":
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(use_version, minecraft_directory, options)
    # print(minecraft_command)
    subprocess.run(minecraft_command)