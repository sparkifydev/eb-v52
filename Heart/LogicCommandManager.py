from Heart.Commands.Server.ChangeAvatarNameCommand import ChangeAvatarNameCommand
from Heart.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand
from Heart.Commands.Server.LogicStarRoadRefreshCommand import LogicStarRoadRefreshCommand
from Heart.Commands.Server.LogicRefreshRandomRewardsCommand import LogicRefreshRandomRewardsCommand
from Heart.Commands.Client.HeroSeenCommand import HeroSeenCommand

from Heart.Commands.Client.PurchaseOfferCommand import PurchaseOfferCommand
from Heart.Commands.Client.SetPlayerThumbnailCommand import SetPlayerThumbnailCommand
from Heart.Commands.Client.SetPlayerNameColorCommand import SetPlayerNameColorCommand
from Heart.Commands.Client.LevelUpCommand import LevelUpCommand
from Heart.Commands.Client.LogicClaimRankUpRewardCommand import LogicClaimRankUpRewardCommand
from Heart.Commands.Client.LogicStarRoadRewardCommand import LogicStarRoadRewardCommand
from Heart.Commands.Client.LogicPurchaseBrawlpassProgressCommand import LogicPurchaseBrawlpassProgressCommand
from Heart.Commands.Client.LogicPurchaseBrawlPassCommand import LogicPurchaseBrawlPassCommand
from Heart.Commands.Client.LogicSelectEmoteCommand import LogicSelectEmoteCommand
from Heart.Commands.Client.LogicSelectSkinCommand import LogicSelectSkinCommand
from Heart.Commands.Client.LogicPurchaseBrawlerCommand import LogicPurchaseBrawlerCommand
from Heart.Commands.Client.LogicSetPlayerBattleCardCommand import LogicSetPlayerBattleCardCommand
from Heart.Commands.Client.LogicSetPlayerFavouriteBrawlerCommand import LogicSetPlayerFavouriteBrawlerCommand
from Heart.Commands.Client.LogicOpenRandomCommand import LogicOpenRandomCommand
from Heart.Commands.Server.LogicClaimMasteriesCommand import LogicClaimMasteriesCommand
from Heart.Commands.Client.LogicViewInboxNotificationCommand import LogicViewInboxNotificationCommand
from Heart.Commands.Client.SelectCharacterCommand import SelectCharacterCommand

class LogicCommandManager:
    commandsList = {
        201: ChangeAvatarNameCommand,
        202: 'DiamondsAddedCommand',
        203: LogicGiveDeliveryItemsCommand,
        204: 'DayChangedCommand',
        205: 'DecreaseHeroScoreCommand',
        206: 'AddNotificationCommand',
        207: 'ChangeResourcesCommand',
        208: 'TransactionsRevokedCommand',
        209: 'KeyPoolChangedCommand',
        210: 'IAPChangedCommand',
        211: 'OffersChangedCommand',
        212: 'PlayerDataChangedCommand',
        213: 'InviteBlockingChangedCommand',
        214: 'GemNameChangeStateChangedCommand',
        215: 'SetSupportedCreatorCommand',
        216: 'CooldownExpiredCommand',
        217: 'ProLeagueSeasonChangedCommand',
        218: 'BrawlPassSeasonChangedCommand',
        219: 'BrawlPassUnlockedCommand',
        220: 'HerowinQuestsChangedCommand',
        222: 'RankedSeasonChangedCommand',
        223: 'CooldownAddedCommand',
        224: 'SetESportsHubNotificationCommand',
        227: LogicStarRoadRefreshCommand,
        228: LogicRefreshRandomRewardsCommand,
        500: 'GatchaCommand',
        503: 'ClaimDailyRewardCommand',
        504: 'SendAllianceMailCommand',
        505: SetPlayerThumbnailCommand,
        506: LogicSelectSkinCommand,
        507: 'UnlockSkinCommand',
        508: 'ChangeControlModeCommand',
        509: 'PurchaseDoubleCoinsCommand',
        511: 'HelpOpenedCommand',
        512: 'ToggleInGameHintsCommand',
        514: 'DeleteNotificationCommand',
        515: 'ClearShopTickersCommand',
        517: LogicClaimRankUpRewardCommand,
        518: 'PurchaseTicketsCommand',
        519: PurchaseOfferCommand,
        520: LevelUpCommand,
        521: 'PurchaseHeroLvlUpMaterialCommand',
        522: HeroSeenCommand,
        523: 'ClaimAdRewardCommand',
        524: 'VideoStartedCommand',
        525: SelectCharacterCommand,
        526: 'UnlockFreeSkinsCommand',
        527: SetPlayerNameColorCommand,
        528: LogicViewInboxNotificationCommand,
        529: 'SelectStarPowerCommand',
        530: 'SetPlayerAgeCommand',
        531: 'CancelPurchaseOfferCommand',
        532: 'ItemSeenCommand',
        533: 'QuestSeenCommand',
        534: LogicPurchaseBrawlPassCommand,
        535: 'ClaimTailRewardCommand',
        536: LogicPurchaseBrawlpassProgressCommand,
        537: 'VanityItemSeenCommand',
        538: LogicSelectEmoteCommand,
        539: 'BrawlPassAutoCollectWarningSeenCommand',
        540: 'PurchaseChallengeLivesCommand',
        541: 'ClearESportsHubNotificationCommand',
        542: 'SelectGroupSkinCommand',
        560: LogicPurchaseBrawlerCommand,
        562: LogicStarRoadRewardCommand,
        569: LogicClaimMasteriesCommand,
        568: LogicSetPlayerBattleCardCommand,
        570: LogicSetPlayerFavouriteBrawlerCommand,
        571: LogicOpenRandomCommand
    }

    def getCommandsName(commandType):
        try:
            command = LogicCommandManager.commandsList[commandType]
        except KeyError:
            command = str(commandType)
        if isinstance(command, str):
            return command
        else:
            return command.__name__

    def commandExist(commandType):
        return commandType in LogicCommandManager.commandsList

    def createCommand(commandType, commandPayload=b''):
        commandList = LogicCommandManager.commandsList
        if LogicCommandManager.commandExist(commandType):
            print(LogicCommandManager.getCommandsName(commandType), "created")
            if isinstance(commandList[commandType], str):
                print(commandType, "skipped")
                return None
            else:
                return commandList[commandType](commandPayload)
        else:
            print(commandType, "skipped")
            return None

    def isServerToClient(commandType):
        if 200 <= commandType < 500:
            return True
        elif 500 <= commandType:
            return False