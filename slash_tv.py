import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashCommand, SlashContext
import io
from PIL import Image
import requests
import time

bot = commands.Bot(command_prefix='!', description="ayuda bot")
bot.remove_command("help")

# Comando slash
slash = SlashCommand(bot, sync_commands=True)
@slash.slash(
    name="tv",
    description="Obtener información del canal de TV",
    
    options=[
        create_option(
            name="canal",
            description="Selecciona el canal de televisión",
            option_type=3,
            required=True,
            choices=[
                {"name": "Telecinco", "value": "Telecinco"},
                {"name": "Cuatro", "value": "Cuatro"},
                {"name": "fdf", "value": "fdf"},
                {"name": "Divinity", "value": "Divinity"},
                {"name": "Boing", "value": "Boing"},
                {"name": "Energy", "value": "Energy"},
                {"name": "bemad", "value": "bemad"},
                {"name": "acontraplus", "value": "acontraplus"},
                {"name": "fight-sports", "value": "fight-sports"},
                {"name": "mtmad-24h", "value": "mtmad-24h"}
            ]
        )
    ]
)
async def tv_slash(ctx: SlashContext, canal: str):
    await ctx.defer()

    urlcanal = requests.get(f"https://mab.mediaset.es/1.0.0/get?oid=mtmw&eid=/v2/live/mtweb?url=www.mitele.es/directo/{canal}/")

    canaltv = urlcanal.json()['event']['name']
    imagenurl = urlcanal.json()['event']['image']
    nombreCanal = urlcanal.json()['event']['channel']
    descripcion = urlcanal.json()['event']['description']
    logo_canal = urlcanal.json()['video']['dataPoster']
    imagencanal = Image.open(io.BytesIO(requests.get(imagenurl).content))

    with io.BytesIO() as image_binary:
        imagencanal.save(image_binary, 'PNG')
        image_binary.seek(0)

        embed = discord.Embed(title=f"{nombreCanal}", description=f"{canaltv}\n\n\n{descripcion}", color=discord.Colour.random())
        embed.set_author(name="TV")
        embed.set_thumbnail(url=f"{logo_canal}")
        embed.set_image(url="attachment://imagen_canal.png")
        embed.set_footer(text=f" ", icon_url=f"{imagenurl}")

        await ctx.send(embed=embed, file=discord.File(fp=image_binary, filename='imagen_canal.png'))

# Manejo de errores para el comando slash
@tv_slash.error
async def tv_slash_error(ctx: SlashContext, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error: el canal no existe!")


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

bot.run('') #OBTEN UN TOKEN EN: https://discord.com/developers/applications
