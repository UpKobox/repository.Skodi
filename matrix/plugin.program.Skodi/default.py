# Module: default
# Author: CoKodico
# Created on: 15.09.2023
import xbmcplugin
from urllib.parse import quote_plus, unquote_plus, parse_qsl
import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
import xbmcplugin
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import os
import shutil
import requests
import random
import re

artworkPath = xbmcvfs.translatePath('special://home/addons/plugin.program.Skodi/resources/media/')
fanart = artworkPath + "fanart.jpg"

def notice(content):
    log(content, xbmc.LOGINFO)

def log(msg, level=xbmc.LOGINFO):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level)

def showErrorNotification(message):
    xbmcgui.Dialog().notification("Skodi", message,
                                  xbmcgui.NOTIFICATION_ERROR, 5000)
def showInfoNotification(message):
    xbmcgui.Dialog().notification("Skodi", message, xbmcgui.NOTIFICATION_INFO, 15000)

def add_dir(name, mode, thumb):
    u = sys.argv[0] + "?" + "action=" + str(mode)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'icon': thumb})
    liz.setProperty("fanart_image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

##############################################

# MENU PRINCIPAL
def main_menu():
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Menu Skodi[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')       
    add_dir("[COLOR aqua]- Choisissez un skin préconfiguré[/COLOR]", 'hk2', artworkPath + 'unnamed.jpg')
    add_dir("[COLOR yellow]-- Installer Skin[/COLOR] (Habillage en obtenir plus...)", 'inst_skin', artworkPath + 'install (2).jpg')
    add_dir("[COLOR lime]--- Ouvrir U2P[/COLOR]", 'ouvrir_u2p', artworkPath + 'icon (U2P).png')
    add_dir("[COLOR lime]---- U2P Token et Bloc-notes (Rentry et Uptobox uniquement)[/COLOR]", 'majHk', artworkPath + '8lULqB5P_400x400.png')
    add_dir("[COLOR magenta]----- Menu HK2 Maj et paramètres / Menu Skin Sauvegardes[/COLOR]", 'menumajhk2', artworkPath + 'istockphoto-1131394388-170667a.jpg')    
    #add_dir("[COLOR lime]Maj Database HK2[/COLOR]", 'menumajhk2', artworkPath + 'icone.png')
    #add_dir("[COLOR blueviolet]----- Sauvegarde et restauration[/COLOR]", 'save_restor', artworkPath + 'save.png')
    #add_dir("[COLOR darkviolet]--- Nettoyer KODI[/COLOR]", 'nettoye', artworkPath + 'icone.png')
    #add_dir("[COLOR yellow]------ Menu repository (A faire, Après installation)[/COLOR]", 'inst_add', artworkPath + 'click-here-button.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU INSTALLER LES REPOSITORY 
def inst_add():
    xbmcplugin.setPluginCategory(__handle__, "Installer les Repo et Skins")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR darkorange]1 - [/COLOR][COLOR yellow]Installer les repo [/COLOR](Redemarrage Kodi obligatoire)", 'inst_tout', artworkPath + 'download-icon.jpg')    
    add_dir("[COLOR darkorange]2 - [/COLOR][COLOR yellow]Activer les repo[/COLOR]", 'au_maj2', artworkPath + 'install.jpg')    
    add_dir("[COLOR darkorange]3 - [/COLOR][COLOR yellow]Installer Skins [/COLOR](Habillage en obtenir plus...)", 'inst_skin', artworkPath + 'install3.jpg') 
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

# MENU INSTALLER ADDONS ADDITIONNELS
def inst_add2():
    xbmcplugin.setPluginCategory(__handle__, "Installer addons additionnels")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR red]1[/COLOR] Copier [COLOR deepskyblue]addons additionnels[/COLOR] en un clic", 'inst_tout2', artworkPath + 'fanart (Ray).jpg')
    add_dir("[COLOR red]2[/COLOR] Relancer Kodi clic ici", 'inst_quit2', artworkPath + 'fanart (Ray).jpg')
    add_dir("[COLOR red]3[/COLOR] Activer [COLOR deepskyblue]addons additionnels[/COLOR] en un clic", 'inst_act2', artworkPath + 'fanart (Ray).jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)


# INSTALLER LES REPOSITORY 
def inst_tout():
    #install repository additionnels
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
        shutil.rmtree(dirPath)
    except:
        print('Error while deleting directory')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(REPO,Téléchargement en cours...)")
    # telechargement et extraction du zip
    zipurl = 'https://github.com/UpKobox/Skodi/raw/main/repo.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp/addons')
    destination_dir = xbmcvfs.translatePath('special://home/addons')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.sleep(2000)
    xbmc.executebuiltin( 'Notification(OK, Les addons sont installés, 2000)' )
    xbmc.sleep(1000)
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.heppen", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.jurialmunkey", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.lattsrepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.titan.bingie.mod", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.marcelveldt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.RayRepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.auramod.aio", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.Skodi", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.Skodi", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.video.catchuptvandmore", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "skin.arctic.horizon.2", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.xbmcbackup", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.video.catchuptvandmore", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "resource.images.catchuptvandmore", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.module.inputstreamhelper", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.keymap", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.audio.radio_de", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.skin.helper.skinbackup", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.skinvariables", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "resource.images.studios.coloured", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.texturemaker", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.video.themoviedb.helper", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.trakt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.video.sendtokodiU2P", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.upnext", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.module.youtube.dl", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "resource.images.weatherfanart.multi", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "resource.images.weathericons.white", "enabled": true }}')
    xbmc.sleep(1000)
    xbmc.executebuiltin( 'Notification(ATTENTION, Redemarrage Kodi obligatoire, 2000)' )
    xbmc.sleep(1000)
    xbmc.executebuiltin('Quit')
 
# ACTIVER LES REPOSITORY
def inst_quit():
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.jurialmunkey", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.lattsrepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.titan.bingie.mod", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.marcelveldt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.RayRepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.auramod.aio", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons activer !)")

# ACTIVER ADDONS ADDITIONNELS
def inst_act():
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.jurialmunkey", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.lattsrepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.titan.bingie.mod", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.marcelveldt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.RayRepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.auramod.aio", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons activer !)")

##############################################

# COPIER ADDONS ADDITIONNELS
def inst_tout2():
    #install addons additionnels
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
        shutil.rmtree(dirPath)
    except:
        print('Error while deleting directory')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(ADDONS,Téléchargement en cours...)")
    # telechargement et extraction du zip
    zipurl = 'http://kodi.prf2.ovh/dbs/addons.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp/addons')
    destination_dir = xbmcvfs.translatePath('special://home/addons')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(ATTENTION Redemarrage Kodi obligatoire)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

# QUITTER KODI
def inst_quit2():
    # fermeture de kodi
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

# ACTIVER ADDONS ADDITIONNELS
def inst_act2():
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "resource.uisounds.androidtv", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "plugin.program.autocompletion", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.vstream", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.module.dnspython", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.upnext", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(MISE A JOUR OK,Addons activer !)")

##############################################

# METTRE A JOUR LES ICONES
def au_maj():
    # mise a jour icone aura
    # telechargement et extraction du zip
    zipurl = 'https://github.com/prf2/pack/raw/kodi/au_maj.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp/addon_data')
    destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmcvfs.translatePath('special://home/temp/temp/addons')
    destination_dir2 = xbmcvfs.translatePath('special://home/addons')
    source_dir3 = xbmcvfs.translatePath('special://home/temp/temp/keymaps')
    destination_dir3 = xbmcvfs.translatePath('special://home/userdata/keymaps')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    shutil.copytree(source_dir3, destination_dir3, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK,Mise à jour effectuée !)")
    xbmc.sleep(2000)
    
##############################################
def au_majCoKo():
    # mise a jour icone CoKodico
    # telechargement et extraction du zip
    zipurl = 'https://github.com/UpKobox/Skodi/raw/main/SKIN/media(CoKodico).zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp')
    destination_dir = xbmcvfs.translatePath('special://home/media')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK,Maj 1 effectuée !)")
    xbmc.sleep(2000)
    zipurl = 'https://github.com/UpKobox/Skodi/raw/main/SKIN/png(CoKodico).zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp')
    destination_dir = xbmcvfs.translatePath('special://home/media')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(EXTRACTION OK,Maj 2 effectuée !)")
    xbmc.sleep(2000)
##############################################

# ACTIVER ET METTRE A JOUR LES REPOSITORY
def au_maj2():
    #install repository additionnels
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
        shutil.rmtree(dirPath)
    except:
        print('Error while deleting directory')
    xbmc.sleep(2000)
    xbmc.executebuiltin( 'Notification(Repository, Téléchargement en cours..., 2000)' )
    # telechargement et extraction du zip
    zipurl = 'https://github.com/UpKobox/Skodi/raw/main/repo.zip'
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://home/temp/temp/'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://home/temp/temp/addons')
    destination_dir = xbmcvfs.translatePath('special://home/addons')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.sleep(3000)
    xbmc.executebuiltin( 'Notification(Maj OK, Repository copiés !, 2000)' )
    #active addon
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.autowidget", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.jurialmunkey", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.prototype", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.lattsrepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.titan.bingie.mod", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.marcelveldt", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.UpKobox", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.RayRepo", "enabled": true }}')
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "repository.auramod.aio", "enabled": true }}')
    xbmc.sleep(2000)
    xbmc.executebuiltin( 'Notification(Maj OK, Addons activer !, 2000)' )

##############################################
# Installer Skin
def inst_skin():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin2.py,True)')
##############################################
 # Fenetre Parametres U2P
def settings_u2p():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/settings fenetre U2P.py,True)')


    # Ouvrir U2P
def ouvrir_u2p():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/Ouvrir U2P.py,True)')
##############################################
 # Fenetre Parametres Backup
def settings_Backup():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/Settings Fenetre Backup.py,True)')

 # Ouvrir SHSB
def ouvrir_SHSB():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/Script SHSB.py,True)')

# Ouvrir openwizard
def ouvrir_openwizard():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/openwizard.py,True)')
##############################################
#active addon
def alladdon():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/active alladdon .py,True)')
##############################################


def extractAnotpad():
    numAnotepad = __addon__.getSetting("numAnotepad")
    motifAnotepad = r'.*<\s*div\s*class\s*=\s*"\s*plaintext\s*"\s*>(?P<txAnote>.+?)</div>.*'
    url = "https://anotepad.com/note/read/" + numAnotepad.strip()
    rec = requests.get(url, verify=False)
    r = re.match(motifAnotepad, rec.text, re.MULTILINE|re.DOTALL)
    tabKey = [x.strip() for x in r.group("txAnote").splitlines() if x]
    return tabKey 

def testUptobox(key):
    url = 'https://uptobox.com/api/user/me?token=' + key
    headers = {'Accept': 'application/json'}
    try:
        data = requests.get(url, headers=headers).json()
        status = data["message"]
        validite = data["data"]["premium_expire"]
    except:
        status = "out"
        validite = ""
    return status, validite 

##############################################

# ACTIVER MISE A JOUR DATABASE AUTOMATIQUE
def db_auto():
    #active autoexec
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.autoexec", "enabled": true }}')
    xbmc.sleep(2000)
    #notification
    xbmc.executebuiltin("Notification(AUTOEXEC, activé...)")

# DESACTIVER MISE A JOUR DATABASE AUTOMATIQUE
def db_auto_no():
    #desactive autoexec
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "service.autoexec", "enabled": false }}')
    xbmc.sleep(2000)
    #notification
    xbmc.executebuiltin("Notification(AUTOEXEC, désactivé...)")

##############################################

# CHOIX SKINRAY HK2
def rayhk2():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skins [/COLOR][COLOR yellow]Rayflix[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("lancer : Skin [COLOR red]LIGHT[/COLOR] [COLOR orange] (le + leger)[/COLOR]", 'ChangeSkinsProjectAuraliteetlance', artworkPath + 'icon (Ray).png')
    #add_dir("[COLOR white]Choisir Rayflix:[/COLOR] Skin LIGHT [COLOR deepskyblue] (le + leger)[/COLOR]", 'hk2lite', artworkPath + 'icon (Ray).png')
    add_dir("lancer : Skin [COLOR red]FULL[/COLOR] [COLOR orange] (le + gourmand)[/COLOR]", 'ChangeSkinsProjectAurahk2fulletlance', artworkPath + 'icon (Ray).png')
    #add_dir("[COLOR white]Choisir Rayflix:[/COLOR] Skin FULL [COLOR deepskyblue] (le + gourmand)[/COLOR]", 'hk2full', artworkPath + 'icon (Ray).png')
    add_dir("lancer : Skin [COLOR red]KIDS[/COLOR] [COLOR orange] (special enfants)[/COLOR]", 'ChangeSkinsProjectAurahk2kidsetlance', artworkPath + 'icon (Ray).png')
    #add_dir("[COLOR white]Choisir Rayflix:[/COLOR] Skin KIDS [COLOR deepskyblue] (special enfants)[/COLOR]", 'hk2kids', artworkPath + 'icon (Ray).png')
    add_dir("lancer : Skin [COLOR red]RETRO[/COLOR] [COLOR orange] (pour les nostalgiques)[/COLOR]", 'ChangeSkinsProjectAurahk2retretlance', artworkPath + 'icon (Ray).png')
    #add_dir("[COLOR white]Choisir Rayflix:[/COLOR] Skin RETRO [COLOR deepskyblue](pour les nostalgiques) [/COLOR]", 'hk2retro', artworkPath + 'icon (Ray).png')
    #add_dir("[COLOR lime]Lancer: Skin Rayflix choisi [/COLOR]", 'ChangeSkinsProjectAura', artworkPath + 'icon (Ray).png')
    #add_dir("Menu installation [COLOR lime](Redemarrage necessaire)[/COLOR]", 'inst_add2', artworkPath + 'icon (Ray).png')
    add_dir("Mettre a jour les icones [COLOR lime](Pour les Skins de Rayflix)[/COLOR]", 'au_maj', artworkPath + 'icon (Ray).png')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR magenta]Menu Maj HK2 et Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'icon (U2P).png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# CHOIX SKIN U2PLAY HK2
def hk2():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skin U2Pplay[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Skins de [COLOR yellow](CoKodico)[/COLOR]", 'CoKo', artworkPath + 'icon (CoKodico).jpg')
    add_dir("Skins de [COLOR yellow](Luc562)[/COLOR]", 'Luc562', artworkPath + 'Luc562logos.png')
    add_dir("Skins de [COLOR yellow](Rayflix)[/COLOR]", 'rayhk2', artworkPath + 'icon (Ray).png')
    add_dir("Skins de [COLOR yellow](pistachePoilue)[/COLOR]", 'pistachePoilue', artworkPath + 'pistache.jpg')
    add_dir("Skins de [COLOR yellow](Vicqing)[/COLOR]", 'Vicqing', artworkPath + 'VicQing.png')
    add_dir("Skins de [COLOR yellow](bePurple)[/COLOR]", 'bePurple', artworkPath + 'bePurple.jpg')
    add_dir("Skins de [COLOR yellow](Ghantholiny)[/COLOR]", 'Ghantholiny', artworkPath + 'ghantholiny.png')
    #add_dir("Skins de [COLOR yellow](FanKai)[/COLOR]", 'FanKai', artworkPath + 'FanKai.png')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    add_dir("[COLOR magenta]Menu Maj HK2 et Menu Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY COKODICO
def CoKo():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skin de [/COLOR][COLOR yellow]CoKodico[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Arctic Horizon 2 [COLOR lime](Alpha)[/COLOR]", 'ChangeSkinAH2CoKoetlance', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'hk2AH2', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR red]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'ChangeSkinAH2CoKo', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Titan BINGIE MOD [COLOR lime](le + gourmand)[/COLOR]", 'ChangeSkinbingieCoKoetlance', artworkPath + 'fanart (titanbingieCoKo).jpg')
    #add_dir("[COLOR white]Choisir:[/COLOR] Choisir Skin Titan BINGIE MOD [COLOR yellow](le + gourmand)[/COLOR]", 'titanbingieCoKo', artworkPath + 'fanart (titanbingieCoKo).jpg')
    #add_dir("[COLOR red]Lancer:[/COLOR] Lancer Skin Titan BINGIE MOD [COLOR yellow](le + gourmand)[/COLOR]", 'ChangeSkinbingieCoKo', artworkPath + 'fanart (titanbingieCoKo).jpg')
    #add_dir("[COLOR cyan]lancer :[/COLOR] Skin Copacetic [COLOR lime](WIP Alpha)[/COLOR]", 'ChangeSkincopacetiCoKoetlance', artworkPath + 'fanart (Copacetic).jpg')
    #add_dir("[COLOR white]Choisir:[/COLOR] Choisir Skin Copacetic [COLOR yellow](WIP Alpha)[/COLOR]", 'SkinCoKopacetic', artworkPath + 'fanart (Copacetic).jpg')
    #add_dir("[COLOR red]Lancer:[/COLOR] Lancer Skin Copacetic [COLOR yellow](WIP Alpha)[/COLOR]", 'ChangeSkincopacetiCoKo', artworkPath + 'fanart (Copacetic).jpg')
    #add_dir("[COLOR cyan]lancer :[/COLOR] Skin Aeon [COLOR lime](MQ 8)[/COLOR]", 'ChangeSkinAeonMQ8CoKoetlance', artworkPath + 'fanart (MQ8).jpg')
    add_dir("[COLOR white]Copier:[/COLOR] Skin Aeon [COLOR yellow](MQ 8)[/COLOR]", 'MQ8', artworkPath + 'fanart (MQ8).jpg')
    add_dir("[COLOR cyan]Lancer:[/COLOR] Skin Aeon [COLOR yellow](MQ 8)[/COLOR]", 'ChangeSkinAeonMQ8CoKo', artworkPath + 'fanart (MQ8).jpg')
    add_dir("[COLOR cyan]Mettre a jour les icones [/COLOR][COLOR lime] (Pour les Skins de CoKodico)[/COLOR]", 'au_majCoKo', artworkPath + 'icone.png')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR magenta]Menu Maj HK2 et Menu Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    #add_dir("[COLOR red]Desactiver Mise a Jour Database Automatique[/COLOR]", 'db_auto_no', artworkPath + 'icon (U2P).png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY bePurple
def bePurple():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skin de [/COLOR][COLOR yellow]bePurple[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Arctic Horizon 2 [COLOR lime](WIP Alpha)[/COLOR]", 'skinAH2bePurpleetlance', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](WIP Alpha)[/COLOR]", 'bePurpleAH2', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'skinAH2bePurple', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR cyan]lancer :[/COLOR] Skin Auramod [COLOR yellow](Enfants)[/COLOR]", 'ChangeSkinbePurpleAuraKidetlance', artworkPath + 'icon (enfants).png')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Auramod [COLOR yellow](Enfants)[/COLOR]", 'bePurpleAuraKid', artworkPath + 'icon (enfants).png')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Auramod [COLOR yellow](Enfants)[/COLOR]", 'ChangeSkinskinauramod', artworkPath + 'icon (enfants).png')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Auramod [COLOR lime](U2P)[/COLOR]", 'ChangeSkinskinauramodetlance', artworkPath + 'Skin Auramod.jpg')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Auramod [COLOR yellow][/COLOR]", 'bePurpleAura', artworkPath + 'Skin Auramod.jpg')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Auramod [COLOR yellow](Enfants)[/COLOR]", 'ChangeSkinskinauramod', artworkPath + 'icon (enfants).png')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR magenta]Menu Maj HK2 et Menu Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    #add_dir("[COLOR red]Desactiver Mise a Jour Database Automatique[/COLOR]", 'db_auto_no', artworkPath + 'icon (U2P).png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

############################################################################################

# MENU CHOIX SKIN U2PLAY Luc562
def Luc562():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skin de [/COLOR][COLOR yellow]Luc562[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Arctic Horizon 2 [COLOR lime](WIP Alpha)[/COLOR]", 'skinLuc562AH2etlance', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](WIP Alpha)[/COLOR]", 'Luc562AH2', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'skinLuc562AH2', artworkPath + 'icon (AH2).png')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Aeon Nox [COLOR lime](Sylvo)[/COLOR]", 'ChangeSkinaeonnoxsilvoetlance', artworkPath + 'aeon(nox).jpg')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Aeon Nox [COLOR yellow](Sylvo)[/COLOR]", 'Luc562Aeon', artworkPath + 'aeon(nox).jpg')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Aeon Nox [COLOR yellow](Sylvo)[/COLOR]", 'ChangeSkinaeonnoxsilvo', artworkPath + 'aeon(nox).jpg')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Mimic [COLOR lime](lr)[/COLOR]", 'ChangeSkinmimiclretlance', artworkPath + 'mimic.jpg')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'Luc562Mimic', artworkPath + 'mimic.jpg')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'ChangeSkinmimiclr', artworkPath + 'mimic.jpg')
    add_dir("[COLOR cyan]lancer :[/COLOR] Cosmic [COLOR lime](WIP Alpha)[/COLOR]", 'vicosmicetlanceLuc', artworkPath + 'SkinCosmicIcon.png')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Arctic Horizon [COLOR lime](1)[/COLOR]", 'horizonetlance', artworkPath + 'skin.arctic.horizon.png')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR magenta]Menu Maj HK2 et Menu Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY pistachePoilue
def pistachePoilue():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skin de [/COLOR][COLOR yellow]pistachePoilue[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Arctic Horizon 2 [COLOR lime](WIP Alpha)[/COLOR]", 'skinAH2pistachePoilueetlance', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](WIP Alpha)[/COLOR]", 'pistachePoilueAH2', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'skinAH2pistachePoilue', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR magenta]Menu Maj HK2 et Menu Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY Vicqing
def Vicqing():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skin de [/COLOR][COLOR yellow]Vicqing[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]lancer :[/COLOR] Cosmic [COLOR lime](WIP Alpha)[/COLOR]", 'vicosmicetlance', artworkPath + 'SkinCosmicIcon.png')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](WIP Alpha)[/COLOR]", 'pistachePoilueAH2', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon 2 [COLOR yellow](Alpha)[/COLOR]", 'skinAH2pistachePoilue', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR magenta]Menu Maj HK2 et Menu Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY Ghantholiny
def Ghantholiny():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skin de [/COLOR][COLOR yellow]Ghantholiny[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Arctic Horizon 2 [COLOR lime](WIP Alpha)[/COLOR]", 'ChangeSkinarctichorizon2etlance', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR cyan]lancer :[/COLOR] Skin Arctic Horizon [COLOR lime](1)[/COLOR]", 'ChangeSkinarctichorizonetlance', artworkPath + 'skin.arctic.horizon.png')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Arctic Horizon [COLOR lime](1)[/COLOR]", 'ChangeSkinarctichorizonetlance', artworkPath + 'skin.arctic.horizon.png')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Arctic Horizon [COLOR yellow](1)[/COLOR]", 'ChangeSkinarctichorizon', artworkPath + 'mimic.jpg')
    add_dir("[COLOR cyan]lancer :[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'GhantholinyMimicetlance', artworkPath + 'mimic.jpg')
    #add_dir("[COLOR white]Choisir:[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'GhantholinyMimic', artworkPath + 'mimic.jpg')
    #add_dir("[COLOR lime]Lancer:[/COLOR] Skin Mimic [COLOR yellow](lr)[/COLOR]", 'GhantholinyMimichange', artworkPath + 'mimic.jpg')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR magenta]Menu Maj HK2 et Menu Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# MENU CHOIX SKIN U2PLAY FanKai
#def FanKai():
    #choix skin
    #xbmcplugin.setPluginCategory(__handle__, "[COLOR lime]Skin de [/COLOR][COLOR yellow]FanKai[/COLOR]")
    #xbmcplugin.setContent(__handle__, 'files')
    #add_dir("[COLOR cyan]installer [/COLOR]FanKai Affiche...[COLOR lime][/COLOR]", 'FanKai', artworkPath + 'FanKai2.jpg')
    #add_dir("[COLOR lime]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR magenta]Menu Maj HK2 et Menu Skin Sauvegarde[/COLOR]", 'menumajhk2', artworkPath + 'NETTOYER1.jpg')
    #xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################



##############################################



##############################################
def kodi_save_restor():
    #menu sauvegarde restauration Kodi
    xbmcplugin.setPluginCategory(__handle__, "[COLOR cyan]Sauvegarde et restauration Kodi[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR lime]Sauvegarder tout [/COLOR][COLOR yellow](addon Backup nécessaire !)[/COLOR]", 'skin_save3', artworkPath + 'icon (backup).png')
    add_dir("[COLOR yellow]Ouvrir Paramètres Addon Backup [/COLOR]", 'settings_Backup', artworkPath + 'icon (backup).png')
    add_dir("[COLOR magenta]Restaurer tout [/COLOR][COLOR yellow](addon Backup nécessaire , dans Repo Kodi !)[/COLOR]", 'skin_restor3', artworkPath + 'icon (backup).png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
##############################################
def skin_save_restor():
    #menu sauvegarde restauration skin
    xbmcplugin.setPluginCategory(__handle__, "[COLOR cyan]Sauvegarde et restauration skin[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR lime]Sauvegarder Skin  [/COLOR][COLOR yellow](addon Skin Helper Service Skin Backup nécessaire, dans Repo Skodi ou Lattsrepo !)[/COLOR]", 'ouvrir_SHSB', artworkPath + 'icon (SHSB).png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)
##############################################

# IMPORT CHOIX SKIN
def importSkin(zipurl):
    # suppression dossier temporaire
    xbmc.executebuiltin("Notification(DOSSIER TEMP,Effacement en cours...,10)")
    dirPath = xbmcvfs.translatePath('special://temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # telechargement et extraction du zip
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(xbmcvfs.translatePath('special://temp/'))
    # copie des fichiers extraie
    source_dir = xbmcvfs.translatePath('special://temp/addon_data/')
    destination_dir = xbmcvfs.translatePath('special://masterprofile/addon_data')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(Copie Skin , OK ,100)")
    xbmc.sleep(1000)
    xbmc.executebuiltin( 'ReloadSkin()' )
    xbmc.executebuiltin( "Notification(Rafraichissement Skin , Profitez...,2000)" )

##############################################

# MENU SAUVEGARDE RESTAURATION
def save_restor():
    #menu sauvegarde restauration
    xbmcplugin.setPluginCategory(__handle__, "[COLOR cyan]Sauvegarde et restauration[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR lime]CREER UNE SAUVEGARDE DU SKIN[/COLOR]", 'skin_save_restor', artworkPath + 'icon (SHSB).png')
    #add_dir("[COLOR lime]Skin Arctic Horizon 2[/COLOR]", 'skin_save1', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR lime]Skin Rayflix[/COLOR]", 'skin_save2', artworkPath + 'icon (Ray).png')
    
    
    add_dir("[COLOR magenta]CREER UNE SAUVEGARDE KODI[/COLOR]", 'kodi_save_restor', artworkPath + 'icon (backup).png')
    #add_dir("[COLOR magenta]Skin Arctic Horizon 2[/COLOR]", 'skin_restor1', artworkPath + 'icon (AH2).png')
    #add_dir("[COLOR magenta]Skin Rayflix[/COLOR]", 'skin_restor2', artworkPath + 'icon (Ray).png')
    #add_dir("[COLOR magenta]Restaurer Skin  [/COLOR][COLOR yellow](addon Skin Backup nécessaire , dans Repo Skodi!)[/COLOR]", 'skin_restor4', artworkPath + 'icon (backup).png')
    
    
    #add_dir("[COLOR cyan]Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    add_dir("[COLOR yellow]Openwizard [/COLOR]", 'ouvrir_openwizard', artworkPath + 'fanart.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

##############################################

# SAUVEGARDE
def skin_save1():
    xbmc.executebuiltin("Notification(Patienter, Copie en cours...)")
    # COPIE DES DOSSIERS ET FICHIERS DU SKIN
    source_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/skin.arctic.horizon.2')
    destination_dir = xbmcvfs.translatePath('special://home/userdata/Sauvegardes/Skin_sauvegarde/AH2/addon_data/skin.arctic.horizon.2')
    source_dir1 = xbmcvfs.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
    destination_dir1 = xbmcvfs.translatePath('special://home/userdata/Sauvegardes/Skin_sauvegarde/AH2/addon_data/script.skinshortcuts')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    # CREATION ARCHIVE ZIP
    shutil.make_archive((xbmcvfs.translatePath('special://home/userdata/Sauvegardes/Skin_sauvegarde/Skin_sauvegardeAH2')),'zip',(xbmcvfs.translatePath('special://home/userdata/Sauvegardes/Skin_sauvegarde/AH2')))
    xbmc.executebuiltin("Notification(Skin Arctic H. 2 , Archive zip Créer !)")
    sys.exit()

def skin_save2():
    xbmc.executebuiltin("Notification(PREPARATION DES FICHIERS,Copie en cours...)")
    # COPIE DES DOSSIERS ET FICHIERS DU SKIN
    source_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/skin.project.aura')
    destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data/skin.project.aura')
    source_dir1 = xbmcvfs.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
    destination_dir1 = xbmcvfs.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data/script.skinshortcuts')
    source_dir2 = xbmcvfs.translatePath('special://home/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    destination_dir2 = xbmcvfs.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    shutil.copy(source_dir2, destination_dir2)
    # CREATION ARCHIVE ZIP
    shutil.make_archive((xbmcvfs.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/Skin_save1')),'zip',(xbmcvfs.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2')))
    xbmc.executebuiltin("Notification(SKIN SAUVEGARDE, Archive ZIP créée !)")
    sys.exit()

def skin_save3():
    #source_dir = xbmcvfs.translatePath('special://home/addons/plugin.program.Skodi/resources/script.xbmcbackup')
    #destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/script.xbmcbackup')
    #shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    #xbmc.sleep(1000)
    xbmc.executebuiltin('RunScript(script.xbmcbackup,mode=backup)')

def skin_save4():
   xbmc.executebuiltin('RunScript(script.skin.helper.skinbackup,action=backup)')              





#def AddonbBackupKodi():
    #xbmc.executebuiltin('Addon.OpenSettings(script.xbmcbackup)')  
    #source_dir = xbmcvfs.translatePath('special://home/addons/plugin.program.Skodi/resources/script.xbmcbackup')
    #destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/script.xbmcbackup')
    #shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    #xbmc.sleep(1000)
    #xbmc.executebuiltin('RunScript(script.xbmcbackup)')
#def AddonbBackupKodiSettings
    #xbmc.executebuiltin('Addon.OpenSettings(script.xbmcbackup)') 
    #xbmcaddon.Addon(id='script.xbmcbackup').openSettings()

##############################################

# RESTAURATION
def skin_restor1():
    # copie des fichiers sauvegarde
    source_dir = xbmcvfs.translatePath('special://home/userdata/Sauvegardes/Skin_sauvegarde/AH2/addon_data')
    destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data')
    source_dir1 = xbmcvfs.translatePath('special://home/userdata/Sauvegardes/Skin_sauvegarde/AH2/addon_data')
    destination_dir1 = xbmcvfs.translatePath('special://home/userdata/addon_data')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(COPIE OK,Mise à jour effectuée !)")
    xbmc.sleep(2000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ACTUALISATION DU SKIN, Skin Save 1...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    sys.exit()

def skin_restor2():
    # copie des fichiers sauvegarde
    source_dir = xbmcvfs.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data')
    destination_dir = xbmcvfs.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmcvfs.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addons/skin.project.aura')
    destination_dir2 = xbmcvfs.translatePath('special://home/addons/skin.project.aura')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(COPIE OK,Mise à jour effectuée !)")
    xbmc.sleep(5000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ACTUALISATION DU SKIN, Skin Save 2...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    sys.exit()

def skin_restor3():
    xbmc.executebuiltin('RunScript(script.xbmcbackup,mode=restore)')


def skin_restor4():
    xbmc.executebuiltin('RunScript(script.skin.helper.skinbackup,action=restore)')
             
##############################################

# MENU MAJ DATABASE
def menumajhk2():
    # menu maj
    xbmcplugin.setPluginCategory(__handle__, "[COLOR yellow]Mise a Jour Database HK2[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR lime]- Paramètres U2P [/COLOR]", 'settings_u2p', artworkPath + 'icon (U2P).png')
    add_dir("[COLOR lime]- M.A.J HK2 et Skin rafraichissement[/COLOR]", 'actuskin', artworkPath + 'icon (U2P).png')
    add_dir("[COLOR lime]- M.A.J HK2 seulement (rapide)[/COLOR]", 'forcermaj', artworkPath + 'icon (U2P).png')
    #add_dir("[COLOR red]En cas de soucis [/COLOR][COLOR deepskyblue]CHANGER COMPTES PREMIUM ALEATOIRE[/COLOR]", 'menuKey', artworkPath + 'icone.png')
    add_dir("[COLOR cyan]-- Menu Sauvegarde [/COLOR]", 'save_restor', artworkPath + 'save.png')
    add_dir("[COLOR magenta]--- Menu Nettoyage [/COLOR](Attention !)", 'nettoye', artworkPath + 'cleaning-thumbnail.png')
    #add_dir("SKIN FULL [COLOR deepskyblue](le + gourmand)[/COLOR]", 'hk2full', artworkPath + 'icone.png')
    #add_dir("SKIN KIDS [COLOR deepskyblue](special enfants)[/COLOR]", 'hk2kids', artworkPath + 'icone.png')
    #add_dir("SKIN RETRO [COLOR deepskyblue](pour les nostalgiques)[/COLOR]", 'hk2retro', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

def forcermaj():
    # forcer maj
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/U2PplayFast.py,True)') 
    
def actuskin():
    # actualiser 
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/U2Pplay.py,True)')

##############################################

# MENU NETTOYAGE
def nettoye():
    #menu nettoyage
    xbmcplugin.setPluginCategory(__handle__, "[COLOR magenta]Nettoyer Kodi[/COLOR]")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR magenta]Nettoyer tout : [/COLOR](un clic)", 'vider_cache', artworkPath + 'NETTOYER.png')
    add_dir("[COLOR cyan]Vider Cache Uniquement[/COLOR]", 'cache_seul', artworkPath + 'cleaning-thumbnail.png')
    add_dir("[COLOR cyan]Vider Tmp Uniquement[/COLOR]", 'tmp_seul', artworkPath + 'cleaning-icon.jpg')
    add_dir("[COLOR cyan]Vider Packages Uniquement[/COLOR]", 'package_seul', artworkPath + 'NETTOYER1.jpg')
    add_dir("[COLOR cyan]Vider Thumbnails Uniquement[/COLOR]", 'thumb_seul', artworkPath + '2771509.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

##############################################

# NETTOYER TOUT D UN COUP
def vider_cache():
    #nettoyer tout
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(DOSSIER PACKAGES,Effacement en cours...)")
    # suppression dossier packages
    dirPath = xbmcvfs.translatePath('special://home/addons/packages/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(DOSSIER THUMBNAILS,Effacement en cours...)")
    # suppression dossier thumbnails
    dirPath = xbmcvfs.translatePath('special://home/userdata/Thumbnails/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(CACHE TEMP,Effacement en cours...)")
    # suppression dossier cache
    dirPath = xbmcvfs.translatePath('special://home/cache/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

##############################################

# VIDER CACHE
def cache_seul():
    #nettoyaer cache uniquement
    xbmc.executebuiltin("Notification(CACHE TEMP,Effacement en cours...)")
    # suppression dossier cache
    dirPath = xbmcvfs.translatePath('special://home/cache/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# VIDER TMP
def tmp_seul():
    #nettoyaer tmp uniquement
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmcvfs.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    # actualisation du skin
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# VIDER PACKAGES    
def package_seul():
    #nettoyaer packages uniquement
    xbmc.executebuiltin("Notification(DOSSIER PACKAGES,Effacement en cours...)")
    # suppression dossier packages
    dirPath = xbmcvfs.translatePath('special://home/addons/packages/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(TERMINE , ...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# VIDER THUMBNAILS
def thumb_seul():
    #nettoyaer thumbnails uniquement
    xbmc.executebuiltin("Notification(DOSSIER THUMBNAILS,Effacement en cours...)")
    # suppression dossier thumbnails
    dirPath = xbmcvfs.translatePath('special://home/userdata/Thumbnails/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ATTENTION KODI VA SE FERMER , Relancez le...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Quit')

##############################################
def majHk():
    #init addon
    addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
    #passage hebegeur en rentry
    addon.setSetting(id="heberg", value="Rentry")
    #recup valeur key upto
    keyUpto = addon.getSetting("keyupto")
    #recyp num rentry
    numRentry = addon.getSetting("numHeberg")
    # si key upto vide
    if not keyUpto:
        dialog = xbmcgui.Dialog()
        d = dialog.input("Token Uptobox: ", type=xbmcgui.INPUT_ALPHANUM)
        if d:
            keyUpto = d
            addon.setSetting(id="keyupto", value=d.strip())
        else:
            return
    # si num rentry vide
    if not numRentry:
        dialog = xbmcgui.Dialog()
        d = dialog.input("Num rentry Databases: ", type=xbmcgui.INPUT_ALPHANUM)
        if d:
            numRentry = d
            addon.setSetting(id="numHeberg", value=d.strip())
        else:
            return
    notice(keyUpto)
    notice(numRentry)
    showInfoNotification(keyUpto + " " + numRentry)
  

##############################################

# LANCER SKIN :

# AH2 COKODICO
def ChangeSkinAH2CoKo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-AH2.py)')
def ChangeSkinAH2CoKoetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinAH2CoKodico.py)')    
def skinAH2bePurple():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-AH2.py)')
def skinAH2bePurpleetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinAH2bePurple.py)')    
def skinLuc562AH2():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-AH2.py)')
def skinLuc562AH2etlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinLuc562AH2.py)')    
def skinAH2pistachePoilue():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-AH2.py)')
def skinAH2pistachePoilueetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinAH2pistachePoilueAH2.py)')    
# Bingie COKODICO
def ChangeSkinbingieCoKo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-bingieCoKo.py)')
def ChangeSkinbingieCoKoetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinbingieCoKodico.py)')    
# CoKopacetic COKODICO
def ChangeSkincopacetiCoKo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-copacetiCoKo.py)')
def ChangeSkincopacetiCoKoetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskin.copacetiCoKodico.py)')    
# AeonMQ8 COKODICO
def ChangeSkinAeonMQ8CoKo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-AeonMQ8CoKo.py)')
def ChangeSkinAeonMQ8CoKoetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinaeonmq8matrixmodCoKodico.py)')      
# ChangeSkin-skin.auramod bePurple
def ChangeSkinskinauramod():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.auramod.py)') 
def ChangeSkinskinauramodetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskin.bePurpleAura.py)')
def ChangeSkinbePurpleAuraKid():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.auramod.py)') 
def ChangeSkinbePurpleAuraKidetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinChangeSkinbePurpleAuraKid.py)')     
# ChangeSkin-luc562
def ChangeSkinaeonnoxsilvo():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.aeon.nox.silvo.py)') 
def ChangeSkinaeonnoxsilvoetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskin.aeon.nox.silvoLuc562.py)')    
def ChangeSkinmimiclr():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.mimic.lr.py)')
def ChangeSkinmimiclretlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileLuc562Mimic.py)')    
def GhantholinyMimichange():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.mimic.lr.py)') 
def GhantholinyMimicetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileGhantholinyMimic.py)') 
def horizonetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskin.arctic.horizonLuc.py)')       
# ChangeSkin-Ghantholiny
def ChangeSkinarctichorizon():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.arctic.horizon.py)')
def ChangeSkinarctichorizonetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskin.arctic.horizonGhantholiny.py)')   
def ChangeSkinarctichorizon2etlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/skin.arctic.horizon2Ghantholiny.py)')        
# ChangeSkin-ProjectAura
def ChangeSkinsProjectAura():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/ChangeSkin-skin.project.aura.py)')
def ChangeSkinsProjectAuraliteetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofileskinChangeSkinsProjectAuraliteetlance.py)') 
def ChangeSkinsProjectAurahk2fulletlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofilesChangeSkinsProjectAurahk2fulletlance.py)')
def ChangeSkinsProjectAurahk2kidsetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofilesChangeSkinsProjectAurahk2kidsetlance.py)') 
def ChangeSkinsProjectAurahk2retretlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/testprofilesChangeSkinsProjectAurahk2retretlance.py)')
def vicosmicetlance():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/skinVicosmic.py)')
def vicosmicetlanceLuc():
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.Skodi/resources/Lucosmic.py)')


##############################################

def router(paramstring):
    params = dict(parse_qsl(paramstring))    
    dictActions = {
        #key uptobox
        #'menuKey':(menuKey, ""),
        #skin
        'hk2lite': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/RayFlix/hk2_light/hk2_light.zip'),
        'hk2full': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/RayFlix/hk2_full/hk2_full.zip'),
        'hk2kids': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/RayFlix/hk2_kids/hk2_kids.zip'),
        'hk2leger': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/RayFlix/hk2_light/hk2_light.zip'),
        'hk2complet': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/RayFlix/hk2_full/hk2_full.zip'),
        'hk2enfants': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/RayFlix/hk2_kids/hk2_kids.zip'),
        'hk2retro': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/RayFlix/hk2_retro/hk2_retro.zip'),
        'hk2AH2': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/AH2_HK2.zip'),
        'titanbingieCoKo': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/Skin_Titan_BINGIE_MOD.zip'),
        'SkinCoKopacetic': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/Skin_Copacetic.zip'), 
        'MQ8': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/Skin_Aeon_MQ_8.zip'), 
        'bePurpleAH2': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/bePurple/skin.arctic.horizon.2.zip'),
        'bePurpleAuraKid': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/bePurple/skin.auramod.enfant.zip'),
        'bePurpleAura': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/bePurple/skin.auramod.zip'),
        'Luc562AH2': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/luc562/skin.arctic.horizon.2.zip'),   
        'Luc562Aeon': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/luc562/skin.aeon.nox.silvo.zip'),
        'Luc562Mimic': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/luc562/skin.mimic.lr.zip'),
        'Luc562AH1': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/luc562/skin.arctic.horizon.zip'), 
        'pistachePoilueAH2': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/pistachePoilue/skin.arctic.horizon.2.zip'),   
        'GhantholinyAH': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/Ghantholiny/skin.arctic.horizon.zip'),
        'GhantholinyAH2': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/Ghantholiny/skin.artic.horizon.2.zip'),
        'GhantholinyMimic': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/Ghantholiny/sin.mimic.lr.zip'),
        'vicosmic': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/Vicing/CosmicVic.zip'), 
        'Lucosmic': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/luc562/skin.cosmic.zip'),
        #'FanKai': (importSkin, 'https://github.com/UpKobox/Skodi/raw/main/SKIN/FanKai/fankai.zip'),
        #Choiir et Lancer Skin
        'ChangeSkinAH2CoKo': (ChangeSkinAH2CoKo, ""),
        'skinAH2bePurple': (skinAH2bePurple, ""),
        'skinLuc562AH2': (skinLuc562AH2, ""),
        'skinAH2pistachePoilue': (skinAH2pistachePoilue, ""), 
        'ChangeSkinsProjectAura': (ChangeSkinsProjectAura, ""),
        'ChangeSkinbingieCoKo': (ChangeSkinbingieCoKo, ""),
        'ChangeSkincopacetiCoKo': (ChangeSkincopacetiCoKo, ""),
        'ChangeSkinAeonMQ8CoKo': (ChangeSkinAeonMQ8CoKo, ""),
        'ChangeSkinskinauramod': (ChangeSkinskinauramod, ""),
        'ChangeSkinaeonnoxsilvo': (ChangeSkinaeonnoxsilvo, ""),
        'ChangeSkinmimiclr': (ChangeSkinmimiclr, ""),
        'ChangeSkinarctichorizon': (ChangeSkinarctichorizon, ""),
        'ChangeSkinAH2CoKoetlance': (ChangeSkinAH2CoKoetlance, ""),
        'skinAH2bePurpleetlance': (skinAH2bePurpleetlance, ""),
        'skinLuc562AH2etlance': (skinLuc562AH2etlance, ""),
        'skinAH2pistachePoilueetlance': (skinAH2pistachePoilueetlance, ""),
        'ChangeSkinbingieCoKoetlance': (ChangeSkinbingieCoKoetlance, ""),
        'ChangeSkincopacetiCoKoetlance': (ChangeSkincopacetiCoKoetlance, ""),
        'ChangeSkinAeonMQ8CoKoetlance': (ChangeSkinAeonMQ8CoKoetlance, ""),
        'ChangeSkinskinauramodetlance': (ChangeSkinskinauramodetlance, ""),
        'ChangeSkinaeonnoxsilvoetlance': (ChangeSkinaeonnoxsilvoetlance, ""),
        'ChangeSkinmimiclretlance': (ChangeSkinmimiclretlance, ""),
        'GhantholinyMimicetlance': (GhantholinyMimicetlance, ""),
        'GhantholinyMimichange': (GhantholinyMimichange, ""),
        'ChangeSkinarctichorizonetlance': (ChangeSkinarctichorizonetlance, ""),
        'horizonetlance': (horizonetlance, ""),
        'ChangeSkinarctichorizon2etlance': (ChangeSkinarctichorizon2etlance, ""),
        'ChangeSkinsProjectAuraliteetlance': (ChangeSkinsProjectAuraliteetlance, ""),
        'ChangeSkinsProjectAurahk2fulletlance': (ChangeSkinsProjectAurahk2fulletlance, ""),
        'ChangeSkinsProjectAurahk2kidsetlance': (ChangeSkinsProjectAurahk2kidsetlance, ""),
        'ChangeSkinsProjectAurahk2retretlance': (ChangeSkinsProjectAurahk2retretlance, ""),
        'vicosmicetlance': (vicosmicetlance, ""),
        'vicosmicetlanceLuc': (vicosmicetlanceLuc, ""),
        #skin HK2
        'hk2': (hk2, ""),
        'rayhk2': (rayhk2, ""),
        #Contrib Skin HK2
        'CoKo': (CoKo, ""),
        'bePurple': (bePurple, ""),
        'Luc562': (Luc562, ""),
        'pistachePoilue': (pistachePoilue, ""),
        'Vicqing': (Vicqing, ""),
        'Ghantholiny': (Ghantholiny, ""), 
        #'FanKai': (FanKai, ""), 
        #Maj autoexec HK2             
        'db_auto': (db_auto, ""),
        'db_auto_no': (db_auto_no, ""),
        #maj hk2
        "majHk": (majHk, ""),
        "menumajhk2": (menumajhk2, ""),
        "forcermaj": (forcermaj, ""),
        "actuskin": (actuskin, ""),
        #nettoyage
        'vider_cache': (vider_cache, ""),
        'cache_seul': (cache_seul, ""),
        'tmp_seul': (tmp_seul, ""),
        'package_seul': (package_seul, ""),
        'thumb_seul': (thumb_seul, ""),
        'nettoye': (nettoye, ""),
        #sauvegarde restauration
        'save_restor': (save_restor, ""),
        'skin_save_restor': (skin_save_restor, ""),
        'kodi_save_restor': (kodi_save_restor, ""),
        'skin_save1': (skin_save1, ""), 
        'skin_save2': (skin_save2, ""), 
        'skin_save3': (skin_save3, ""), 
        'skin_save4': (skin_save3, ""),
        'skin_restor1': (skin_restor1, ""), 
        'skin_restor2': (skin_restor2, ""), 
        'skin_restor3': (skin_restor3, ""),
        'skin_restor4': (skin_restor3, ""),
        #'AddonbBackupKodi': (AddonbBackupKodi, ""),
        #'AddonbBackupKodiSettings': (AddonbBackupKodiSettings, ""),         
        #autres
        'au_maj': (au_maj, ""),
        'au_majCoKo': (au_majCoKo, ""),
        'au_maj2': (au_maj2, ""),       
        'inst_tout': (inst_tout, ""),
        'inst_tout2': (inst_tout2, ""),
        'inst_add': (inst_add, ""),
        'inst_add2': (inst_add2, ""),
        'inst_act': (inst_act, ""),
        'inst_act2': (inst_act2, ""),
        'inst_quit': (inst_quit, ""),
        'inst_quit2': (inst_quit2, ""),
        'inst_skin': (inst_skin, ""),
        'settings_u2p': (settings_u2p, ""),
        'ouvrir_u2p': (ouvrir_u2p, ""),
        'ouvrir_SHSB': (ouvrir_SHSB, ""),
        'ouvrir_openwizard': (ouvrir_openwizard, ""),
        'alladdon': (alladdon, ""),
        'settings_Backup': (settings_Backup, ""),
        }
        
    if params:
        fn = params['action']
        if fn in dictActions.keys():
            argv = dictActions[fn][1]
            if argv:
                dictActions[fn][0](argv)
            else:
                dictActions[fn][0]()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
         main_menu()

if __name__ == '__main__':
    __addon__ = xbmcaddon.Addon("plugin.program.Skodi")
    __handle__ = int(sys.argv[1])
    router(sys.argv[2][1:])