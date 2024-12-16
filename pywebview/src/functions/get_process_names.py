import psutil

def get_process_names():
    """
    Get list of unique process names,
    including hidden applications
    (without active windows).
    """
    unique_apps = set()

    for process in psutil.process_iter(attrs=['name']):
        try:
            name = process.info['name']
            if name:
                unique_apps.add(name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Ignore processes that don't have a name or are zombie
            continue

    return sorted(unique_apps)