#!/usr/bin/env python3

# Program to coordinate queries to the IPFS network made by IPFSEnricher.

import subprocess
import socket
import ipaddress
import get_ipfs_multiaddress
import get_ipfs_providers

# Function to resolve the DNS names for IPFS gateway to IP addresses.
def resolve_gateway_ips():
    gateway_ips = []
    with open('gateway_domains', 'r') as f:
        gateway_dns_names = f.read().splitlines()
        for gateway in gateway_dns_names:
            try:
                gateway_ips.append(socket.gethostbyname(gateway))
            except:
                pass
    return gateway_ips

# Class defining an IPFSEnricher object.
class IPFSEnricher:

    # Initialisation method.
    def __init__(self):
        # Initialise the ipfs node.
        cmd = "ipfs init"
        subprocess.run(cmd, shell=True)
        # Start an instance of the IPFS daemon. 
        cmd = "nohup ipfs daemon &"
        subprocess.run(cmd, shell=True)
        # Retrieve IP addresses for the current gateways
        self.gateway_ips = resolve_gateway_ips()

    # Getter method for the gateway_ips attribute.
    def get_gateway_ips(self):
        attributes = self.__dict__
        return attributes['gateway_ips']

    # Function to retrieve multiaddresses for a given peer address. 
    def get_multiaddress(self, peer_address):

        multiaddresses = get_ipfs_multiaddress.get_multiaddress(peer_address)
        return multiaddresses

    # Function to retrieve providers for a given CID.
    def get_providers(self, cid):

        providers = get_ipfs_providers.get_providers(cid)
        return providers

    # Function to retrieve provider multiaddresses for a given CID.
    # Returns a dictionary containing mutliaddresses (values) for each provider (key).
    def cid_to_provider_multiaddresses(self, cid):

        providers = self.get_providers(cid)
        providers = providers[1]
        all_multiaddresses = {}

        if providers:
            for provider in providers:
                multiaddresses = self.get_multiaddress(provider)
                if multiaddresses[1]:
                    all_multiaddresses[provider] = multiaddresses[1]
        else:
            return []

        return all_multiaddresses

    # Function to retrieve provider addressess for a given CID.
    # Returns a dictionary containing parsed addresses (values) for each provider (key).
    def cid_to_provider_addresses(self, cid):

        providers = self.get_providers(cid)
        providers = providers[1]
        all_multiaddresses = {}

        if providers:
            for provider in providers:
                multiaddresses = self.get_multiaddress(provider)
                if multiaddresses[1]:
                    all_multiaddresses[provider] = self.clean_multiaddresses(multiaddresses[1])
        else:
            return []

        return all_multiaddresses

    # Function to clean up multiaddresses by removing non-ipv4 addresses, private address space and gateways. 
    def clean_multiaddresses(self, multiaddresses):

        clean_addresses = []

        # Parse out public IPv4 addresses.
        for multiaddress in multiaddresses:
            chunks = multiaddress.split("/")
            for chunk in chunks:
                try:
                    ip = ipaddress.ip_address(chunk)
                    if "IPv4" in str(type(ip)):
                        if not ipaddress.ip_address(chunk).is_private:
                            clean_addresses.append(chunk)
                except:
                    pass

        clean_addresses = list(dict.fromkeys(clean_addresses))

        # Remove IPv4 addressess that are IPFS gateways.
        for clean_address in clean_addresses:
            if clean_addresses in self.get_gateway_ips():
                clean_addresses.remove(clean_address)

        return clean_addresses

if __name__ == "__main__":

    pass


