import sys
import argparse
from xml.etree import ElementTree as ET
import oca

ADDRESS = 'https://api.hpccloud.surfsara.nl/RPC2'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('id', type=int, help="Template ID", nargs='*')
    parser.add_argument('--name', default='', help="VM name")
    parser.add_argument('-m', '--memory', default=3072, type=int, help="Memory (MB)")
    parser.add_argument('-c', '--cpu', default=2, type=int, help="Number of CPU cores")
    parser.add_argument('-C', '--vcpu', default=2, type=int,
                        help="Number of virtual CPU cores")
    args = parser.parse_args()
    return args


def main(idx, name='', memory=2048, cpu=2, vcpu=2):
    client = oca.Client(None, address=ADDRESS)

    if not idx:
        result = client.call('templatepool.info', -3, -1, -1)
        root = ET.fromstring(result)
        for node in root.findall('./VMTEMPLATE'):
            idx = int(node.find('ID').text)
            name = node.find('NAME').text
            print(f"VM {name}: id {idx}")
        return

    options = f"memory={memory} cpu={cpu} vcpu={vcpu}"
    for id in idx:
        # [secret,] ID, name, hold/pending, extra-attrs, persistent
        vmid = client.call('template.instantiate', id, name, False, options, False)
        print("Started VM with ID =", vmid)


if __name__ == '__main__':
    args = parse_args()
    main(args.id, name=args.name, memory=args.memory, cpu=args.cpu,
         vcpu=args.vcpu)
