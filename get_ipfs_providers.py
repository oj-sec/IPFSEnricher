#!/usr/bin/env python3

# Python module to return provider peer addresses for a given IPFS content address (CID) by invoking the kubo-ipfs binary.

# The IPFS daemon must be running and the kubo binary must be present on the PATH.

import subprocess

def get_providers(cid):

    cmd = f"ipfs dht findprovs {cid}"
    rtrn = subprocess.run(cmd, capture_output=True, shell=True)

    # Return failure signal if IPFS returns output to stderr 
    if rtrn.stderr:
        return 1, str(rtrn.stderr.decode('utf-8') + " : " + str(cid))
    else:
        providers = rtrn.stdout.decode('utf-8').split('\n')
        providers.remove("")
        return 0, providers

if __name__ == "__main__":
    quit()