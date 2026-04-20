import minecraft_launcher_lib

minecraft_directory = "installations/minecraft-1-17-1"
minecraft_launcher_lib.install.install_minecraft_version("1.17", minecraft_directory)

options = minecraft_launcher_lib.utils.generate_test_options()

minecraft_command = minecraft_launcher_lib.command.get_minecraft_command("1.17", minecraft_directory, options)
print(minecraft_command)
