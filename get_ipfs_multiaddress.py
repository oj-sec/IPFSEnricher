#!/usr/bin/env python3

# Python module to return the multiaddresses for a given IPFS peer address by invoking an ipfs-kubo binary.

# The IPFS daemon must be running and the kubo binary must be present on the PATH.

import subprocess

def get_multiaddress(peer_address):

    cmd = f"ipfs dht findpeer {peer_address}"
    rtrn = subprocess.run(cmd, capture_output=True, shell=True)

    # Return failure signal if IPFS returns output to stderr 
    if rtrn.stderr:
        return 1, str(rtrn.stderr.decode('utf-8')+ " : " + str(peer_address))
    else:
        multiaddresses = rtrn.stdout.decode('utf-8').split('\n')
        multiaddresses.remove("")
        return 0, multiaddresses

if __name__ == "__main__":
    quit()