import os
import sys
import asyncio
import aiohttp
import time

SERVICES_FILE = "services.txt"
EDITOR_CMD = "/usr/bin/editor"


def get_services_file_abspath():
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir_path, SERVICES_FILE)


async def check_service(session: aiohttp.ClientSession, url: str):
    res = await session.get(url)
    res_status = res.status
    if res_status == 200:
        print(f"ONLINE [{res_status}] {url}")
    else:
        print(f"OFFLINE [{res_status}] {url}")


async def check_services():
    services_file = get_services_file_abspath()

    if not os.path.exists(services_file):
        print("CREATING NEW SERVICES FILE...")
        f = open(services_file, "x")
        f.close()
        print("DONE")
        return

    print("=====CHECKING SERVICES=====")

    lines = []
    with open(services_file, "r") as f:
        lines = f.readlines()

    async with aiohttp.ClientSession() as session:
        tasks = [check_service(session, line.strip()) for line in lines]
        await asyncio.gather(*tasks, return_exceptions=True)


def edit_services_file():
    services_file = get_services_file_abspath()
    os.system(f"{EDITOR_CMD} {services_file}")


def list_services():
    services_file = get_services_file_abspath()
    with open(services_file) as f:
        contents = f.read()
        print(contents)


def print_help_menu():
    text = """=====HELP=====
`CMD check` checks all the services in the service file
`CMD edit` opens the serviecs file in the default sytem editor (at /usr/bin/editor)
`CMD ls` lists all services in the service file
`CMD help` displays this menu

where CMD is the command to execute this script
"""
    print(text)


if __name__ == "__main__":
    expected_args = 1
    args = sys.argv[1:]
    if len(args) == 0:
        print_help_menu()
        exit(0)
    elif len(args) != expected_args:
        print(
            f"error: invalid number of arguments: expected {expected_args}, got {len(args)}")
        exit(1)

    option = args[0]

    try:
        if option == "check":
            t0 = time.time()
            asyncio.run(check_services())
            t1 = time.time()

            print(f"Finished in {t1 - t0} seconds")
        elif option == "edit":
            edit_services_file()
        elif option == "ls":
            list_services()
        elif option == "help":
            print_help_menu()
        else:
            print(
                f"error: invalid option: {option}, use `help` for a list of commands")
            exit(1)
    except Exception as e:
        print(f"error: {e}")
        exit(1)
