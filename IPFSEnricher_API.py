#!/usr/bin/env python3

# API interface for IPFS Enricher. 

from flask import Flask, jsonify, request
import datetime
import IPFSEnricher
import get_ipfs_multiaddress
import get_ipfs_providers

app = Flask(__name__)

# Function to expose an API endpoint for resolving a CID to IP addresses provinding the CID to the IPFS network.
# Note that this function strips out IP addresses likely to relate to IPFS gateways to reduce false positives. 
@app.route("/cid_to_provider_ip/<string:cid>/")
def cid_to_provider_ip(cid):

	formatted_return = {}
	formatted_return['meta'] = {}
	formatted_return['meta']['endpoint'] = 'cid_to_provider_ip'
	formatted_return['meta']['query'] = cid
	formatted_return['meta']['requestTime'] = str(datetime.datetime.now().astimezone().replace(microsecond=0).isoformat())
	
	try:
		formatted_return['results'] = []
		providers = enricher.cid_to_provider_addresses(cid)
		formatted_return['meta']['resultCount'] = len(providers)
		formatted_return['meta']['resultType'] = 'success'
		for provider in providers.keys():
			temp = {}
			temp['provider'] = provider
			temp['IPAdresses'] = providers[provider]
			formatted_return['results'].append(temp)
			return formatted_return
	except:
		formatted_return['meta']['resultType'] = 'error'
		return formatted_return

	return formatted_return 

# Function to expose an API endpoint for resolving a CID to peer IDs.
@app.route("/cid_to_provider_id/<string:cid>/")
def cid_to_provider_id(cid):

	formatted_return = {}
	formatted_return['meta'] = {}
	formatted_return['meta']['endpoint'] = 'cid_to_provider_id'
	formatted_return['meta']['query'] = cid
	formatted_return['meta']['requestTime'] = str(datetime.datetime.now().astimezone().replace(microsecond=0).isoformat())

	try:
		providers = enricher.get_providers(cid)
		assert enricher[0] == 0
		providers = providers[1]
		formatted_return['meta']['resultCount'] = len(providers)
		formatted_return['meta']['resultType'] = 'success'
		formatted_return['results'] = []
		for provider in providers:
			temp = {}
			temp['providerID'] = provider
			formatted_return['results'].append(temp)
	except:
		formatted_return['meta']['resultType'] = 'error'
		formatted_return['data'] = enricher.get_providers(cid)[1]
	
	return formatted_return

# Function to expose an API endpoint for resolving a peer ID to multiaddresses.
@app.route("/peer_to_multiaddress/<string:peer>/")
def peer_to_multiaddress(peer):

	formatted_return = {}
	formatted_return['meta'] = {}
	formatted_return['meta']['endpoint'] = 'peer_to_multiaddress'
	formatted_return['meta']['query'] = peer
	formatted_return['meta']['requestTime'] = str(datetime.datetime.now().astimezone().replace(microsecond=0).isoformat())

	try:
		multiaddresses = enricher.get_multiaddress(peer)
		assert multiaddresses[0] == 0
		multiaddresses = multiaddresses[1]
		formatted_return['meta']['resultCount'] = len(multiaddresses)
		formatted_return['meta']['resultType'] = 'success'
		formatted_return['results'] = []
		for address in multiaddresses:
			temp = {}
			temp['multiaddresses'] = address
			formatted_return['results'].append(temp)

	except:
		formatted_return['meta']['resultType'] = 'error'
		formatted_return['data'] = multiaddresses = enricher.get_multiaddress(peer)[1]
	
	return formatted_return

if __name__ == '__main__':
	enricher = IPFSEnricher.IPFSEnricher()
	app.run(host='0.0.0.0', port=5000)
