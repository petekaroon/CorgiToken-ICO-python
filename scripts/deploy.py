from brownie import accounts, CorgiTokenICO

def main():
  CorgiTokenICO.deploy(accounts[0], {'from': accounts[0]})
