'''
    Test program to try out the ccxt API. 
    Try to get price of a coin and maybe do some
    fake transactions.

    Author: Josh Anderson
    Created: 07/21/18

    TODOs/Ideas:
        - Make a moving average 
        - Plot return vs just holding
        - Multiple exchanges and coins
        - Modularize functions better

'''

# Imports

import ccxt
import matplotlib.pyplot as plt
import datetime
import time


class Account:

    def __init__(self, exchange = "kraken", ticker = "XLM/USD", cash = 1000,
            loss_percent = 0.99999, gain_percent = 1.00005):
        '''
            Constructor for our Account class. Initialize some variables
        '''
        if (exchange is "kraken"):
            self.exchange = ccxt.kraken()
        self.starting_cash = cash
        self.current_cash = cash
        self.loss_percent = loss_percent
        self.gain_percent = gain_percent
        self.ticker = ticker
        self.current_shares = 0 # shares

        # get current price
        self.current_price = self.get_price()

        # calculate sell for loss price
        sell_for_loss_price = self.current_price * self.loss_percent

        # calculate sell for gain price
        sell_for_gain_price = self.current_price * self.gain_percent
        self.portfolio_value = [] # our portfolio's value

        # calculate our buy target 
        self.buy_target = self.get_buy_target()
        return


    def buy_shares(self, quantity, price):
        # TODO would buy here
        print("Buying in at", current_price)
        current_shares = current_cash / current_price # ALL IN
        print("Bought", current_shares)
        current_cash = 0

        # calculate sell for loss price
        sell_for_loss_price = current_price * loss_percent

        # calculate sell for gain price
        sell_for_gain_price = current_price * gain_percent

        return


    def sell_shares(self, quantity, price):
        print("Selling (loss)", current_shares, "at", current_price)

        # TODO would sell here - let's assume we sell all shares
        current_cash = current_shares * current_price
        current_shares = 0

        # recalculate targets
        # want to buy back in when there's another dip
        buy_target = current_price * loss_percent
        print("New target = $" + str(buy_target))

        return


    def plot_returns(self, times, holding):
        if len(self.portfolio_value) > 1 and len(holding) > 1:
            plt.plot(times, self.portfolio_value)
            plt.plot(times, holding)
            axes = plt.gca()
            axes.set_ylim([-10, 10]) # TODO fix
            plt.title("MY ALGORITHM")
            plt.ylabel("Value")
            plt.legend(["Portfolio Value", "Holding Value"])
            plt.draw()
            plt.pause(5)
            plt.close()
        return
        

    def get_price(self):
        '''
            Return the latest bid price on an exchange for a pairing
        '''
        latest_info = self.exchange.fetch_ticker(self.ticker)
        return latest_info["bid"]


    def get_buy_target(self):
        '''
            Return the target we want to buy at 
        '''
        return (self.get_price() * self.loss_percent)


    def print_price(self):
        while(1):
            print (get_price(exchange, ticker))
            time.sleep(1)


if __name__ == "__main__":
    '''
        Entry point for our program
    '''

    darias_account = Account() # make a default account object

    # get current price
    current_price = darias_account.get_price()
    print(current_price)

    original_shares = darias_account.current_cash / current_price

    # calculate our buy in target
    buy_target = current_price * darias_account.loss_percent

    print ("Current price = $" + str(darias_account.current_price))
    print ("I will buy in at", buy_target)

    holding_value = [] # if we just bought and held - for comparison
    times = []

    last_price = 0

    # Magic loop
    while (True):
        current_price = darias_account.get_price()
        if (current_price == last_price):
            last_price = current_price
            darias_account.plot_returns(times, holding_value)
            continue

        print("Cash = $" + str(darias_account.current_cash))
        print("BTC Shares =", darias_account.current_shares)
        print("Current BTC Price = $" + str(current_price))

        if (not(darias_account.current_cash)): # means we are holding BTC
            if (current_price <= darias_account.sell_for_loss_price):
                darias_account.sell_shares()
            elif (current_price >= darias_account.sell_for_gain_price):
                darias_account.sell_shares()
            else:
                print("Holding at", current_price)
        else: # we are holding cash
            if (current_price <= buy_target): # price is low so buy
                darias_account.buy_shares()
            else: # recalculate target and hold
                buy_target = current_price * darias_account.loss_percent
                print("New target = $" + str(buy_target))

        current_cash_value = darias_account.current_cash
        if (not(current_cash_value)): # convert shares to current_cash
            current_cash_value = current_shares * current_price

        darias_account.portfolio_value.append(current_cash_value)
        holding_value.append(original_shares * current_price)
        times.append(datetime.datetime.now())

        darias_account.plot_returns(times, holding_value)
        last_price = current_price


