import os
import json
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()  # loads WEB3_PROVIDER_URL

RPC_URL = os.getenv("WEB3_PROVIDER_URL")

async def run(input):
    contract_address = input["contractAddress"]
    abi_file = input["abiFile"]
    method = input["method"]
    args = input.get("args", [])

    try:
        with open(abi_file, "r") as f:
            abi_json = json.load(f)

            if isinstance(abi_json, dict) and "abi" in abi_json:
                abi_json = abi_json["abi"]
    except Exception as e:
        return {"status": "error", "error": f"Failed to load ABI: {str(e)}"}
    

    if not RPC_URL:
        return {"status": "error", "error": "WEB3_PROVIDER_URL not set"}

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        return {"status": "error", "error": "Could not connect to RPC"}

   
    try:
        contract = w3.eth.contract(address=contract_address, abi=abi_json)
    except Exception as e:
        return {"status": "error", "error": f"Failed to create contract: {str(e)}"}

    try:
        fn = getattr(contract.functions, method)(*args)
        raw_result = fn.call()
        return {"status": "ok", "result": raw_result}
    except Exception as e:
        return {"status": "error", "error": f"Contract call failed: {str(e)}"}
    
    
contract_read_tool = {
        "name": "contract_read_from_file",
        "description": "Reads a view function from a smart contract using ABI loaded from a JSON file",
        "schema": {
            "type": "object",
            "required": ["contractAddress", "abiFile", "method"],
            "properties": {
                "contractAddress": {
                    "type": "string",  
        },
                "abiFile": {
                    "type": "string",  
                },
                "method": {
                    "type": "string",  
                },
                "args": {
                    "type": "array",  
                },
            },
        },
        "run": run
    }

def get_tool():
    return contract_read_tool

