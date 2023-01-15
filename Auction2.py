from Card import *

class SecondAuction:
    @staticmethod
    def secondMoney(isFirstTime, highestMoney, players, communityCards, moneyText):
        highestPrice = highestMoney
        player1Cards = players[1].cards + communityCards
        player2Cards = []
        if len(players) > 2:
            player2Cards = players[2].cards + communityCards
        player3Cards = []
        if len(players) > 3:
            player3Cards = players[3].cards + communityCards
        playersCards = [player1Cards, player2Cards, player3Cards]
        if players[0].currentAlive == 'Alive':
            price = 0
            if isFirstTime:
                player = players[0]
                kwota = moneyText
                try:
                    if kwota == 'p':
                        player.currentAlive = 'OOTR'
                    else:
                        price = int(kwota)
                        if price > player.currentMoney or price < 1:
                            raise ValueError('Niepoprawna wartość kwoty licytacji')
                        highestPrice += price
                        player.currentMoney -= price
                        player.moneyOnTable += price
                    
                except:
                    raise TypeError('Nie została prawidłowo podana kwota licytacji')
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
                            if price > player.currentMoney or price < 1:
                                raise ValueError('Niepoprawna wartość kwoty licytacji')
                            if price < highestPrice - player.moneyOnTable:
                                player.currentAlive = 'OOTR'
                                price = 0
                                print('Za mala kwota aby wyrownac lub podbic')
                            else:
                                highestPrice = price+player.moneyOnTable
                                player.currentMoney -= price
                                player.moneyOnTable += price
                        except:
                            raise TypeError('Nie została prawidłowo podana kwota licytacji')
        isFirstTime = False

        for i in range(1, len(players)):
            player = players[i]
            if highestPrice - player.moneyOnTable >= player.currentMoney:
                player.currentAlive = 'OOTR'
            elif player.currentAlive == 'Alive' and (highestPrice > player.moneyOnTable or players[0].currentAlive == 'OOTR'):
                if highestPrice < 30 and highestPrice < player.currentMoney:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 60:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                                37 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 37
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 300 and \
                                33 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 33
                            elif 35 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 35
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 1800 and \
                                45 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 45
                            elif PokerHandler.getBestCards(playersCards[i-1]).score >= 300 and \
                                40 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 40
                            elif PokerHandler.getBestCards(playersCards[i-1]).score >= 200 and \
                                35 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 35
                            elif 30 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 30
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                elif highestPrice < 35 and highestPrice < player.currentMoney:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 100:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                                40 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 40
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and \
                                35 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 35
                            elif 35 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 35
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                                50 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 50
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and \
                                45 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 45
                            elif 40 - player.moneyOnTable <= player.currentMoney:
                                highestPrice = 40
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                elif highestPrice <= 40:
                    if (PokerHandler.getBestCards(playersCards[i-1]).score > 50 or player.riskLevel == 2) \
                        and highestPrice < player.currentMoney:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                                50 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 50
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and \
                                45 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 45
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 300 and \
                                42 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 42
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                                55 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 55
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and \
                                50 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 50
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 300 and \
                                45 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 45
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice <= 45:
                    if (PokerHandler.getBestCards(playersCards[i-1]).score > 50 or player.riskLevel == 2) \
                        and highestPrice < player.currentMoney:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                                55 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 55
                            elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and \
                                52 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 52
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 300 and \
                                50 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 50
                            elif 45 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 45
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                                60 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 60
                            elif PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and \
                                55 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 55
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 300 and \
                                50 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 50
                            elif 47 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 47
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice <= 50:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if player.riskLevel > 1 and 65 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 65
                        elif player.riskLevel > 0 and 58 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 58
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if player.riskLevel > 1 and 63 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 63
                        elif player.riskLevel > 0 and 55 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 55
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 250 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if player.riskLevel > 1 and 60 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 60
                        elif player.riskLevel > 0 and 52 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 52
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 100 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice <= 60:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if player.riskLevel > 1 and 70 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 70
                        elif player.riskLevel > 0 and 63 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 63
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if player.riskLevel > 1 and 68 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 68
                        elif player.riskLevel > 0 and 62 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 62
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 250 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if player.riskLevel > 1 and 62 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 62
                        elif player.riskLevel > 0 and 60 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 60
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 100 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                else:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and highestPrice <= player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'

        return (highestPrice, isFirstTime, players)
