import discord
import requests

from utils.exceptions import TooManyMatches, NoMatchFound


# find a member by their partial name
def find_by_partial(name, guild):
    member = [member for member in guild.members if name.lower() == member.name.lower()]
    if len(member) != 1:
        member = [member for member in guild.members if name.lower() in member.name.lower()]
        if len(member) > 1:
            raise TooManyMatches
        if len(member) < 1:
            raise NoMatchFound
    # there should only be a single member in the list now, this must be the member
    return member[0]

def get_twitch_token(secret, id):
    r = requests.post("https://id.twitch.tv/oauth2/token", params={
        "client_id" : id,
        "client_secret" : secret,
        "grant_type" : "client_credentials"
    })
    r = r.json()
    return r["access_token"]

