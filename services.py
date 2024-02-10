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

    print("CHECKING SERVICES...")

    lines = []
    with open(services_file, "r") as f:
        lines = f.readlines()

    async with aiohttp.ClientSession() as session:
        tasks = [check_service(session, line.strip()) for line in lines]
        await asyncio.gather(*tasks, return_exceptions=True)

    print("DONE")


def edit_services_file():
    services_file = get_services_file_abspath()
    os.system(f"{EDITOR_CMD} {services_file}")


if __name__ == "__main__":
    expected_args = 2
    if len(sys.argv) != expected_args:
        raise Exception(
            f"invalid number of arguments: expected {expected_args}, got {len(sys.argv)}")

    option = sys.argv[1]

    if option == "check":
        t0 = time.time()
        asyncio.run(check_services())
        t1 = time.time()

        print(f"Finished in {t1 - t0} seconds")
    elif option == "edit":
        edit_services_file()
    else:
        raise Exception(f"invalid option: {option}")
