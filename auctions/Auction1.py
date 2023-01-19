from Card import *


class FirstAuction:
    @staticmethod
    def firstMoney(isFirstTime, highestMoney, players, communityCards,
                   moneyText):
        """
        This is void handling first auction, it gets input from user or allows
        to resign for that round if user writes p in input,
        It takes user's price and check for every computer player if it should
        resign or take the same bid or put more money.
        It decide it based on player's cards and risk level of the player.
        """

        highestPrice = highestMoney
        price = 0
        if isFirstTime:
            player = players[0]
            kwota = moneyText
            moneyText = ""
            try:
                if kwota == 'p':
                    player.currentAlive = 'OOTR'
                else:
                    price = int(kwota)
                    if price > player.currentMoney/2 or price < 1:
                        raise ValueError('Niepoprawna wartość kwoty licytacji')
                    highestPrice = price
                    player.currentMoney -= price
                    player.moneyOnTable += price
            except Exception:
                raise TypeError('Nieprawidłowo podana kwota licytacji')
        else:
            player = players[0]
            if player.moneyOnTable < highestPrice:
                kwota = moneyText
                if kwota == 'p':
                    player.currentAlive = 'OOTR'
                elif kwota == 'w':
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                else:
                    try:
                        price = int(kwota)
                        if price > player.currentMoney/2 or price < 1:
                            raise ValueError('Niepoprawna kwota licytacji')
                        if price < highestPrice - player.moneyOnTable:
                            player.currentAlive = 'OOTR'
                            price = 0
                            print('Za mala kwota aby wyrownac lub podbic')
                        highestPrice = price + player.moneyOnTable
                        player.currentMoney -= price
                        player.moneyOnTable += price
                    except Exception:
                        raise TypeError('Nieprawidłowo podana kwota licytacji')
        isFirstTime = False

        for i in range(1, len(players)):
            player = players[i]
            if highestPrice - player.moneyOnTable >= player.currentMoney:
                player.currentAlive = 'OOTR'
            elif player.currentAlive == 'Alive' and (highestPrice > player.moneyOnTable or players[0].currentAlive == 'OOTR'):
                if highestPrice >= 0 and highestPrice < 20:
                    if PokerHandler.getTwoCardResult(players[1].cards).score >= 100 and \
                    players[1].riskLevel > 1 and 35 - player.moneyOnTable < player.currentMoney:
                        highestPrice = 35
                    elif PokerHandler.getTwoCardResult(players[1].cards).score > 18 and \
                    players[1].riskLevel > 1 and 25 - player.moneyOnTable < player.currentMoney:
                        highestPrice = 25
                    elif PokerHandler.getTwoCardResult(players[1].cards).score > 30 and \
                    players[1].riskLevel > 0 and 25 - player.moneyOnTable < player.currentMoney:
                        highestPrice = 25
                    elif PokerHandler.getTwoCardResult(players[1].cards).score > 18 and \
                    players[1].riskLevel > 0 and 22 - player.moneyOnTable < player.currentMoney:
                        highestPrice = 22
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                elif highestPrice >= 20 and highestPrice <= 40:
                    if PokerHandler.getTwoCardResult(players[1].cards).score >= 100 and \
                       players[1].riskLevel > 1 and \
                       35 - player.moneyOnTable < player.currentMoney:

                        highestPrice = 35 if 35 > highestPrice \
                                    else highestPrice
                        temp = highestPrice - player.moneyOnTable
                        player.currentMoney -= temp
                        player.moneyOnTable += temp
                    elif PokerHandler.getTwoCardResult(player.cards).score > 18:
                        temp = highestPrice - player.moneyOnTable
                        player.currentMoney -= temp
                        player.moneyOnTable += temp
                    else:
                        player.currentAlive = 'OOTR'
                else:
                    if PokerHandler.getTwoCardResult(player.cards).score >= 100:
                        temp = highestPrice - player.moneyOnTable
                        player.currentMoney -= temp
                        player.moneyOnTable += temp
                    else:
                        player.currentAlive = 'OOTR'
        
        return (highestPrice, isFirstTime, players)