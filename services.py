import requests
import os
import sys
from tqdm import tqdm

SERVICES_FILE = "services.txt"


def get_services_file_abspath():
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir_path, SERVICES_FILE)


def check_services():
    services_file = get_services_file_abspath()

    if not os.path.exists(services_file):
        print("CREATING NEW SERVICES FILE...")
        f = open(services_file, "x")
        f.close()
        print("DONE")
        return

    print("CHECKING SERVICES...")

    online: list[tuple[str, int]] = []
    offline: list[tuple[str, int]] = []

    with open(services_file, "r") as f:
        lines = f.readlines()
        num_lines = len(lines)

        for line_index in tqdm(range(num_lines), leave=True):
            url = lines[line_index].strip()
            res = requests.get(url)
            if res.status_code == 200:
                online.append((url, res.status_code))
            else:
                offline.append((url, res.status_code))

    print("DONE\n")

    print("====ONLINE====")
    for (site, _) in online:
        print(site)

    print()

    print("====OFFLINE====")
    for (site, status) in offline:
        print(site, f"(STATUS: {status})")


def edit_services_file():
    services_file = get_services_file_abspath()
    os.system(f"/usr/bin/editor {services_file}")


if __name__ == "__main__":
    expected_args = 2
    if len(sys.argv) != expected_args:
        raise Exception(
            f"invalid number of arguments: expected {expected_args}, got {len(sys.argv)}")

    option = sys.argv[1]

    if option == "check":
        check_services()
    elif option == "edit":
        edit_services_file()
    else:
        raise Exception(f"invalid option: {option}")
