"""
Trello Activity Cog

Polls the specified trello board every hour and updates a channel with the latest
activity from that channel.
"""

import discord
from discord.ext import commands
from trello import TrelloClient
import time
import threading
import configparser
import json
import dateutil.parser
import asyncio

# convers action names to human-readable strings,
# and also filters the type of actions that are sent
action_dict = {
    "deleteCard": "Card Deleted",
    "createCard": "Card Created",
    "addMembertoCard": "Member Assigned to Card",
    "commentCard": "Comment left on Card",
    "updateCard": "Card Updated",
    "addLabelToCard": "Label Added",
    "addAttachmentToCard": "Attachment Added"
}

ACTION_FILTER = "addAdminToBoard,addAdminToOrganization,addAttachmentToCard,addBoardsPinnedToMember,addChecklistToCard,addLabelToCard,addMemberToBoard,addMemberToCard,addMemberToOrganization,addToOrganizationBoard,commentCard,convertToCardFromCheckItem,copyBoard,copyCard,copyChecklist,createLabel,copyCommentCard,createBoard,createBoardInvitation,createBoardPreference,createCard,createChecklist,createList,createOrganization,createOrganizationInvitation,deleteAttachmentFromCard,deleteBoardInvitation,deleteCard,deleteCheckItem,deleteLabel,deleteOrganizationInvitation,disablePlugin,disablePowerUp,emailCard,enablePlugin,enablePowerUp,makeAdminOfBoard,makeAdminOfOrganization,makeNormalMemberOfBoard,makeNormalMemberOfOrganization,makeObserverOfBoard,memberJoinedTrello,moveCardFromBoard,moveCardToBoard,moveListFromBoard,moveListToBoard,removeAdminFromBoard,removeAdminFromOrganization,removeBoardsPinnedFromMember,removeChecklistFromCard,removeFromOrganizationBoard,removeLabelFromCard,removeMemberFromBoard,removeMemberFromCard,removeMemberFromOrganization,unconfirmedBoardInvitation,unconfirmedOrganizationInvitation,updateBoard,updateCard,updateCheckItem,updateCheckItemStateOnCard,updateChecklist,updateLabel,updateList,updateMember,updateOrganization,voteOnCard"

SCHEDULER_POLL_RATE = 5 # 30 seconds

class TrelloActivity:
    
    def __init__(self, bot, trello_board_id, trello_api_key, trello_api_token, trello_channel):
        self.bot = bot
        self.board_id = trello_board_id
        self.trello_channel_id = trello_channel
        # not using OAuth process
        self.tclient = TrelloClient(
            api_key=trello_api_key,
            api_secret=trello_api_token
        )
        # get the last activity that took place in the target board
        b = self.tclient.get_board(self.board_id)
        self.last_activity_date = b.get_last_activity()
        self.bot.loop.create_task(self.update_task())

    async def update_task(self):
        
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.update_channel()
            await asyncio.sleep(SCHEDULER_POLL_RATE)


    async def post_action(self, action: dict):
        """
        Post an action as an embed to the Discord channel

        """
        action_type = action["type"]
        if action_type in action_dict:
            # get the channel
            c = self.bot.get_channel(self.trello_channel_id)

            #async with c.typing():
            # make an embed and send a message with the action
            e = self.make_action_embed(action, action_dict[action_type])
            await c.send(action_type, embed=e)
        else:
            print("Ignoring action ", action_type)
            # discard this action
        print("done with action")

    async def update_channel(self):
        # get the trello board
        b = self.tclient.get_board(self.board_id)
        # get all actions that have happened since the previous actoin
        actions = b.fetch_actions(ACTION_FILTER, action_limit=50, before=None, since=self.last_activity_date)

        # this can get spammy
        # print(actions)

        if actions is not None and len(actions) > 0:
            # update the last activity date
            activity_date = dateutil.parser.parse(actions[0]['date'])

            if self.last_activity_date == activity_date:
                # print('Last activity date has not changed')
                return
            else:
                self.last_activity_date = activity_date
                # print('Last activity date: ', self.last_activity_date) 
        else:
            # print('No new actions, or None.')
            return

        # if there are new actions, then send them to the discord channel
        # because we get the most recent actions first, send these in reverse order
        for a in actions[::-1]:
            print("Posting about action ", a)
            await self.post_action(a)
            # post 1/s to lazily get around rate limits
            await asyncio.sleep(5)
        print("Posted all updates.")
    
    def make_action_embed(self, action: dict, action_type: str) -> discord.Embed:
        e = discord.Embed(title=action_type, color=discord.Color.dark_purple())
        
        # add the author
        author = self.get_author(action)
        if author is not None:
            e.set_author(name=author)

        # because I'm lazy, just append info to the description
        e.description = ""

        list_name = self.get_list_name(action)
        if list_name is not None:
            e.description += f"In list {list_name}\n"
        
        board_name = self.get_board_name(action)
        if board_name is not None:
            e.description += f"In board {board_name}\n"
        
        card = self.get_card(action)
        if card is not None:
            e.description += f"Card {card['name']} w/ description {card.get('desc', 'none')}\n"

        card_move = self.get_card_moved(action)
        if card_move is not None:
            e.description += f"Card was moved from {card_move[0]} to {card_move[1]}"
        
        return e

    def get_author(self, action: dict) -> str:
        """
        Gets the author from the action dict
        """
        creator = action.get("memberCreator")
        if creator is not None:
            fullname = creator.get("fullName", "Error")
            initials = creator.get("initials", "N/A")
            return f'{fullname} ({initials})'
        return "N/A"

    def get_list_name(self, action: dict) -> str:
        """
        Gets the list name, if supplied. Returns none if not supplied.
        """
        data = action.get("data")
        if data is not None:
            l = data.get("list")
            if l is not None:
                return l["name"]
        return None

    def get_board_name(self, action: dict) -> str:
        """
        Gets the board name, if supplied.
        """
        data = action.get("data")
        if data is not None:
            b = data.get("board")
            if b is not None:
                return b["name"]
        return None

    def get_card(self, action: dict) -> str:
        """
        Gets the json for a card, if supplied.
        """
        data = action.get("data")
        if data is not None:
            return data.get("card")
        return None

    def get_card_moved(self, action: dict) -> tuple:
        """
        Gets the name the list a card was moved (from, to), if supplied.
        """
        data = action.get("data")
        if data is not None:
            before = data.get("listBefore")
            after = data.get("listAfter")
            if before is not None and after is not None:
                return (before["name"], after["name"])
        return None

        

# add this cog to the bot
def setup(bot):
    # assume that config.ini is in expected path
    config = configparser.ConfigParser()
    with open('config.ini') as config_file:
        config.read_file(config_file)
    board_id = config['Trello']['board_id']
    api_key = config['Trello']['api_key']
    api_token = config['Trello']['api_token']
    trello_channel = int(config['Discord']['trello_channel_id'])
    bot.add_cog(TrelloActivity(bot, board_id, api_key, api_token, trello_channel))

# optional, but helpful for testing via the shell
if __name__ == '__main__':
    import doctest

    doctest.testmod()
