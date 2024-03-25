import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
from PIL import ImageChops
from PIL import Image
import pyautogui
import pydirectinput

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class PanelView(View):
    def buttonInit(self):
        super().buttonInit()

    @discord.ui.button(emoji='📷', style=discord.ButtonStyle.secondary, row=1,)
    async def camera(self, interaction, button):
        await updateInteraction(interaction, "none")
        
    @discord.ui.button(emoji='⬆', style=discord.ButtonStyle.primary, row=1)
    async def up_button(self, interaction, button):
        await updateInteraction(interaction, "up")
        
    @discord.ui.button(emoji='🖱️', style=discord.ButtonStyle.secondary, row=1)
    async def icon(self, interaction, button):
        await updateInteraction(interaction, "click")
        
    @discord.ui.button(emoji='⬅', style=discord.ButtonStyle.primary, row=2)
    async def left_button(self, interaction, button):
        await updateInteraction(interaction, "left")
        
    @discord.ui.button(emoji='🔦', style=discord.ButtonStyle.secondary, row=2)
    async def nightvision_button(self, interaction, button):
        await updateInteraction(interaction, "nightvision")

    @discord.ui.button(emoji='➡', style=discord.ButtonStyle.primary, row=2)
    async def right_button(self, interaction, button):
        await updateInteraction(interaction, "right")
    
    @discord.ui.button(emoji='⏮️', style=discord.ButtonStyle.secondary, row=3)
    async def farleft_button(self, interaction, button):
        await updateInteraction(interaction, "farleft")
        
    @discord.ui.button(emoji='⬇', style=discord.ButtonStyle.primary, row=3)
    async def down_button(self, interaction, button):
        await updateInteraction(interaction, "down")
        
    @discord.ui.button(emoji='⏭️', style=discord.ButtonStyle.secondary, row=3)
    async def farright_button(self, interaction, button):
        await updateInteraction(interaction, "farright")


class EmptyView(View):
    def buttonInit(self):
        super().buttonInit()

@bot.command()
async def cctv(ctx):
    # Handle the embed
    embed = discord.Embed(title='Remote Control', description='Use the buttons below to control the mouse', color=0x2b2d31)
    embed.set_image(url='attachment://screenshot.png')
    
    # Send the message
    await ctx.send(view=PanelView(), embed=embed, file=discord.File('screenshot.png'))


async def updateInteraction(interaction, action):
    await interaction.response.edit_message(content= 'One moment...', view=EmptyView())
    if(action == "up"):
        for i in range(30):
            pydirectinput.moveRel(0, -10, relative=True)
        await screenShotUpdate(interaction)
    if(action == "down"):
        for i in range(30):
            pydirectinput.moveRel(0, 10, relative=True)
        await screenShotUpdate(interaction)
    if(action == "left"):
        for i in range(30):
            pydirectinput.moveRel(-10, 0, relative=True)
        await screenShotUpdate(interaction)
    if(action == "right"):
        for i in range(30):
            pydirectinput.moveRel(10, 0, relative=True)
        await screenShotUpdate(interaction)
    if(action == "none"):
        await screenShotUpdate(interaction)
    if(action == "click"):
        pyautogui.click()
        await screenShotUpdate(interaction)
    if(action == "farright"):
        for i in range(95):
            pydirectinput.moveRel(10, 0, relative=True)
        await screenShotUpdate(interaction)
    if(action == "farleft"):
        for i in range(95):
            pydirectinput.moveRel(-10, 0, relative=True)
        await screenShotUpdate(interaction)
    if(action == "nightvision"):
        pyautogui.press('n')
        await screenShotUpdate(interaction)

async def screenShotUpdate(interaction):
    # Screenshot
    pyautogui.screenshot("screenshot.png")
    # Handle the embed
    embed = discord.Embed(title='Remote Control', description='Use the buttons below to control the mouse', color=0x2b2d31)
    embed.set_image(url='attachment://screenshot.png')
    # Update the message
    await interaction.message.edit(content="CCTV Camera, last updated <t:" + # Timestamp for the message.
        str(int(datetime.now().timestamp()))
        + ":R>", embed=embed, attachments=[discord.File('screenshot.png')], view=PanelView())


bot.run(os.environ['TOKEN'])