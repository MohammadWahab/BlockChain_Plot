# ethereum_contract_connector.py
from web3 import Web3


class EthereumContractConnector:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
        self.contract_address = '0xE27C6864E65EB02Cb17f2A7e7EE1B37c95A2B325'  # Replace with your actual contract address
        self.abi = [
            {
                "inputs": [
                    {"internalType": "string", "name": "ownerEmail", "type": "string"},
                    {"internalType": "string", "name": "ownerNid", "type": "string"},
                    {"internalType": "address", "name": "ownerMetamaskId", "type": "address"},
                ],
                "name": "addOwner",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "string", "name": "plotName", "type": "string"},
                    {"internalType": "uint256", "name": "plotPrice", "type": "uint256"},
                    {"internalType": "address", "name": "ownerMetamaskId", "type": "address"},
                ],
                "name": "addPlot",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "string", "name": "plotName", "type": "string"},
                    {"internalType": "address", "name": "existingOwnerMetamaskId", "type": "address"},
                    {"internalType": "address", "name": "newOwnerMetamaskId", "type": "address"},
                ],
                "name": "purchasePlot",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "address", "name": "ownerMetamaskId", "type": "address"}],
                "name": "getOwner",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [{"internalType": "string", "name": "plotName", "type": "string"}],
                "name": "getPlot",
                "outputs": [
                    {"internalType": "string", "name": "", "type": "string"},
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint256", "name": "", "type": "uint256"},
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                ],
                "name": "owners",
                "outputs": [
                    {"internalType": "string", "name": "email", "type": "string"},
                    {"internalType": "string", "name": "nidNumber", "type": "string"},
                    {"internalType": "bool", "name": "isRegistered", "type": "bool"},
                ],
                "stateMutability": "view",
                "type": "function",
            },
            {
                "inputs": [
                    {"internalType": "string", "name": "", "type": "string"},
                ],
                "name": "plots",
                "outputs": [
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "address", "name": "ownerMetamaskId", "type": "address"},
                    {"internalType": "uint256", "name": "price", "type": "uint256"},
                    {"internalType": "bool", "name": "isOwned", "type": "bool"},
                ],
                "stateMutability": "view",
                "type": "function",
            },
        ]

        #Default account information
        self.default_account = '0x9d116Afc638A0d24c43E79b3d3580accE7c5b31c'
        self.private_key = '0xc3ffc67eb042a6457f36b2c2beed8621ce679173f9961366fbf3d60177388839'


        # Load the contract
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)




    def add_owner(self, email, nid_number, meta_mask_id):
       

        # Call the smart contract function
        transaction_data = self.contract.functions.addOwner(email, nid_number, meta_mask_id).build_transaction({
        'gas': 2000000,  # adjust gas limit accordingly
        'gasPrice': self.web3.to_wei('20', 'gwei'),  # adjust gas price accordingly
        'nonce': self.web3.eth.get_transaction_count('0x9d116Afc638A0d24c43E79b3d3580accE7c5b31c'),  # replace with your actual address
    })



        # Step 2: Sign the transaction data with the private key
        signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, self.private_key)

        # Step 3: Send the signed transaction to the Ethereum network
        transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        transaction_receipt = self.web3.eth.wait_for_transaction_receipt(transaction_hash)
       
        print(f"Owner added successfully. Transaction Hash: {transaction_hash}")




    
    def transfer_plot_ownership(self, plot_name, existing_owner_metamask_id, new_owner_metamask_id):

        # Call the smart contract function
        transaction_data = self.contract.functions.purchasePlot(plot_name, existing_owner_metamask_id, new_owner_metamask_id).build_transaction({
            'from': self.default_account,
            'gas': 2000000,  # Adjust gas value based on your contract requirements
            'gasPrice': self.web3.to_wei('20', 'gwei'),  # Adjust gas price based on your requirements
            'nonce': self.web3.eth.get_transaction_count(self.default_account),
        })


        # Step 2: Sign the transaction data with the private key
        signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, self.private_key)

        # Step 3: Send the signed transaction to the Ethereum network
        transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        transaction_receipt = self.web3.eth.wait_for_transaction_receipt(transaction_hash)

        # Transaction successful, you can add additional logic if needed
        print(f"Plot ownership transferred successfully. Transaction Hash: {transaction_hash}")
        



    
    def add_plot(self, plot_name, plot_price, owner_metamask_id):
        # Assuming 'addPlot' function in your smart contract takes three parameters
        transaction_data = self.contract.functions.addPlot(
            plot_name, plot_price, owner_metamask_id
        ).build_transaction({
            'from': self.default_account,
            'gas': 2000000,  # Adjust gas value based on your contract requirements
            'gasPrice': self.web3.to_wei('20', 'gwei'),  # Adjust gas price based on your requirements
            'nonce': self.web3.eth.get_transaction_count(self.default_account),
        })



        # Step 2: Sign the transaction data with the private key
        signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, self.private_key)

        # Step 3: Send the signed transaction to the Ethereum network
        transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        transaction_receipt = self.web3.eth.wait_for_transaction_receipt(transaction_hash)

        print(f"plot added successfully. Transaction Hash: {transaction_hash}")
    
   