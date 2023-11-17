import sys
import json
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--pid',
        type=str,
        help="specify "
    )
    parser.add_argument(
        '--process-name',
        type=str,
        help="specify process name"
    )
    parser.add_argument(
        '--operation',
        type=str,
        help="specify operation for filter"
    )
    parser.add_argument(
        '--file',
        type=str,
    )
    parser.add_argument('--path', type=str)
    parser.add_argument('--str', action="store_true")
    parser.add_argument('--exclude', action="store_true")
    parser.add_argument('--print-all-processes', action='store_true')
    parser.add_argument('--print-all-processes-without-details', action='store_true')
    parser.add_argument('--only-processes', action='store_true')
    parser.add_argument('--only-events', action='store_true')
    parser.add_argument('--events', action='store_true')
    return parser


def pretty_print_events(events: list):
    print("EVENTS:")
    for event in events:
        for key, value in event.items():
            print("{}: {}".format(key, value))
        print("=" * 30)


def pretty_print_processes(pr: dict):
    print("\n\nPROCESSES:")
    for proc in pr:
        for key, value in proc.items():
            print("{}: {}".format(key, value))
        print("=" * 30)


def match_event(event: dict, filter_keys: dict) -> bool:
    pid_match = ("PID" in filter_keys and event.get("PID") == filter_keys.get("PID")) or "PID" not in filter_keys
    operation_match = ("Operation" in filter_keys and
                       event.get("Operation") == filter_keys.get("Operation")) or \
                      "Operation" not in filter_keys
    process_name_match = ("Process_Name" in filter_keys and
                          event.get("Process_Name") == filter_keys.get("Process_Name")) or \
                         "Process_Name" not in filter_keys
    path_match = ("Path" in filter_keys and event.get("Path") == filter_keys.get("Path")) or "Path" not in filter_keys
    return pid_match & operation_match & process_name_match & path_match


def match_processes(process: dict, filter_keys: dict) -> bool:
    pid_match = ("PID" in filter_keys and process.get("ProcessId") == filter_keys.get("PID")) or "PID" not in filter_keys
    process_name_match = ("Process_Name" in filter_keys and
                          process.get("ProcessName") == filter_keys.get("Process_Name")) or \
                         "Process_Name" not in filter_keys
    return pid_match & process_name_match


def filter_json(file: dict, keys: dict) -> dict:
    events = file["procmon"]["eventlist"]["event"]
    processes = file["procmon"]["processlist"]["process"]
    res = {
        "events": [],
        "processes": []
    }
    for event in events:
        if (match_event(event, keys) and "Exclude" not in keys.keys()) or (not match_event(event, keys) and "Exclude" in keys.keys()):
            res["events"].append(event)
    for pr in processes:
        if (match_processes(pr, keys) and "Exclude" not in keys.keys()) or (not match_event(event, keys) and "Exclude" in keys.keys()):
            res["processes"].append(pr)
    return res


def show_all_processes_without_details(processes: dict) -> list:
    process_set = set()
    for proc in processes:
        process_set.add(proc["ProcessName"])
    process_list = list(process_set)
    return process_list


def show_all_processes(processes: dict) -> list:
    pass  # TODO: fix after


def main():
    filter_keys = {}
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    with open("Logfile.JSON", "r") as logfile:
        data = json.load(logfile)
    if namespace.print_all_processes_without_details:
        print("PROCESS_NAME:")
        proc_list = show_all_processes_without_details(data["procmon"]["processlist"]["process"])
        for i in range(len(proc_list)):
            print('{}: {}'. format(i + 1, proc_list[i]))
    elif namespace.print_all_processes:
        proc_list = show_all_processes(data["procmon"]["processlist"]["process"])
        pretty_print_processes(data["procmon"]["processlist"]["process"])
    else:
        if namespace.pid:
            filter_keys["PID"] = namespace.pid
        if namespace.process_name:
            filter_keys["Process_Name"] = namespace.process_name
        if namespace.operation:
            filter_keys["Operation"] = namespace.operation
        if namespace.path:
            filter_keys["Path"] = namespace.path
        if namespace.exclude:
            filter_keys["Exclude"] = 1
        if "Operation" not in filter_keys and "PID" not in filter_keys and "Process_Name" not in filter_keys and "Path" not in filter_keys:
            if namespace.str:
                data_str = json.dumps(data)
                print(data_str)
            else:
                pretty_print_events(data["procmon"]["eventlist"]["event"])
                pretty_print_processes(data["procmon"]["processlist"]["proces"])
        else:
            data = filter_json(data, filter_keys)
            if namespace.file:
                with open(namespace.file, "w") as output_file:
                    json.dump(data, output_file)
            elif namespace.str:
                data_str = json.dumps(data)
                print(data_str)
            else:
                if len(data["events"]) != 0 and not namespace.only_processes:
                    pretty_print_events(data["events"])
                if len(data["processes"]) != 0 and not namespace.only_events:
                    pretty_print_processes(data["processes"])


if __name__ == "__main__":
    main()
