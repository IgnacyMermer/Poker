from Card import *


class FourthAuction:
    @staticmethod
    def fourthMoney(isFirstTime, highestMoney, players, communityCards, 
                    moneyText):
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
                except Exception:
                    raise TypeError('Nie została prawidłowo podana kwota licytacji')
            else:
                player = players[0]
                if player.moneyOnTable < highestPrice:
                    kwota = moneyText
                    if kwota == 'p':
                        player.currentAlive = 'OOTR'
                    elif kwota == 'w':
                        temp = highestPrice - player.moneyOnTable
                        player.currentMoney -= temp
                        player.moneyOnTable += temp
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
                        except Exception:
                            raise TypeError('Nie została prawidłowo podana kwota licytacji')
        isFirstTime = False

        for i in range(1, len(players)):
            player = players[i]
            if highestPrice - player.moneyOnTable >= player.currentMoney:
                player.currentAlive = 'OOTR'
            elif player.currentAlive == 'Alive' and (highestPrice > player.moneyOnTable or players[0].currentAlive == 'OOTR'):
                if highestPrice < 50 and highestPrice < player.currentMoney:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 200:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and 60 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 60
                            elif PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and 54 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 54
                            elif 52 <= player.currentMoney:
                                highestPrice = 52
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and 65 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 65
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and 60 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 60
                            elif 55 <= player.currentMoney:
                                highestPrice = 55
                    player.currentMoney -= highestPrice - player.moneyOnTable
                    player.moneyOnTable += highestPrice - player.moneyOnTable
                elif highestPrice <= 60:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 150:
                        if player.riskLevel == 1:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and 63 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 63
                        elif player.riskLevel == 2:
                            if PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and 66 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 66
                            elif PokerHandler.getBestCards(playersCards[i-1]).score > 500 and 62 - player.moneyOnTable < player.currentMoney:
                                highestPrice = 62
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'
                elif highestPrice <= 65:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 500 and \
                       highestPrice- player.moneyOnTable < player.currentMoney:
                        if player.riskLevel > 1 and 74 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 74
                        elif player.riskLevel > 0 and 68 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 68
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score > 130 and \
                        highestPrice- player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'
                elif highestPrice <= 70:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 1500 and \
                       highestPrice - player.moneyOnTable <= player.currentMoney:
                        if 77 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 77
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 250 and player.riskLevel > 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 72 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 72
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score > 100 and player.riskLevel > 1 \
                        and highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 250 and player.riskLevel > 0 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice <= 75:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 200 and player.riskLevel > 1 and \
                       highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 300 and player.riskLevel > 0 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1800 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 79 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 79
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 2500 and highestPrice <= player.currentMoney:
                        if 82 - player.moneyOnTable <= player.currentMoney:
                            highestPrice = 82
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'
                elif highestPrice <= 80:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 300 and player.riskLevel > 1 and \
                       highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and player.riskLevel > 0 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 2000 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 82 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 82
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 3000 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 87 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 87
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice <= 85:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 400 and player.riskLevel > 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1500 and player.riskLevel > 0 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 3000 and player.riskLevel == 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 84 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 84
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 5000 and player.riskLevel == 2 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 92 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 92
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice <= 90:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 500 and player.riskLevel > 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and player.riskLevel > 0 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 4000 and player.riskLevel == 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 90 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 90
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 5000 and player.riskLevel == 2 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 95 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 95
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice <= 95:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 1000 and player.riskLevel > 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 3500 and player.riskLevel > 0 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 5500 and player.riskLevel == 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 95 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 95
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 6500 and player.riskLevel == 2 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 98 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 98
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                elif highestPrice <= 100:
                    if PokerHandler.getBestCards(playersCards[i-1]).score > 1500 and player.riskLevel > 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 4000 and player.riskLevel > 0 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 6000 and player.riskLevel == 1 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 102 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 102
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    elif PokerHandler.getBestCards(playersCards[i-1]).score >= 7500 and player.riskLevel == 2 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        if 105 - player.moneyOnTable < player.currentMoney:
                            highestPrice = 105
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR' 
                else:
                    if PokerHandler.getBestCards(playersCards[i-1]).score >= 5000 and \
                        highestPrice - player.moneyOnTable < player.currentMoney:
                        player.currentMoney -= highestPrice - player.moneyOnTable
                        player.moneyOnTable += highestPrice - player.moneyOnTable
                    else:
                        player.currentAlive = 'OOTR'
        return (highestPrice, isFirstTime, players)