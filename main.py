import minecraft_launcher_lib
import subprocess


minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
use_version = input("What minecraft version do you want to install? ")

minecraft_directory = "installations/minecraft-1-17-1"
print(f"Installing minecraft at {minecraft_directory}")
#minecraft_launcher_lib.install.install_minecraft_version("1.17", minecraft_directory)

#options = minecraft_launcher_lib.utils.generate_test_options()
#options["demo"] = True

#minecraft_command = minecraft_launcher_lib.command.get_minecraft_command("1.17", minecraft_directory, options)
#print(minecraft_command)
#subprocess.run(minecraft_command)



