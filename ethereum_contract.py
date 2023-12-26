# ethereum_contract_connector.py
from web3 import Web3

class EthereumContractConnector:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))  # Use the correct URL for your Ethereum node
        self.contract_address = '0xYourContractAddress'  # Replace with your actual contract address
        self.abi = [...]  # Replace with your contract ABI

        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def add_owner(self, email, nid_number, meta_mask_id):
        # Convert string inputs to bytes if needed
        email_bytes = Web3.toBytes(text=email)
        nid_number_bytes = Web3.toBytes(text=nid_number)
        meta_mask_id_bytes = Web3.toBytes(text=meta_mask_id)

        # Call the smart contract function
        transaction_hash = self.contract.functions.addOwner(email_bytes, nid_number_bytes, meta_mask_id_bytes).transact()

        # Wait for the transaction to be mined
        transaction_receipt = self.web3.eth.waitForTransactionReceipt(transaction_hash)

        # Check if the transaction was successful
        if transaction_receipt['status'] != 1:
            raise Exception(f"Transaction failed: {transaction_receipt}")

        # Transaction successful, you can add additional logic if needed
        print(f"Owner added successfully. Transaction Hash: {transaction_hash}")
    
    def transfer_plot_ownership(self, plot_name, existing_owner_email, new_owner_email):
        # Convert string inputs to bytes if needed
        plot_name_bytes = Web3.toBytes(text=plot_name)
        existing_owner_email_bytes = Web3.toBytes(text=existing_owner_email)
        new_owner_email_bytes = Web3.toBytes(text=new_owner_email)

        # Call the smart contract function
        transaction_hash = self.contract.functions.purchasePlot(plot_name_bytes, existing_owner_email_bytes, new_owner_email_bytes).transact()

        # Wait for the transaction to be mined
        transaction_receipt = self.web3.eth.waitForTransactionReceipt(transaction_hash)

        # Check if the transaction was successful
        if transaction_receipt['status'] != 1:
            raise Exception(f"Transaction failed: {transaction_receipt}")

        # Transaction successful, you can add additional logic if needed
        print(f"Plot ownership transferred successfully. Transaction Hash: {transaction_hash}")
    
    # def add_plot(self, plot_name, plot_price, owner_metamask_id):
    #     # Assuming 'addPlot' function in your smart contract takes three parameters
    #     transaction_data = self.contract.functions.addPlot(plot_name, plot_price, owner_metamask_id).buildTransaction({
    #         'from': self.w3.eth.accounts[0],  # Replace with your Ethereum account
    #         'gas': 2000000,  # Adjust the gas limit as needed
    #         'gasPrice': self.w3.toWei('50', 'gwei')  # Adjust the gas price as needed
    #     })

    #     private_key = "0xYourPrivateKey"  # Replace with your private key
    #     signed_transaction = self.w3.eth.account.signTransaction(transaction_data, private_key)
    #     transaction_hash = self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    #     # Wait for the transaction to be mined
    #     receipt = self.w3.eth.waitForTransactionReceipt(transaction_hash)

    #     return receipt
    
    def add_plot(self, plot_name, plot_price, owner_metamask_id):
        # Assuming 'addPlot' function in your smart contract takes three parameters
        transaction_hash = self.contract.functions.addPlot(
            plot_name, plot_price, owner_metamask_id
        ).transact()

        # Wait for the transaction to be mined
        receipt = self.w3.eth.waitForTransactionReceipt(transaction_hash)

        # Check if the transaction was successful
        if receipt['status'] != 1:
            raise Exception(f"Transaction failed: {receipt}")

        return receipt

