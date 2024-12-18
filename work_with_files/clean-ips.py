import os
import argparse
import ipaddress

def filter_valid_ips(ip_list):
    """
    Filters out invalid IP addresses from a list.

    Args:
        ip_list (list): List of IP addresses as strings.

    Returns:
        list: A list containing only valid IPv4Addresses objects.
    """
    valid_ips = []
    for ip in ip_list:
        try:
            addr_obj = ipaddress.ip_address(ip)
            valid_ips.append(addr_obj)
        except ValueError:
            pass


    valid_ips = sorted(valid_ips)
    return valid_ips

def read_file_to_list(file_path):
    try:
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for file '{file_path}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main(f1, f2, f3):
    """
    A simple function that takes two positional arguments  f1  a file with a list of ips to process,
    f2 a file with a list of ips that must be removed and optional third argument f3  with name
    that result file must have
    """
    # f1s = 0
    # f2s = 0
    try:
        f1s =os.path.getsize(f1) 
    except OSError:
        print(f"os error while get size for {f1}")
    
    try:
        f2s =os.path.getsize(f2) 
    except OSError:
        print(f"os error while get size for {f2}")


    if (f1s == 0):
        print("file {ip_list} has no IPs to process")
        sys.exit(0)
    if (f2s == 0):
        print("theres is no  IPs to process in {bad_ip_list} file")
        sys.exit(0)

    ip_list = read_file_to_list(f1)
    ip_list = filter_valid_ips(ip_list)

    if len(ip_list)  == 0:
        print("after filtering invalid ips allowed ip list is empty")
        sys.exit(0)

    bad_ip_list = read_file_to_list(f2)
    bad_ip_list = filter_valid_ips(bad_ip_list)

    if len(bad_ip_list)  == 0:
        print("after filtering invalid ips bad ip list is empty")
        sys.exit(0)

    result_list = []
    for ip in bad_ip_list:
        if ip in ip_list:
            ip_list.remove(ip)

    with open(f3, "w") as f:
        for ip in ip_list:
            f.write(f"{ip}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to demonstrate three input parameters.")

    # Adding three parameters as arguments
    parser.add_argument("ips_file", type=str, help="Name of file with IPs")
    parser.add_argument("bad_ips_file", type=str, help="Name of file with bad IPs")
    parser.add_argument("--result_file", type=str, default="good_ips", help="Name of file with result")

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.ips_file, args.bad_ips_file, args.result_file)

