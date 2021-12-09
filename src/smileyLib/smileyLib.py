import subprocess
import atexit
import psutil
import warnings
import json
import requests
import base64
from datetime import datetime

class smiley:
    """
    The module *smiley* is a python wrapper for the smileycoin-cli command line interface.
    It is designed to be easy to use and to provide a high level of abstraction.

    There are several options in regards to how the server is handled.
    ```
    options = {
        shutDownAfterRun: boolean,  # If true, the server will be shut down after the python script has finished running
        startServer: boolean,       # If true, the server will be started before the python script runs
        rpcUser: string,            # The rpc user to use when connecting to the server
        rpcPassword: string,        # The rpc password to use when connecting to the server
        rpcPort: string             # The rpc port to use when connecting to the server
    }
    ```
    """

    def startServer(self):
        if not self.serverStarted and self.shouldStartServer:
            process = [x for x in psutil.process_iter() if x.name()
                       == 'smileycoind']
            if len(process) > 0:
                print('smileyCoin server already running...')
                self.serverHandled = False
            else:
                print('smileyCoin server not running, starting now...')
                self.smileyCoinServer = subprocess.Popen(['smileycoind'])
                self.serverHandled = True
            self.serverStarted = True

    def stopServer(self):
        if self.serverStarted and self.serverHandled:
            self.smileyCoinServer.terminate()
            self.serverStarted = False
            self.serverHandled = False

    def __communicateWithServer(self, method, data=[]):
        data = json.dumps({
            "jsonrpc": "1.0",
            "id": method + "python_client",
            "method": method,
            "params": data
        })
        response = requests.get(
            f'http://localhost:{self.rpcPort}',
            headers={'content-type': 'text/plain'},
            auth=(self.rpcUser, self.rpcPassword),
            data=data.encode()
        )
        return response.json()['result']

    def addchapter(self, servicename, chapternumber, chapteraddress):
        """
        Add new chapter to book chapter service.  
        ___
        ## Args:

        * **servicename**: The book chapter service name associated with the chapter address

        * **chapternumber**: The smileycoin number associated with the book chapter service

        * **chapteraddress**: The smileycoin address associated with the book chapter service

        ## Returns: 

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: Not tested yet...")
        return self.__communicateWithServer('addchapter', [servicename, chapternumber, chapteraddress])

    def addcoupon(self, servicename, couponlocation, couponname, coupondatetime, couponprice, couponaddress):
        """
        Create a new coupon on the blockchain.   
        ___
        ## Args:

        * **servicename**: The service name associated with the new coupon

        * **couponlocation**: The smileycoin coupon sales service address associated with the new coupon

        * **couponname**: The coupon name

        * **coupondatetime**: The coupon date and time

        * **couponprice**: The coupon price

        * **couponaddress**: The smileycoin address associated with the new coupon

        ## Returns: 

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: Not tested yet...")
        coupondatetime = coupondatetime.strftime("%d/%m/%Y%H:%M")
        return self.__communicateWithServer('addcoupon', [servicename, couponlocation, couponname, coupondatetime, couponprice, couponaddress])

    def adddex(self, servicename, dexaddress, dexdescription):
        """
        Add new DEX address to DEX service.
        ___
        ## Args:

        * **servicename**: The DEX service name associated with the new DEX address

        * **dexaddress**: The smileycoin address associated with the DEX service

        * **dexdescription**: The DEX description

        ## Returns: 

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: Not tested yet...")
        return self.__communicateWithServer('adddex', [servicename, dexaddress, dexdescription])

    def addmultisigaddress(self, nrequired, keys, account=None):
        """
        Add a nrequired-to-sign multisignature address to the wallet.
        Each key is a Smileycoin address or hex-encoded public key.
        If 'account' is specified, assign address to that account.
        ___
        ## Args:

        * **nrequired**: The number of required signatures to spend from the multisig address

        * **keys**: a list of smileycoin addresses or hex-encoded public keys

        * **account**: (optional) the account name to assign the new address to

        ## Returns:

        * A smileycoin address that is associated with the keys
        """
        warnings.warn("Warning: Not tested yet...")
        data = [nrequired, keys, account] if account else [nrequired, keys]
        return self.__communicateWithServer('addmultisigaddress', data)

    def addnode(self, node, command):
        """
        Attempts to add or remove a node from the addnode list.
        Or try a connection to a node once.
        ___
        ## Args:

        * **node**: The node to add or remove (see getpeerinfo for nodes)

        * **command**: One of *add*, *remove*, *onetry*
        """
        warnings.warn("Warning: Not tested yet...")
        return self.__communicateWithServer('addnode', [node, command])

    def addubi(self, servicename, ubiaddress):
        """
        Add new UBI recipient to UBI service.
        ___
        ## Args:

        * **servicename**: The UBI service name associated with the new UBI recipient address

        * **ubiaddress**: The smileycoin UBI recipient address associated with the UBI service

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: Not tested yet...")
        return self.__communicateWithServer('addubi', [servicename, ubiaddress])

    def backupwallet(self, destination):
        """
        Safely copies wallet.dat to destination, which can be a directory or a path with filename.
        ___
        ## Args:
        * **destination**: The destination directory or file
        """
        warnings.warn("Warning: backupwallet has not been tested yet...")
        return self.__communicateWithServer('backupwallet', [destination])

    def buycoupon(self, couponaddress):
        """
        Buy a coupon on the blockchain.
        ___
        ## Args:

        * **couponaddress**: The smileycoin coupon address associated with the coupon

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: buycoupon has not been tested yet...")
        return self.__communicateWithServer('buycoupon', [couponaddress])

    def consolidate(self, smileycoinaddress, N):
        """
        Consolidate UTXOs (Unspent Transaction Outputs) into a single transaction, up to 200.
        ___
        ## Args:

        * **smileycoinaddress**: One of your own smileycoin addresses that contains UTXOs

        * **N**: The number of UTXOs to consolidate

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: consolidate has not been tested yet...")
        return self.__communicateWithServer('consolidate', [smileycoinaddress, N])

    def createmultisig(self, nrequired, keys):
        """
        Create a multi-signature address with n signature of m keys required.
        ___
        ## Args:

        * **nrequired**: The number of required signatures to spend from the multisig address

        * **keys**: a list of smileycoin addresses or hex-encoded public keys

        ## Returns:

        * A json object with the address and redeemScript
        """
        warnings.warn("Warning: createmultisig has not been tested yet...")
        return self.__communicateWithServer('createmultisig', [nrequired, keys])

    def createrawtransaction(self, transactions, addresses, data=None):
        """
        Create a transaction spending the given inputs and sending to the given addresses.
        Returns hex-encoded raw transaction.
        Note that the transaction's inputs are not signed, and
        it is not stored in the wallet or transmitted to the network.
        ___
        ## Args:

        * **transactions**: A list of transaction objects of the form:

        ```
        [
            {
                "txid": "id",
                "vout": n,
                "sequence": n, #(optional)
            }, 
            ...
        ]
        ```

        * **addresses**: A dict of addresses and amounts to send to, of the form:

        ```
            {
                "address": amount,
                ...
            }
        ```

        * **data**: (optional) A string of data to include in the transaction

        ## Returns:

        * A hex-encoded raw transaction
        """
        warnings.warn(
            "Warning: createrawtransaction has not been tested yet...")
        if data:
            addresses.append({'data': base64.b16encode(data)})
        return self.__communicateWithServer('createrawtransaction', [transactions, addresses])

    def createservice(self, servicename, serviceaddress, servicetype):
        """
        Create a new service on the blockchain. The price of creating a service is 10 SMLY.
        ___
        ## Args:

        * **servicename**: The name of the service

        * **serviceaddress**: The smileycoin address associated with the service

        * **servicetype**: The type of service

        ### Service types:

        1. Coupon Sales
        1. UBI
        1. Book Chapter
        1. Traceability
        1. Nonprofit Organization
        1. DEX
        1. Survey
        1. Organization group

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: createservice has not been tested yet...")
        return self.__communicateWithServer('createservice', [servicename, serviceaddress, servicetype])

    def decoderawtransaction(self, hexstring):
        """
        Return a dict representing the serialized, hex-encoded transaction.
        ___
        ## Args:

        * **hexstring**: The hex-encoded transaction

        ## Returns:

        * A dict containing the transaction data
        """
        warnings.warn(
            "Warning: decoderawtransaction has not been tested yet...")
        return self.__communicateWithServer('decoderawtransaction', [hexstring])

    def decodescript(self, hexstring):
        """
        Decode a hex-encoded script.
        ___
        ## Args:

        * **hexstring**: The hex-encoded script

        ## Returns:

        * A dict containing the script data
        """
        warnings.warn("Warning: decodescript has not been tested yet...")
        return self.__communicateWithServer('decodescript', [hexstring])

    def decryptmessage(self, smileycoinaddress, encryptedmessage):
        """
        Decrypt a message encrypted with the public key of the given smileycoin address.
        ___
        ## Args:

        * **smileycoinaddress**: The smileycoin address whose public key will be used to decrypt the message

        * **encryptedmessage**: The encrypted message

        ## Returns:

        * The decrypted message encoded in base 64
        """
        warnings.warn("Warning: decryptmessage has not been tested yet...")
        return self.__communicateWithServer('decryptmessage', [smileycoinaddress, encryptedmessage])

    def deletecoupon(self, serviceaddress, couponaddress):
        """
        Delete the coupon with the service address, coupon address pair.
        ___
        ## Args:

        * **serviceaddress**: The smileycoin service address associated with the service

        * **couponaddress**: The smileycoin coupon address associated with the coupon

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: deletecoupon has not been tested yet...")
        return self.__communicateWithServer('deletecoupon', [serviceaddress, couponaddress])

    def deleteorg(self, serviceaddress, orgaddress):
        """
        Delete the organization with the service address, organization address pair.
        ___
        ## Args:

        * **serviceaddress**: The smileycoin service address associated with the service

        * **orgaddress**: The smileycoin organization address associated with the organization

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: deleteorg has not been tested yet...")
        return self.__communicateWithServer('deleteorg', [serviceaddress, orgaddress])

    def deleteservice(self, serviceaddress):
        """
        Delete the service with the given service address.
        ___
        ## Args:

        * **serviceaddress**: The smileycoin service address associated with the service

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: deleteservice has not been tested yet...")
        return self.__communicateWithServer('deleteservice', [serviceaddress])

    def deleteubi(self, serviceaddress, ubiaddress):
        """
        Delete the UBI with the service address, UBI address pair.
        ___
        ## Args:

        * **serviceaddress**: The smileycoin service address associated with the service

        * **ubiaddress**: The smileycoin UBI address associated with the UBI

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: deleteubi has not been tested yet...")
        return self.__communicateWithServer('deleteubi', [serviceaddress, ubiaddress])

    def dumpprivkey(self, smileycoinaddress):
        """
        Reveals the private key corresponding to the given address.
        Then the *importprivkey* can be used with it.
        ___
        ## Args:

        * **smileycoinaddress**: The smileycoin address for which the private key will be revealed

        ## Returns:

        * The private key
        """
        warnings.warn("Warning: dumpprivkey has not been tested yet...")
        return self.__communicateWithServer('dumpprivkey', [smileycoinaddress])

    def dumpwallet(self, filename):
        """
        Dumps all wallet keys in a human-readable format.
        ___
        ## Args:

        * **filename**: The filename to which the keys will be written
        """
        warnings.warn("Warning: dumpwallet has not been tested yet...")
        return self.__communicateWithServer('dumpwallet', [filename])

    def encryptmessage(self, smileycoinaddress, message):
        """
        Encrypt a message with the public key of the given smileycoin address.
        ___
        ## Args:

        * **smileycoinaddress**: The smileycoin address whose public key will be used to encrypt the message

        * **message**: The message to encrypt

        ## Returns:

        * The encrypted message encoded in base 64
        """
        warnings.warn("Warning: encryptmessage has not been tested yet...")
        return self.__communicateWithServer('encryptmessage', [smileycoinaddress, message])

    def encryptwallet(self, passphrase):
        """
        Encrypts the wallet with 'passphrase'. This is for first time encryption.
        After this, any calls that interact with private keys such as sending or signing 
        will require the passphrase to be set prior the making these calls.
        Use the walletpassphrase call for this, and then walletlock call.
        If the wallet is already encrypted, use the walletpassphrasechange call.
        Note that this will shutdown the server.
        ___
        ## Args:

        * **passphrase**: The passphrase with which to encrypt the wallet. It must be at least 1 character, but should be long.

        ## Returns:

        * The transaction id of the transaction that was created
        """
        warnings.warn("Warning: encryptwallet has not been tested yet...")
        return self.__communicateWithServer('encryptwallet', [passphrase])

    def getaccount(self, smileycoinaddress):
        """
        Returns the account associated with the given address.
        ___
        ## Args:

        * **smileycoinaddress**: The smileycoin address for account lookup.

        ## Returns:

        * The account address
        """
        warnings.warn("Warning: getaccount has not been tested yet...")
        return self.__communicateWithServer('getaccount', [smileycoinaddress])

    def getaccountaddress(self, account):
        """
        Returns the current smileycoin address for receiving payments to this account.
        ___
        ## Args:

        * **account**: The account name for the address. It can also be empty string to represent the default account. The account does not need to exist, it will be created and new address created if there is no account by the given name.

        ## Returns:

        * The account smileycoin address
        """
        warnings.warn("Warning: getaccountaddress has not been tested yet...")
        return self.__communicateWithServer('getaccountaddress', [account])

    def getaddednodeinfo(self, dns, node):
        """
        Returns information about the given added node, or all added nodes
        (note that onetry addnodes are not listed here)
        If dns is false, only a list of added nodes will be provided,
        otherwise connected information will also be available.
        ___
        ## Args:

        * **dns**: If false, only a list of added nodes will be provided, otherwise connected information will also be available.

        * **node**: If provided, return information about this specific node, otherwise all nodes are returned.

        ## Returns:

        * List of added nodes (dns=false) or full node information (dns=true)
        """
        warnings.warn("Warning: getaddednodeinfo has not been tested yet...")
        return self.__communicateWithServer('getaddednodeinfo', [dns, node])

    def getaddressesbyaccount(self, account):
        """
        Returns the list of addresses for the given account.
        ___
        ## Args:

        * **account**: The account name for the address.

        ## Returns:

        * The list of addresses associated with the account
        """
        warnings.warn(
            "Warning: getaddressesbyaccount has not been tested yet...")
        return self.__communicateWithServer('getaddressesbyaccount', [account])

    def getaddressbalance(self):
        """
        ! WARNING: This function is not implemented at all.
        """
        warnings.warn(
            "Warning: getaddressbalance has not been tested yet, and is not documented in the smileycoin client...")

    def getallcouponlists(self):
        """
        Returns all listed coupons under each specified service address.
        ___
        ## Returns:

        * The list of coupons.
        """
        warnings.warn("Warning: getallcouponlists has not been tested yet...")
        return self.__communicateWithServer('getallcouponlists')

    def getallorglists(self):
        """
        Returns all listed organization groups.
        ___
        ## Returns:

        * The list of organization groups.
        """
        warnings.warn("Warning: getallorglists has not been tested yet...")
        return self.__communicateWithServer('getallorglists')

    def getbalance(self, account = "", minconf = 1):
        """
        If account is not specified, returns the server's total available balance.
        If account is specified, returns the balance in the account.
        Note that the account "" is not the same as leaving the parameter out.
        The server total may be different to the balance in the default "" account.
        ___
        ## Args:

        * **account**: The selected account, or "*" for entire wallet. It may be the default account using "".

        * **minconf**: The minimum number of confirmations before payments are included.

        ## Returns:

        * The total amount in smileycoin received for this account.        
        """
        warnings.warn("Warning: getbalance has not been tested yet...")
        return self.__communicateWithServer('getbalance', [account, minconf])

    def getbestblockhash(self):
        """
        Returns the hash of the best (tip) block in the longest block chain.
        ___
        ## Returns:

        * The hash of the best (tip) block in the longest block chain.
        """
        warnings.warn("Warning: getbestblockhash has not been tested yet...")
        return self.__communicateWithServer('getbestblockhash')

    def getblock(self, hash, verbose=True):
        """
        Returns information about the block with the given hash.
        ___
        ## Args:

        * **hash**: The block hash to retrieve.
        
        * **verbose**: If false, returns a string that is serialized, hex-encoded data for block 'hash'.

        ## Returns:

        * If verbose is false, returns a string that is serialized, hex-encoded data for block 'hash'. If verbose is true, returns an Object with information about block <hash>.
        """
        warnings.warn("Warning: getblock has not been tested yet...")
        return self.__communicateWithServer('getblock', [hash, verbose])

    def getblockchaininfo(self):
        """
        Returns an object containing various state info regarding block chain processing.
        ___
        ## Returns:

        * Object containing various state info regarding block chain processing.
        """
        warnings.warn("Warning: getblockchaininfo has not been tested yet...")
        return self.__communicateWithServer('getblockchaininfo')

    def getblockcount(self):
        """
        Returns the number of blocks in the longest block chain.
        ___
        ## Returns:

        * The number of blocks in the longest block chain.
        """
        warnings.warn("Warning: getblockcount has not been tested yet...")
        return self.__communicateWithServer('getblockcount')

    def getblockhash(self, index):
        """
        Returns the hash of the block in the best-block-chain at height index.
        ___
        ## Args:

        * **index**: The block height index.

        ## Returns:

        * The hash of the block in the best-block-chain at height index.
        """
        warnings.warn("Warning: getblockhash has not been tested yet...")
        return self.__communicateWithServer('getblockhash', [index])

    def getblocktemplate(self, jsonrequest):
        """
        If the request parameters include a 'mode' key, that is used to explicitly select between the default 'template' request or a 'proposal'.
        It returns data needed to construct a block to work on.
        See https://en.bitcoin.it/wiki/BIP_0022 for full specification.
        ___
        ## Args:

        * **jsonrequest**: (optional) A json object with parameters to getblocktemplate.
        ```
        {
            "mode": "template"
            "capabilities": [
                "support"       // longpoll, coinbasetxn, coinbasevalue, proposal, serverlist, workid
            ]
        }
        ```

        ## Returns:

        An object with information about the given block template.
        """
        warnings.warn("Warning: getblocktemplate has not been tested yet...")
        return self.__communicateWithServer('getblocktemplate', [jsonrequest])

    def getbooklist(self, address):
        """
        Returns all book chapters that belong to the specified book service address.
        ___
        ## Args:

        * **address**: The book service address.    

        ## Returns:

        * The list of book chapters.
        """
        warnings.warn("Warning: getbooklist has not been tested yet...")
        return self.__communicateWithServer('getbooklist', [address])

    def getconnectioncount(self):
        """
        Returns the number of connections to other nodes.
        ___
        ## Returns:

        * The connection count.
        """
        warnings.warn("Warning: getconnectioncount has not been tested yet...")
        return self.__communicateWithServer('getconnectioncount')

    def getcouponlist(self, address):
        """
        Returns all coupons that belong to the specified coupon service address.
        ___
        ## Args:

        * **address**: The coupon service address.

        ## Returns:

        * The list of coupons.
        """
        warnings.warn("Warning: getcouponlist has not been tested yet...")
        return self.__communicateWithServer('getcouponlist', [address])

    def getdexlist(self, address):
        """
        Returns all DEX addresses that belong to the specified DEX service address.
        ___
        ## Args:

        * **address**: The DEX service address.

        ## Returns:

        * The list of DEX addresses.
        """
        warnings.warn("Warning: getdexlist has not been tested yet...")
        return self.__communicateWithServer('getdexlist', [address])

    def getdifficulty(self):
        """
        Returns the proof-of-work difficulty as a multiple of the minimum difficulty.
        ___
        ## Returns:

        * The proof-of-work difficulty as a multiple of the minimum difficulty.
        """
        warnings.warn("Warning: getdifficulty has not been tested yet...")
        return self.__communicateWithServer('getdifficulty')

    def getgenerate(self):
        """
        Return if the server is set to generate coins or not. The default is false.
        It is set in the smileycoin.conf file or with *setgenerate*.
        ___
        ## Returns:

        * True or False to indicate if the server is set to generate coins or not.
        """
        warnings.warn("Warning: getgenerate has not been tested yet...")
        return self.__communicateWithServer('getgenerate')

    def gethashespersec(self):
        """
        Returns a recent hashes per second performance measurement while generating.
        ___
        ## Returns:

        * The number of hashes per second.
        """
        warnings.warn("Warning: gethashespersec has not been tested yet...")
        return self.__communicateWithServer('gethashespersec')

    def getinfo(self):
        """
        Gets info about the smileycoin deamon.  
        ___
        Returns: 

        * A JSON object containing various information about the deamon.
        """
        return self.__communicateWithServer('getinfo')

    def getmessages(self):
        """
        Gets encrypted messages sent to the wallet and decrypts them.
        ___
        Returns:

        * The list of decrypted messages.
        """
        warnings.warn("Warning: getmessages has not been tested yet...")
        return self.__communicateWithServer('getmessages')

    def getmininginfo(self):
        """
        Returns an object containing mining-related information.
        ___
        ## Returns:

        * Object containing mining-related information.
        """
        warnings.warn("Warning: getmininginfo has not been tested yet...")
        return self.__communicateWithServer('getmininginfo')

    def getnettotals(self):
        """
        Returns information about network traffic, including bytes in, bytes out, and current time.
        ___
        ## Returns:

        * Object containing information about network traffic.
        """
        warnings.warn("Warning: getnettotals has not been tested yet...")
        return self.__communicateWithServer('getnettotals')

    def getnetworkinfo(self):
        """
        Returns an object containing various state info regarding P2P networking.
        ___
        ## Returns:

        * Object containing various state info regarding P2P networking.
        """
        warnings.warn("Warning: getnetworkinfo has not been tested yet...")
        return self.__communicateWithServer('getnetworkinfo')

    def getnewaddress(self, account=None, pattern=None):
        """
        Returns a new Smileycoin address for receiving payments.
        If 'account' is specified (recommended), it is added to the address book 
        so payments received with the address will be credited to 'account'.
        ___
        ## Args:

        * **account**: (optional) The account name for the address to be linked to.

        * **pattern**: (optional) A pattern that need to be found in the address generated.

        ## Returns:
        """
        warnings.warn("Warning: getnewaddress has not been tested yet...")
        data = [account, pattern] if pattern is None and account is None else [
            account] if account is not None else []
        return self.__communicateWithServer('getnewaddress', data)

    def getorglist(self, address):
        """
        Returns all organizations that belong to the specified organization service address.
        ___
        ## Args:

        * **address**: The organization service address.

        ## Returns:

        * The list of organizations.
        """
        warnings.warn("Warning: getorglist has not been tested yet...")
        return self.__communicateWithServer('getorglist', [address])

    def getpeerinfo(self):
        """
        Returns data about each connected network node as a list of objects.
        ___
        ## Returns:

        * The list of network nodes.
        """
        warnings.warn("Warning: getpeerinfo has not been tested yet...")
        return self.__communicateWithServer('getpeerinfo')

    def getrawchangeaddress(self):
        """
        Returns a new Smileycoin address, for receiving change.
        This is for use with raw transactions, NOT normal use.
        ___
        ## Returns:

        * The new Smileycoin address.
        """
        warnings.warn(
            "Warning: getrawchangeaddress has not been tested yet...")
        return self.__communicateWithServer('getrawchangeaddress')

    def getrawmempool(self, verbose=False):
        """
        Returns all transaction ids in memory pool as a list of transaction ids.
        ___
        ## Args:

        * **verbose**: (optional) If true, returns a list of objects, instead of just a list of transaction ids.

        ## Returns:

        * The list of transaction ids, or the list of objects if verbose is true.
        """
        warnings.warn("Warning: getrawmempool has not been tested yet...")
        return self.__communicateWithServer('getrawmempool', [verbose])

    def getrawtransaction(self, txid, verbose=False):
        """
        Return the raw transaction data.
        ___
        ## Args:

        * **txid**: The transaction id.

        * **verbose**: (optional) If true, returns an object, instead of a string.

        ## Returns:

        * The raw transaction data, or the object if verbose is true.
        """
        warnings.warn("Warning: getrawtransaction has not been tested yet...")
        return self.__communicateWithServer('getrawtransaction', [txid, 1 if verbose else 0])

    def getreceivedbyaccount(self, account = "", minconf=1):
        """
        Returns the total amount received by addresses with account in transactions with at least minconf confirmations.
        ___
        ## Args:

        * **account**: The account name. May be default if using "".

        * **minconf**: (optional) Minimum number of confirmations required for transactions.

        ## Returns:

        * The total amount received by the account.
        """
        warnings.warn(
            "Warning: getreceivedbyaccount has not been tested yet...")
        return self.__communicateWithServer('getreceivedbyaccount', [account, minconf])

    def getreceivedbyaddress(self, smileycoinaddress, minconf=1):
        """
        Returns the total amount received by smileycoinaddress in transactions with at least minconf confirmations.
        ___
        ## Args:

        * **smileycoinaddress**: The address.

        * **minconf**: (optional) Minimum number of confirmations required for transactions.

        ## Returns:

        * The total amount received by the address.
        """
        warnings.warn(
            "Warning: getreceivedbyaddress has not been tested yet...")
        return self.__communicateWithServer('getreceivedbyaddress', [smileycoinaddress, minconf])

    def getrichaddresses(self):
        """
        Returns all rich addresses, ordered by height.
        ___
        ## Returns:

        * The list of rich addresses.
        """
        warnings.warn("Warning: getrichaddresses has not been tested yet...")
        return self.__communicateWithServer('getrichaddresses')

    def getserviceaddresses(self):
        """
        Returns all verified addresses, ordered by the type of service they provide.
        ___
        ## Returns:

        * The list of verified addresses.
        """
        warnings.warn(
            "Warning: getserviceaddresses has not been tested yet...")
        return self.__communicateWithServer('getserviceaddresses')

    def gettransaction(self, txid):
        """
        Get detailed information about in-wallet transaction txid
        ___
        ## Args:

        * **txid**: The transaction id.

        ## Returns:

        * The transaction details.
        """
        warnings.warn("Warning: gettransaction has not been tested yet...")
        return self.__communicateWithServer('gettransaction', [txid])

    def gettxout(self, txid, n, includemempool=True):
        """
        Returns details about an unspent transaction output.
        ___
        ## Args:

        * **txid**: The transaction id.

        * **n**: The output number.

        * **includemempool**: (optional) If true, the mempool is queried for transactions.

        ## Returns:

        * The transaction output details.
        """
        warnings.warn("Warning: gettxout has not been tested yet...")
        return self.__communicateWithServer('gettxout', [txid, n, includemempool])

    def gettxoutsetinfo(self):
        """
        Returns statistics about the unspent transaction output set.
        Note this call may take some time.
        ___
        ## Returns:

        * The transaction output statistics.
        """
        warnings.warn("Warning: gettxoutsetinfo has not been tested yet...")
        return self.__communicateWithServer('gettxoutsetinfo')

    def getubilist(self):
        """
        Returns all UBI recipient addresses that belong to the specified UBI service address.
        ___
        ## Returns:

        * The list of UBI recipients.
        """
        warnings.warn("Warning: getubilist has not been tested yet...")
        return self.__communicateWithServer('getubilist')

    def getunconfirmedbalance(self):
        """
        Returns the server's total unconfirmed balance.
        ___
        ## Returns:

        * The unconfirmed balance.
        """
        warnings.warn(
            "Warning: getunconfirmedbalance has not been tested yet...")
        return self.__communicateWithServer('getunconfirmedbalance')

    def getwalletinfo(self):
        """
        Returns an object containing various wallet state info.
        ___
        ## Returns:

        * The wallet state info.
        """
        warnings.warn("Warning: getwalletinfo has not been tested yet...")
        return self.__communicateWithServer('getwalletinfo')

    def importprivkey(self, smileycoinprivkey, label=None, rescan=True):
        """
        Adds a private key (as returned by dumpprivkey) to your wallet.
        ___
        ## Args:

        * **smileycoinprivkey**: The private key.

        * **label**: (optional) Label to assign to the address.

        * **rescan**: (optional) If true, the wallet will rescan the blockchain looking for transactions.
        """
        warnings.warn("Warning: importprivkey has not been tested yet...")
        data = [smileycoinprivkey, label, rescan] if label else [
            smileycoinprivkey, rescan]
        return self.__communicateWithServer('importprivkey', data)

    def importwallet(self, filename):
        """
        Imports keys from a wallet dump file (see dumpwallet).
        ___
        ## Args:

        * **filename**: The wallet file name.
        """
        warnings.warn("Warning: importwallet has not been tested yet...")
        return self.__communicateWithServer('importwallet', [filename])

    def keypoolrefill(self, newsize=100):
        """
        Fills the keypool.
        ___
        ## Args:

        * **newsize**: (optional) The new keypool size.
        """
        warnings.warn("Warning: keypoolrefill has not been tested yet...")
        return self.__communicateWithServer('keypoolrefill', [newsize])

    def listaccounts(self, minconf=1):
        """
        Returns Object that has account names as keys, account balances as values.
        ___
        ## Args:

        * **minconf**: (optional) Minimum number of confirmations required for transactions.

        ## Returns:

        * The account balances.
        """
        warnings.warn("Warning: listaccounts has not been tested yet...")
        return self.__communicateWithServer('listaccounts', [minconf])

    def listaddressgroupings(self):
        """
        Lists groups of addresses which have had their common ownership
        made public by common use as inputs or as the resulting change
        in past transactions
        ___
        ## Returns:

        * The address groupings.
        """
        warnings.warn(
            "Warning: listaddressgroupings has not been tested yet...")
        return self.__communicateWithServer('listaddressgroupings')

    def listlockunspent(self):
        """
        Return list of temporarily unspendable outputs.
        See the lockunspent call to lock and unlock transactions for spending.
        ___
        ## Returns:

        * The list of temporarily unspendable outputs.
        """
        warnings.warn("Warning: listlockunspent has not been tested yet...")
        return self.__communicateWithServer('listlockunspent')

    def listreceivedbyaccount(self, minconf=1, includeempty=False):
        """
        List balances by account.
        ___
        ## Args:

        * **minconf**: (optional) Minimum number of confirmations required for transactions.

        * **includeempty**: (optional) Whether to include accounts that haven't received any payments.

        ## Returns:

        * The account balances.
        """
        warnings.warn(
            "Warning: listreceivedbyaccount has not been tested yet...")
        return self.__communicateWithServer('listreceivedbyaccount', [minconf, includeempty])

    def listreceivedbyaddress(self, minconf=1, includeempty=False):
        """
        List balances by receiving address.
        ___
        ## Args:

        * **minconf**: (optional) Minimum number of confirmations required for transactions.

        * **includeempty**: (optional) Whether to include addresses that haven't received any payments.

        ## Returns:

        * The address balances.
        """
        warnings.warn(
            "Warning: listreceivedbyaddress has not been tested yet...")
        return self.__communicateWithServer('listreceivedbyaddress', [minconf, includeempty])

    def listsinceblock(self, blockhash=None, target_confirmations=1):
        """
        Get all transactions in blocks since block [blockhash], or all transactions if omitted.
        ___
        ## Args:

        * **blockhash**: (optional) The block hash to list transactions since.

        * **target_confirmations**: (optional) The confirmations required.

        ## Returns:

        * The transactions.
        """
        warnings.warn("Warning: listsinceblock has not been tested yet...")
        data = [blockhash, target_confirmations] if blockhash is None else []
        return self.__communicateWithServer('listsinceblock', data)

    def listtransactions(self, account, count=10, skip=0):
        """
        Returns up to 'count' most recent transactions skipping the first 'from' transactions for account 'account'.
        ___
        ## Args:

        * **account**: The account to list transactions for.

        * **count**: (optional) The number of transactions to return.

        * **skip**: (optional) The number of transactions to skip.

        ## Returns:

        * The transactions.
        """
        warnings.warn("Warning: listtransactions has not been tested yet...")
        data = [account, count, skip] if account else []
        return self.__communicateWithServer('listtransactions', data)

    def listunspent(self, minconf=1, maxconf=9999999, addresses=[]):
        """
        Lists the unspent transactions for the base address.  
        ___
        ## Args:

        * **minconf**: minimum number of confirmations

        * **maxconf**: maximum number of confirmations

        * **addresses**: list of addresses to filter

        ## Returns: 

        * An array of json objects containing unspent transactions
        """
        return self.__communicateWithServer('listunspent', [minconf, maxconf, addresses])

    def lockunspent(self, unlock, transactions):
        """
        Updates list of temporarily unspendable outputs.
        Temporarily lock (unlock=false) or unlock (unlock=true) specified transaction outputs.
        A locked transaction output will not be chosen by automatic coin selection, when spending smileycoins.
        Locks are stored in memory only. Nodes start with zero locked outputs, and the locked output list
        is always cleared (by virtue of process exit) when a node stops or fails.
        Also see the listunspent call
        ___
        ## Args:

        * **unlock**: If true, unlock the transactions.

        * **transactions**: The transactions to lock or unlock. Each object contains the *txid* and *vout*

        ## Returns:

        * True if transaction was updated.
        """
        warnings.warn("Warning: lockunspent has not been tested yet...")
        return self.__communicateWithServer('lockunspent', [unlock, transactions])

    def move(self, fromaccount, toaccount, amount, minconf=1, comment=""):
        """
        Move a specified amount from one account in your wallet to another.
        ___
        ## Args:

        * **fromaccount**: The name of the account to move funds from.

        * **toaccount**: The name of the account to move funds to.

        * **amount**: The amount to move.

        * **minconf**: (optional) Minimum number of confirmations required for transactions.

        * **comment**: (optional) A comment. Stored in the wallet only.

        ## Returns:

        * True if successful.
        """
        warnings.warn("Warning: move has not been tested yet...")
        return self.__communicateWithServer('move', [fromaccount, toaccount, amount, minconf, comment])

    def replywithmessage(self, txid, value, message):
        """
        Send an encrypted message to the sender of a transaction,
        we find one public key used in its inputs, encrypt the message
        with that public key and send it to the corresponding address.
        ___
        ## Args:

        * **txid**: The transaction id.

        * **value**: The value of the transaction.

        * **message**: The message to send.

        ## Returns:

        * True if successful.
        """
        warnings.warn("Warning: replywithmessage has not been tested yet...")
        return self.__communicateWithServer('replywithmessage', [txid, value, message])

    def sendfrom(self, fromaccount, tosmileycoinaddress, amount, minconf=1, comment="", commentto=""):
        """
        Send an amount from an account to a smileycoin address.
        The amount is a real and is rounded to the nearest 0.00000001.
        ___
        ## Args:

        * **fromaccount**: The name of the account to send the funds from.

        * **tosmileycoinaddress**: The smileycoin address to send the funds to.

        * **amount**: The amount to send.

        * **minconf**: (optional) Minimum number of confirmations required for transactions.

        * **comment**: (optional) A comment. Stored in the wallet only.

        * **commentto**: (optional) A comment to store the name of the recipiant in the wallet only.

        ## Returns:

        * The transaction id.
        """
        warnings.warn("Warning: sendfrom has not been tested yet...")
        return self.__communicateWithServer('sendfrom', [fromaccount, tosmileycoinaddress, amount, minconf, comment, commentto])

    def sendmany(self, fromaccount, tosmileycoinaddresses, minconf=1, comment=""):
        """
        Send multiple times. Amounts are double-precision floating point numbers.
        ___
        ## Args:

        * **fromaccount**: The name of the account to send the funds from.

        * **tosmileycoinaddresses**: A dictionary of smileycoin addresses and amounts to send.

        * **minconf**: (optional) Minimum number of confirmations required for transactions.

        * **comment**: (optional) A comment. Stored in the wallet only.

        ## Returns:

        * The transaction id.
        """
        warnings.warn("Warning: sendmany has not been tested yet...")
        return self.__communicateWithServer('sendmany', [fromaccount, tosmileycoinaddresses, minconf, comment])

    def sendrawtransaction(self, hex, allowhighfees=False):
        """
        Submits raw transaction (serialized, hex-encoded) to local node and network.
        ___
        ## Args:

        * **hex**: The transaction hex.

        * **allowhighfees**: (optional) Allow high fees.

        ## Returns:

        * The transaction hash in hex.
        """
        warnings.warn("Warning: sendrawtransaction has not been tested yet...")
        return self.__communicateWithServer('sendrawtransaction', [hex, allowhighfees])

    def sendtoaddress(self, smileycoinaddress, amount, comment="", commentto=""):
        """
        Send an amount to a given address. The amount is a real and is rounded to the nearest 0.00000001.
        ___
        ## Args:

        * **smileycoinaddress**: The smileycoin address to send the funds to.

        * **amount**: The amount to send.

        * **comment**: (optional) A comment. Stored in the wallet only.

        * **commentto**: (optional) A comment to store the name of the recipiant in the wallet only.

        ## Returns:

        * The transaction id.
        """
        warnings.warn("Warning: sendtoaddress has not been tested yet...")
        return self.__communicateWithServer('sendtoaddress', [smileycoinaddress, amount, comment, commentto])

    def setaccount(self, smileycoinaddress, account):
        """
        Sets the account associated with the given address.
        ___
        ## Args:

        * **smileycoinaddress**: The smileycoin address to associate.

        * **account**: The account to associate with the address.
        """
        warnings.warn("Warning: setaccount has not been tested yet...")
        return self.__communicateWithServer('setaccount', [smileycoinaddress, account])

    def setgenerate(self, generate, genproclimit=-1):
        """
        Set 'generate' true or false to turn generation on or off.
        Generation is limited to 'genproclimit' processors, -1 is unlimited.
        See the getgenerate call for the current setting.
        ___
        ## Args:

        * **generate**: True to turn generation on.

        * **genproclimit**: (optional) Number of processors to limit generation to. Can be -1 for unlimited.
        """
        warnings.warn("Warning: setgenerate has not been tested yet...")
        return self.__communicateWithServer('setgenerate', [generate, genproclimit])

    def settxfee(self, amount):
        """
        Set the transaction fee per kB.
        ___
        ## Args:

        * **amount**: The transaction fee in smileycoin/1000 bytes, rounded to the nearest 0.00000001.

        ## Returns:

        * True if successful.
        """
        warnings.warn("Warning: settxfee has not been tested yet...")
        return self.__communicateWithServer('settxfee', [amount])

    def signmessage(self, smileycoinaddress, message):
        """
        Sign a message with the private key of an address.
        ___
        ## Args:

        * **smileycoinaddress**: The address to sign the message with.

        * **message**: The message to sign.

        ## Returns:

        * The signed message in base 64.
        """
        warnings.warn("Warning: signmessage has not been tested yet...")
        return self.__communicateWithServer('signmessage', [smileycoinaddress, message])

    def signrawtransaction(self, hexstring, prevtxs=None, privkeys=None, sighashtype='ALL'):
        """
        Sign inputs for raw transaction (serialized, hex-encoded).
        The second optional argument (may be null) is an array of previous transaction outputs that
        this transaction depends on but may not yet be in the block chain.
        The third optional argument (may be null) is an array of base58-encoded private
        keys that, if given, will be the only keys used to sign the transaction.
        ___
        ## Args:

        * **hexstring**: The transaction hex.

        * **prevtxs**: (optional) Previous transaction outputs that this transaction depends on but may not yet be in the block chain.

        * **privkeys**: (optional) The base58-encoded private keys that, if given, will be the only keys used to sign the transaction.

        * **sighashtype**: (optional) The signature hash type must be one of these:
            * **ALL**: Sign all inputs.
            * **NONE**: Do not sign any inputs.
            * **SINGLE**: Sign only the first input.
            * **ALL|ANYONECANPAY**: Sign all inputs unless there is a complete set of signatures with at least one input being signed by a key that is not one of the private keys.
            * **NONE|ANYONECANPAY**: Do not sign any inputs unless there is a complete set of signatures with at least one input being signed by one of the keys.
            * **SINGLE|ANYONECANPAY**: Sign only the first input unless there is a complete set of signatures with at least one input being signed by a key that is not one of the private keys.

        ## Returns:

        * The signed transaction in hex.
        """
        warnings.warn("Warning: signrawtransaction has not been tested yet...")
        data = [x for x in [hexstring, prevtxs, privkeys, sighashtype] if x]
        return self.__communicateWithServer('signrawtransaction', data)

    def submitblock(self, hexdata, jsonparameters=None):
        """
        Attempts to submit new block to network.
        The 'jsonparametersobject' parameter is currently ignored.
        See https://en.bitcoin.it/wiki/BIP_0022 for full specification.
        ___
        ## Args:

        * **hexdata**: The block hex.

        * **jsonparametersobject**: (optional) The json parameters object.
        """
        warnings.warn("Warning: submitblock has not been tested yet...")
        data = [hexdata, jsonparameters] if jsonparameters else [hexdata]
        return self.__communicateWithServer('submitblock', data)

    def validateaddress(self, smileycoinaddress):
        """
        Return information about the given smileycoin address.
        ___
        ## Args:

        * **smileycoinaddress**: The smileycoin address to validate.

        ## Returns:

        * A dict containing various information about the address.
        """
        warnings.warn("Warning: validateaddress has not been tested yet...")
        return self.__communicateWithServer('validateaddress', [smileycoinaddress])

    def verifychain(self, checklevel=3, nblocks=288):
        """
        Verifies blockchain database.
        ___
        ## Args:

        * **checklevel**: (optional) The check level.

        * **nblocks**: (optional) The number of blocks to check.

        ## Returns:

        * True if verified.
        """
        warnings.warn("Warning: verifychain has not been tested yet...")
        return self.__communicateWithServer('verifychain', [checklevel, nblocks])

    def verifymessage(self, smileycoinaddress, signature, message):
        """
        Verify a signed message.
        ___
        ## Args:

        * **smileycoinaddress**: The address the message was signed with.

        * **signature**: The signature.

        * **message**: The message.

        ## Returns:

        * True if the signature is valid.
        """
        warnings.warn("Warning: verifymessage has not been tested yet...")
        return self.__communicateWithServer('verifymessage', [smileycoinaddress, signature, message])

    def __init__(self, options):
        self.serverStarted = False
        self.serverHandled = None
        self.smileyCoinServer = None
        self.shutDownAfterRun = options['shutDownAfterRun']
        self.shouldStartServer = options['startServer']
        self.rpcUser = options['rpcUser']
        self.rpcPassword = options['rpcPassword']
        self.rpcPort = options['rpcPort']
        self.startServer()
        atexit.register(self.stopServer)


# smileyObject = smiley({
#     'shutDownAfterRun': False,
#     'startServer': True,
#     'rpcUser': "smileyoinrp",
#     'rpcPassword': "EAUbvD7ddK7eiS1izojpb9ZgMdqVsb36dL8KAjDKyzL",
#     'rpcPort': "14243"
# })
# print(json.dumps(smileyObject.addcoupon("test", "test",
#       "test", datetime.now(), 10, "test"), indent=4))
# smileyObject.stopServer()
