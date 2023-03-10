# IPFSEnricher

IPFSEnricher is a dockerized API wrapper for kubo-ipfs distributed hash table queries. IPFSEnricher is intended to facilitate the identification of IP addresses for nodes providing specific content IDs to the Inter Planetary File System (IPFS) network. 

The core use-case for IPFSEnricher is to enrich detections or external threat intelligence feeds that contain indicators related to IPFS by automating pivots to threat actor-controlled IPs. 

## Background

Threat actors are increasingly abusing IPFS to stage malware payloads and host phishing content. Threat actors abusing IPFS typically use public web gateways for delivery via HTTP, avoiding the need for the victim to communicate peer-to-peer over IPFS protocols. 

Threat actor abuse of IPFS web gateways for delivery limits opportunities for organisations to detect threats based on IP address, as threat actors do not directly expose their infrastructure during typical attacks. Using IPFSEnricher may allow organisations to identify ongoing attack patterns and develop forward detections.  

## Example

NB: this section refers to actual malicious infrastructure. 

A threat actor creates a credential phishing page and pins the files from their local IPFS node, providing the page to the IPFS network. 

The threat actor sends a phishing email to a target containing an IPFS web gateway link to their credential phishing content, e.g.- ```hxxps[:]//gateway.ipfs[.]io/ipfs/QmbLd37HqzS5Nid7yrwZVb3X28qYyVRtodF5U1gnBqTeC3``` . When the target accesses the link, the IPFS web gateway retrieves the file from the threat actor's IPFS node and serves it to the target. 

The IPFS web gateway acts as a proxy between the threat actor and the target, meaning the threat actor has served up the phishing page without exposing IP or domain name surface area. 

By using IPFSEnricher, a network defender can resolve a content ID (CID) to the IP addresses serving the content to the IPFS network. By providing the CID for the phishing page (the QmbLd.* section of the URI) the defender can identify that the credential phishing page above is being provided by a peer with multiaddresses pointing to ```157.90.132[.]176```. 

The threat actor's IP address would not normally be revealed through investigation of the attack chain. The threat actor may be able to launch multiple attacks without targets clustering intrusions and identifying a targeted attack or identifying opportunities for pivots and forward detection. 

## Usage

IPFSEnricher returns JSON data from three API endpoints:

- ```localhost/cid_to_provider_ip/{cid}```
	- returns the IP addresses of nodes supplying the provided content ID (CID) to the IPFS network. The endpoint resolves a given CID to the node IDs providing that content to the IPFS network and then resolves those nodes to multiaddresses. Multiaddresses are parsed for IPv4 strings. Finally, IPv4 strings related to IPFS web-gateways are stripped from results to reduce the incidence of false positives/low value indicators. 
- ```localhost/cid_to_provider_id/{cid}``` 
	- returns the provider IDs for nodes supplying the provided CID to the IPFS network. 
- ```localhost/peer_to_multiaddress/{peer}```
	- returns the the raw multiaddresses for a given peer ID.

IPFSEnricher does not use caching and makes queries to the IPFS network as it receives requests. These requests will often hang for 5-10 seconds while the distributed hash table is queried and should be accounted for in calling code. 

IPFSEnricher currently uses the Python Flask development web server and should not be exposed to untrusted input. 

## Installation

IPFSEnricher is intended to be deployed via docker.

To build the image from the included Dockerfile using default settings run: 

```docker image build -t IPFSEnricher .```

Alternatively, to pull the pre-built image from docker hub:

```docker pull 0jsec/IPFSEnricher:latest```

To run the container, exposing the API interface on port 5000, run:

```docker run -p 5000:5000 -d IPFSEnricher```

