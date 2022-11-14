import requests
import discord
from discord.ext import commands
import io
from PIL import Image
import time
 
 
bot = commands.Bot(command_prefix='!', description="ayuda bot") #Comando
bot.remove_command("help") # Borra el comando por defecto !help
 
 
@bot.command()
async def tv(ctx, *, canal):
    await ctx.message.delete() #Borramos el comando para no dejar sucio el chat xD
    await ctx.send(f"Generando información del canal {canal}...", delete_after=0)
    time.sleep(3) #Añadimos un tiempo para que sea borrado
    urlcanal = requests.get(f"https://mab.mediaset.es/1.0.0/get?oid=mtmw&eid=/v2/live/mtweb?url=www.mitele.es/directo/{canal}/")
   
    canaltv = urlcanal.json()['event']['name']
    
    imagenurl = urlcanal.json()['event']['image']
    nombreCanal= urlcanal.json()['event']['channel']
    descripcion = urlcanal.json()['event']['description']
    logo_canal = urlcanal.json()['video']['dataPoster']
    imagencanal = Image.open(io.BytesIO(requests.get(imagenurl).content))
    with io.BytesIO() as image_binary:

        imagencanal.save(image_binary, 'PNG')
        image_binary.seek(0)
        embed = discord.Embed(title=f"{nombreCanal}",description=f"{canaltv}", color=discord.Colour.random())
        
        embed.set_author(name="TV")
        embed.set_thumbnail(url=f"{logo_canal}")
        embed.set_image(url="attachment://imagen_canal.png")
        
        embed.set_footer(text=f"{descripcion}", icon_url=f"{imagenurl}")


        await ctx.send(embed=embed,file=discord.File(fp=image_binary, filename='imagen_canal.png'))


@tv.error
async def tv_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error el canal no existe!")
 
@bot.event
async def on_ready():
    print("BOT listo!")
    
 
    
bot.run('') #OBTEN UN TOKEN EN: https://discord.com/developers/applications

