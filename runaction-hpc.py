import argparse
import sys
from xml.etree import ElementTree as ET
import oca

EXCEPTIONS = {'terminate': [66789]}

ADDRESS = 'https://api.hpccloud.surfsara.nl/RPC2'

STATES = {
    0: "INIT",
    1: "PENDING",
    2: "HOLD",
    3: "ACTIVE",
    4: "STOPPED",
    5: "SUSPENDED",
    6: "DONE",
    7: "FAILED",
    8: "POWEROFF",
    9: "UNDEPLOYED",
    10: "CLONING",
    11: "CLONING_FAILURE",
}
LCM_STATES = {
    0: "LCM_INIT",
    1: "PROLOG",
    2: "BOOT",
    3: "RUNNING",
    4: "MIGRATE",
    5: "SAVE_STOP",
    6: "SAVE_SUSPEND",
    7: "SAVE_MIGRATE",
    8: "PROLOG_MIGRATE",
    9: "PROLOG_RESUME",
    10: "EPILOG_STOP",
    11: "EPILOG",
    12: "SHUTDOWN",
    13: "//CANCEL",
    14: "//FAILURE",
    15: "CLEANUP_RESUBMIT",
    16: "UNKNOWN",
    17: "HOTPLUG",
    18: "SHUTDOWN_POWEROFF",
    19: "BOOT_UNKNOWN",
    20: "BOOT_POWEROFF",
    21: "BOOT_SUSPENDED",
    22: "BOOT_STOPPED",
    23: "CLEANUP_DELETE",
    24: "HOTPLUG_SNAPSHOT",
    25: "HOTPLUG_NIC",
    26: "HOTPLUG_SAVEAS",
    27: "HOTPLUG_SAVEAS_POWEROFF",
    28: "HOTPLUG_SAVEAS_SUSPENDED",
    29: "SHUTDOWN_UNDEPLOY",
    30: "EPILOG_UNDEPLOY",
    31: "PROLOG_UNDEPLOY",
    32: "BOOT_UNDEPLOY",
    33: "HOTPLUG_PROLOG_POWEROFF",
    34: "HOTPLUG_EPILOG_POWEROFF",
    35: "BOOT_MIGRATE",
    36: "BOOT_FAILURE",
    37: "BOOT_MIGRATE_FAILURE",
    38: "PROLOG_MIGRATE_FAILURE",
    39: "PROLOG_FAILURE",
    40: "EPILOG_FAILURE",
    41: "EPILOG_STOP_FAILURE",
    42: "EPILOG_UNDEPLOY_FAILURE",
    43: "PROLOG_MIGRATE_POWEROFF",
    44: "PROLOG_MIGRATE_POWEROFF_FAILURE",
    45: "PROLOG_MIGRATE_SUSPEND",
    46: "PROLOG_MIGRATE_SUSPEND_FAILURE",
    47: "BOOT_UNDEPLOY_FAILURE",
    48: "BOOT_STOPPED_FAILURE",
    49: "PROLOG_RESUME_FAILURE",
    50: "PROLOG_UNDEPLOY_FAILURE",
    51: "DISK_SNAPSHOT_POWEROFF",
    52: "DISK_SNAPSHOT_REVERT_POWEROFF",
    53: "DISK_SNAPSHOT_DELETE_POWEROFF",
    54: "DISK_SNAPSHOT_SUSPENDED",
    55: "DISK_SNAPSHOT_REVERT_SUSPENDED",
    56: "DISK_SNAPSHOT_DELETE_SUSPENDED",
    57: "DISK_SNAPSHOT",
    58: "//DISK_SNAPSHOT_REVERT",
    59: "DISK_SNAPSHOT_DELETE",
    60: "PROLOG_MIGRATE_UNKNOWN",
    61: "PROLOG_MIGRATE_UNKNOWN_FAILURE",
    62: "DISK_RESIZE",
    63: "DISK_RESIZE_POWEROFF",
    64: "DISK_RESIZE_UNDEPLOYED",
}


#    LCM_INIT PROLOG BOOT RUNNING MIGRATE SAVE_STOP SAVE_SUSPEND
#    SAVE_MIGRATE PROLOG_MIGRATE PROLOG_RESUME EPILOG_STOP EPILOG
#    SHUTDOWN CANCEL FAILURE CLEANUP UNKNOWN""".split()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['list', 'terminate'])
    parser.add_argument('ids', nargs='*')
    parser.add_argument('-i', '--confirm', action='store_true',
                        help="Confirm the action for each VM")
    args = parser.parse_args()
    args.command = args.command.lower()
    return args


def main(command, ids, confirm=False):
    client = oca.Client(None, address=ADDRESS)

    result = client.call('vmpool.info', -1, -1, -1, -1)
    root = ET.fromstring(result)
    #ET.dump(root)
    #exit()
    nodes = []
    for node in root.findall('./VM/ID/..'):
        nodes.append({'id': int(node.find('ID').text),
                      'name': node.find('NAME').text,
                      'ip': node.find('TEMPLATE/CONTEXT/ETH0_IP').text,
                      'state': (STATES[int(node.find('STATE').text)],
                                LCM_STATES[int(node.find('LCM_STATE').text)]),
        })
    if command == 'list':
        for node in nodes:
            print('id =', node['id'])
            print('name =', node['name'])
            print('ip =', node['ip'])
            print('state =', node['state'])
            print()

    else:
        for idx in ids:
            idx = int(idx)
            node = next((node for node in nodes if node['id'] == idx), None)
            if not node:
                print("ID", idx, "not found!")
                continue
            if confirm:
                while True:
                    answer = input(f"Run {command} for VM id: {node['id']}, name: {node['name']}, ip: {node['ip']} (yes/no) ").lower()
                    if answer in ['yes', 'no']:
                        break
                    print("Please answer 'yes' or 'no'")
                if answer == 'no':
                    continue
            if idx in EXCEPTIONS.get(command, []):
                sys.stderr.write(
                    f"    Not terminating {idx}: this VM is in the " +
                    f"exceptions for the '{command}' command\n")
                continue
            result = client.call('vm.action', command, idx)
            print(result)


if __name__ == '__main__':
    args = parse_args()
    main(args.command, args.ids, args.confirm)
