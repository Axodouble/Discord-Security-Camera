import discord
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
import pyautogui

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class PanelView(View):
    def buttonInit(self):
        super().buttonInit()

    @discord.ui.button(emoji='📷', style=discord.ButtonStyle.secondary, row=1,)
    async def camera(self, interaction, button):
        await updateInteraction(interaction, "none")
    @discord.ui.button(emoji='⬆', style=discord.ButtonStyle.primary, custom_id='up_button', row=1)
    async def up_button(self, interaction, button):
        await updateInteraction(interaction, "up")
    @discord.ui.button(emoji='🖱️', style=discord.ButtonStyle.secondary, custom_id="click", row=1)
    async def icon(self, interaction, button):
        await updateInteraction(interaction, "click")
    @discord.ui.button(emoji='⬅', style=discord.ButtonStyle.primary, custom_id='left_button', row=2)
    async def left_button(self, interaction, button):
        await updateInteraction(interaction, "left")
    @discord.ui.button(emoji='⬇', style=discord.ButtonStyle.primary, custom_id='down_button', row=2)
    async def down_button(self, interaction, button):
        await updateInteraction(interaction, "down")
    @discord.ui.button(emoji='➡', style=discord.ButtonStyle.primary, custom_id='right_button', row=2)
    async def right_button(self, interaction, button):
        await updateInteraction(interaction, "right")

class EmptyView(View):
    def buttonInit(self):
        super().buttonInit()

@bot.command()
async def cctv(ctx):
    embed = discord.Embed(title='Remote Control', description='Use the buttons below to control the mouse', color=0x2b2d31)
    embed.set_image(url='attachment://screenshot.png')
    
    await ctx.send(view=PanelView(), embed=embed, file=discord.File('screenshot.png'))


async def updateInteraction(interaction, direction):
    await interaction.response.edit_message(content= 'One moment...', view=EmptyView())
    
    if(direction == "up"):
        pyautogui.moveRel(0, -100, duration=0.25)
        await screenShotUpdate(interaction)
    if(direction == "down"):
        pyautogui.moveRel(0, 100, duration=0.25)
        await screenShotUpdate(interaction)
    if(direction == "left"):
        pyautogui.moveRel(-100, 0, duration=0.25)
        await screenShotUpdate(interaction)
    if(direction == "right"):
        pyautogui.moveRel(100, 0, duration=0.25)
        await screenShotUpdate(interaction)
    if(direction == "none"):
        await screenShotUpdate(interaction)
    if(direction == "click"):
        pyautogui.click()
        await screenShotUpdate(interaction)

async def screenShotUpdate(interaction):
    # Screenshot
    pyautogui.screenshot("screenshot.png")
    # Handle the embed
    embed = discord.Embed(title='Remote Control', description='Use the buttons below to control the mouse', color=0x2b2d31)
    embed.set_image(url='attachment://screenshot.png')
    # Update the message
    await interaction.message.edit(content="CCTV Camera, last updated <t:" + # Timestamp
        str(int(datetime.now().timestamp()))
        + ":R>", embed=embed, attachments=[discord.File('screenshot.png')], view=PanelView())


bot.run("")