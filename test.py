import minecraft_launcher_lib


current_max = 0


def set_status(status: str):
    print(status)


def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")


def set_max(new_max: int):
    global current_max
    current_max = new_max


minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

minecraft_launcher_lib.install.install_minecraft_version("1.17", minecraft_directory, callback=callback)