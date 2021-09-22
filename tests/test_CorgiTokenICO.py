import pytest
import brownie

# corgiToken Tests
@pytest.fixture
def corgiToken(CorgiToken, accounts):
  founder = accounts[0]
  return founder.deploy(CorgiToken)

def test_token_deployment(corgiToken, accounts):
  founder = accounts[0]
  founderBalance = corgiToken.balanceOf(founder)
  assert founderBalance == 50000

  tokenTotalSupply = corgiToken.totalSupply()
  assert tokenTotalSupply == founderBalance


# corgiTokenICO Tests
@pytest.fixture(scope="module", autouse=True)
def corgiTokenICO(CorgiTokenICO, accounts):
  founder = accounts[0]
  admin = accounts[1]
  corgiTokenICOContract = admin.deploy(CorgiTokenICO, founder)
  yield corgiTokenICOContract

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
  pass

def test_ICO_deployment(corgiTokenICO, accounts):
  founder = accounts[0]
  admin = accounts[1]
  
  depositAddress = corgiTokenICO.depositAddr()
  assert depositAddress == founder

  adminAddress = corgiTokenICO.admin()
  assert adminAddress == admin

def test_changeDepositAddress(corgiTokenICO, accounts):
  admin = accounts[1]
  corgiTokenICO.changeDepositAddress(accounts[2], {'from': admin})
  newDepositAddress = corgiTokenICO.depositAddr()
  assert newDepositAddress == accounts[2]

def test_changeDepositAddressByNonAdmin(corgiTokenICO, accounts):
  nonAdmin = accounts[3]
  with brownie.reverts('You are not the admin'):
    corgiTokenICO.changeDepositAddress(accounts[2], {'from': nonAdmin})

def test_invest(corgiTokenICO, accounts):
  founder = accounts[0]
  user1 = accounts[4]
  depositAccETHBalance = founder.balance()

  # User1 invest 2 ETH and receives 200 CORGI
  user1.transfer(corgiTokenICO, '2 ether')

  user1TokenBalance = corgiTokenICO.balanceOf(user1)
  assert user1TokenBalance == 200

  newDepositAccETHBalance = founder.balance()
  assert newDepositAccETHBalance == depositAccETHBalance + '2 ether'

def test_investExceedMaxInvestment(corgiTokenICO, accounts):
  user1 = accounts[4]
  with brownie.reverts('Please invest a valid amount.'):
    # User1 tries to invest 25 ETH
    user1.transfer(corgiTokenICO, '25 ether')

def test_transferToken(corgiTokenICO, accounts):
  user1 = accounts[4]
  user2 = accounts[5]

  # User1 invests 2 ETH and receive 200 CORGI
  user1.transfer(corgiTokenICO, '2 ether')

  # User1 transfers 50 CORGI to User2
  corgiTokenICO.transfer(user2, 50, {'from': user1})

  user1TokenBalance = corgiTokenICO.balanceOf(user1)
  user2TokenBalance = corgiTokenICO.balanceOf(user2)

  assert user1TokenBalance == 150
  assert user2TokenBalance == 50