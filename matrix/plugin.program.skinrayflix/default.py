# Module: default
# Author: Rayflix, noway
# Created on: 19.01.2022
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

artworkPath = xbmcvfs.translatePath('special://home/addons/plugin.program.skinrayflix/resources/media/')
fanart = artworkPath + "fanart.jpg"

def notice(content):
    log(content, xbmc.LOGINFO)

def log(msg, level=xbmc.LOGINFO):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level)

def showErrorNotification(message):
    xbmcgui.Dialog().notification("UptoRay", message,
                                  xbmcgui.NOTIFICATION_ERROR, 5000)
def showInfoNotification(message):
    xbmcgui.Dialog().notification("UptoRay", message, xbmcgui.NOTIFICATION_INFO, 15000)

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
    xbmcplugin.setPluginCategory(__handle__, "Choix UptoRay")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("Mettre a jour les icones", 'au_maj', artworkPath + 'icone.png')    
    add_dir("[COLOR deepskyblue]COMPTES PREMIUM ALEATOIRE CLIC ICI[/COLOR]", 'menuKey', artworkPath + 'icone.png')
    add_dir("Choix SKins [COLOR red]U2Pplay HK2[/COLOR] Clic ici", 'hk2', artworkPath + 'icone.png')
    add_dir("Choix SKins [COLOR green]vStream[/COLOR] Clic ici", 'vstream', artworkPath + 'icone.png')
    add_dir("Sauvegarde et restauration", 'save_restor', artworkPath + 'icone.png')
    add_dir("Mise a Jour Database HK2", 'menumajhk2', artworkPath + 'icone.png')
    add_dir("[COLOR red]NETTOYER KODI[/COLOR]", 'nettoye', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

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

# COMPTES PREMIUM ALEATOIRE
def menuKey():
    tabkey = extractAnotpad()
    nb = 0
    ok = False
    while tabkey:
        keyUpto = random.choice(tabkey)
        status, validite = testUptobox(keyUpto)
        if status == "Success":
            showInfoNotification("Notification(Key Upto ok! expire: %s)" %validite)
            ok = True
            break
        else:
            tabkey.remove(keyUpto)
            showErrorNotification("Prevenir Ray key: %s HS" %keyUpto)
            nb += 1
        if nb > 50:
            break
            return
    if ok:
        # config u2play
        try:
            addon = xbmcaddon.Addon("plugin.video.sendtokodiU2P")
            addon.setSetting(id="keyupto", value=keyUpto)
            nb_items = "50"
            addon.setSetting(id="nb_items", value=nb_items)
            thumbnails = "5000"
            addon.setSetting(id="thumbnails", value=thumbnails)
        except Exception as e:
            notice("Erreur HK: " + str(e))
        
        # config vstream
        try:
            addon = xbmcaddon.Addon("plugin.video.vstream")
            cache_v = "8"
            addon.setSetting(id="pastebin_cacheDuration", value=cache_v)
            hoster_uptobox_premium = "true"
            addon.setSetting(id="hoster_uptobox_premium", value=hoster_uptobox_premium)
            hoster_uptobox_mode_default = "2"
            addon.setSetting(id="hoster_uptobox_mode_default", value=hoster_uptobox_mode_default)
            meta_view = "true"
            addon.setSetting(id="meta-view", value=meta_view)
            addon.setSetting(id="hoster_uptobox_token", value=keyUpto)
        except Exception as e:
            notice("Erreur Vstream: " + str(e))
        
        #config catchup
        try:
            addon = xbmcaddon.Addon("plugin.video.catchuptvandmore")
            mail = "rayflix@laposte.net"
            mot2passe = "Mot2passe"
            addon.setSetting(id="nrj.login", value=mail)
            addon.setSetting(id="6play.login", value=mail)
            addon.setSetting(id="rmcbfmplay.login", value=mail)
            addon.setSetting(id="nrj.password", value=mot2passe)
            addon.setSetting(id="6play.password", value=mot2passe)
            addon.setSetting(id="rmcbfmplay.password", value=mot2passe)
        except Exception as e:
            notice("Erreur CatchUp: " + str(e))

        showInfoNotification("Config Comptes ok")

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

# CHOIX SKIN U2PLAY HK2
def hk2():
    #choix skin
    xbmcplugin.setPluginCategory(__handle__, "Choix skin HK2")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR red]u2Play[/COLOR] SKIN LIGHT [COLOR deepskyblue](le + leger)[/COLOR]", 'hk2lite', artworkPath + 'icone.png')
    add_dir("[COLOR red]u2Play[/COLOR] SKIN FULL [COLOR deepskyblue](le + gourmand)[/COLOR]", 'hk2full', artworkPath + 'icone.png')
    add_dir("[COLOR red]u2Play[/COLOR] SKIN KIDS [COLOR deepskyblue](special enfants)[/COLOR]", 'hk2kids', artworkPath + 'icone.png')
    add_dir("[COLOR red]u2Play[/COLOR] SKIN RETRO [COLOR deepskyblue](pour les nostalgiques)[/COLOR]", 'hk2retro', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# CHOIX SKIN VSTREAM
def vstream():
    #skin vstream
    xbmcplugin.setPluginCategory(__handle__, "Choix skin vStream")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR red]Supprimer[/COLOR] les Anciens Codes Past de [COLOR green]vStream[/COLOR] Clic ici (supprime le setting)", 'suppast', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Ajouter[/COLOR] Tous les Codes Past pour [COLOR green]vStream[/COLOR] Clic ici", 'choixpastall', artworkPath + 'icone.png')
    add_dir("Ou [COLOR deepskyblue]Ajouter[/COLOR] un Mix de Codes Past pour [COLOR green]vStream[/COLOR] Clic ici", 'choixpastmix', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]AJOUTER COMPTES PREMIUM ALEATOIRE CLIC ICI[/COLOR]", 'menuKey', artworkPath + 'icone.png')
    add_dir("[COLOR green]vStream[/COLOR] SKIN SUPER LIGHT [COLOR deepskyblue](le encore + leger)[/COLOR]", 'choixskinsuplitev', artworkPath + 'icone.png')
    add_dir("[COLOR green]vStream[/COLOR] SKIN LIGHT [COLOR deepskyblue](le + leger)[/COLOR]", 'choixskinlitev', artworkPath + 'icone.png')
    add_dir("[COLOR green]vStream[/COLOR] SKIN FULL [COLOR deepskyblue](le + gourmand)[/COLOR]", 'choixskinfullv', artworkPath + 'icone.png')
    add_dir("[COLOR green]vStream[/COLOR] SKIN KIDS [COLOR deepskyblue](special enfants)[/COLOR]", 'choixskinkidsv', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)

##############################################

# SUPPRIMER LES ANCIENS CODES PAST
def suppast():
    xbmc.executebuiltin("Notification(OPTION DE VSTREAM,Effacement en cours...)")
    # suppression du setting de vstream
    # nous devrions vérifier si le fichier existe ou non avant de le supprimer.
    if os.path.isfile(xbmc.translatePath('special://home/userdata/addon_data/plugin.video.vstream/settings.xml')):
        os.remove(xbmc.translatePath('special://home/userdata/addon_data/plugin.video.vstream/settings.xml'))
    else:
        print("Impossible de supprimer le fichier car il n'existe pas")
    xbmc.sleep(2000)
    xbmc.executebuiltin("Notification(Setting Vstream,Supprimé...)")

##############################################

# AJOUTER TOUS LES CODES PAST
def importpastall():
    #past all
    addon = xbmcaddon.Addon("plugin.video.vstream")
    meta_view = "true"
    addon.setSetting(id="meta-view", value=meta_view)
    pastebin_id_1 = "GQgyuquo8"
    addon.setSetting(id="pastebin_id_1", value=pastebin_id_1)
    pastebin_id_1_1 = "qNtuqy4w3"
    addon.setSetting(id="pastebin_id_1_1", value=pastebin_id_1_1)
    pastebin_id_1_2 = "6JK958n64"
    addon.setSetting(id="pastebin_id_1_2", value=pastebin_id_1_2)
    pastebin_id_2 = "CuSaw6GX9"
    addon.setSetting(id="pastebin_id_2", value=pastebin_id_2)
    pastebin_id_2_1 = "wud76FvV2"
    addon.setSetting(id="pastebin_id_2_1", value=pastebin_id_2_1)
    pastebin_id_2_2 = "rAYRYTfJ3"
    addon.setSetting(id="pastebin_id_2_2", value=pastebin_id_2_2)
    pastebin_id_3 = "yaA3sIezf"
    addon.setSetting(id="pastebin_id_3", value=pastebin_id_3)
    pastebin_id_3_1 = "V98AXTbyc"
    addon.setSetting(id="pastebin_id_3_1", value=pastebin_id_3_1)
    pastebin_id_4 = "cZEyUDCnb"
    addon.setSetting(id="pastebin_id_4", value=pastebin_id_4)
    pastebin_id_4_1 = "19kQJVf4f"
    addon.setSetting(id="pastebin_id_4_1", value=pastebin_id_4_1)
    pastebin_id_5 = "y3duNqoM1"
    addon.setSetting(id="pastebin_id_5", value=pastebin_id_5)
    pastebin_id_6 = "0cwaTCkid"
    addon.setSetting(id="pastebin_id_6", value=pastebin_id_6)
    pastebin_id_7 = "vyMOtqrNf"
    addon.setSetting(id="pastebin_id_7", value=pastebin_id_7)
    pastebin_id_7_1 = "7FjFI8FJ4"
    addon.setSetting(id="pastebin_id_7_1", value=pastebin_id_7_1)
    pastebin_id_8 = "fxPLhFDe5"
    addon.setSetting(id="pastebin_id_8", value=pastebin_id_8)
    pastebin_id_9 = "2Vc6sZW21"
    addon.setSetting(id="pastebin_id_9", value=pastebin_id_9)
    pastebin_label_1 = "1 Films"
    addon.setSetting(id="pastebin_label_1", value=pastebin_label_1)
    pastebin_label_2 = "2 Series"
    addon.setSetting(id="pastebin_label_2", value=pastebin_label_2)
    pastebin_label_3 = "3 Dessin Animes"
    addon.setSetting(id="pastebin_label_3", value=pastebin_label_3)
    pastebin_label_4 = "4 Docs"
    addon.setSetting(id="pastebin_label_4", value=pastebin_label_4)
    pastebin_label_5 = "5 Concert"
    addon.setSetting(id="pastebin_label_5", value=pastebin_label_5)
    pastebin_label_6 = "6 Spectacle"
    addon.setSetting(id="pastebin_label_6", value=pastebin_label_6)
    pastebin_label_7 = "7 Animés"
    addon.setSetting(id="pastebin_label_7", value=pastebin_label_7)
    pastebin_label_8 = "8 Sport"
    addon.setSetting(id="pastebin_label_8", value=pastebin_label_8)
    pastebin_label_9 = "9 Adultes"
    addon.setSetting(id="pastebin_label_9", value=pastebin_label_9)
    pastebin_id_10 = "bE9gqAb10"
    addon.setSetting(id="pastebin_id_10", value=pastebin_id_10)
    pastebin_id_11 = "pnm949oQ3"
    addon.setSetting(id="pastebin_id_11", value=pastebin_id_11)
    pastebin_id_12 = "hEAy2BsY0"
    addon.setSetting(id="pastebin_id_12", value=pastebin_id_12)
    pastebin_id_13 = "5XBJXBI80"
    addon.setSetting(id="pastebin_id_13", value=pastebin_id_13)
    pastebin_label_10 = "widget films"
    addon.setSetting(id="pastebin_label_10", value=pastebin_label_10)
    pastebin_label_11 = "widget series"
    addon.setSetting(id="pastebin_label_11", value=pastebin_label_11)
    pastebin_label_12 = "widget docs"
    addon.setSetting(id="pastebin_label_12", value=pastebin_label_12)
    pastebin_label_13 = "widgets dessin animé"
    addon.setSetting(id="pastebin_label_13", value=pastebin_label_13)
    pastebin_nbItemParPage = "30"
    addon.setSetting(id="pastebin_nbItemParPage", value=pastebin_nbItemParPage)
    showInfoNotification("Ajout Past All ok")

##############################################

# AJOUTER UN MIX DE CODES PAST
def importpastmix():
    #past Mix
    addon = xbmcaddon.Addon("plugin.video.vstream")
    meta_view = "true"
    addon.setSetting(id="meta-view", value=meta_view)
    pastebin_id_1 = "txDUtOdte"
    addon.setSetting(id="pastebin_id_1", value=pastebin_id_1)
    pastebin_id_1_1 = "qsJ1OBfk4"
    addon.setSetting(id="pastebin_id_1_1", value=pastebin_id_1_1)
    pastebin_id_1_2 = "8oEErrWMe"
    addon.setSetting(id="pastebin_id_1_2", value=pastebin_id_1_2)
    pastebin_id_2 = "pVuIECFkc"
    addon.setSetting(id="pastebin_id_2", value=pastebin_id_2)
    pastebin_id_2_1 = "V0I1z8qAd"
    addon.setSetting(id="pastebin_id_2_1", value=pastebin_id_2_1)
    pastebin_id_2_2 = "sDZaHTsPd"
    addon.setSetting(id="pastebin_id_2_2", value=pastebin_id_2_2)
    pastebin_id_3 = "2KicsN7Le"
    addon.setSetting(id="pastebin_id_3", value=pastebin_id_3)
    pastebin_id_3_1 = "8IAzteea1"
    addon.setSetting(id="pastebin_id_3_1", value=pastebin_id_3_1)
    pastebin_id_4 = "I3UK5AW70"
    addon.setSetting(id="pastebin_id_4", value=pastebin_id_4)
    pastebin_id_4_1 = "qKh2NIJoc"
    addon.setSetting(id="pastebin_id_4_1", value=pastebin_id_4_1)
    pastebin_id_5 = "w7wG1JDca"
    addon.setSetting(id="pastebin_id_5", value=pastebin_id_5)
    pastebin_id_6 = "KXFQXaIQ0"
    addon.setSetting(id="pastebin_id_6", value=pastebin_id_6)
    pastebin_id_7 = "WpwoNm177"
    addon.setSetting(id="pastebin_id_7", value=pastebin_id_7)
    pastebin_id_7_1 = "W9Ozl7nXb"
    addon.setSetting(id="pastebin_id_7_1", value=pastebin_id_7_1)
    pastebin_id_8 = "fxPLhFDe5"
    addon.setSetting(id="pastebin_id_8", value=pastebin_id_8)
    pastebin_id_9 = "2Vc6sZW21"
    addon.setSetting(id="pastebin_id_9", value=pastebin_id_9)
    pastebin_label_1 = "1 Films"
    addon.setSetting(id="pastebin_label_1", value=pastebin_label_1)
    pastebin_label_2 = "2 Series"
    addon.setSetting(id="pastebin_label_2", value=pastebin_label_2)
    pastebin_label_3 = "3 Dessin Animes"
    addon.setSetting(id="pastebin_label_3", value=pastebin_label_3)
    pastebin_label_4 = "4 Docs"
    addon.setSetting(id="pastebin_label_4", value=pastebin_label_4)
    pastebin_label_5 = "5 Concert"
    addon.setSetting(id="pastebin_label_5", value=pastebin_label_5)
    pastebin_label_6 = "6 Spectacle"
    addon.setSetting(id="pastebin_label_6", value=pastebin_label_6)
    pastebin_label_7 = "7 Animés"
    addon.setSetting(id="pastebin_label_7", value=pastebin_label_7)
    pastebin_label_8 = "8 Sport"
    addon.setSetting(id="pastebin_label_8", value=pastebin_label_8)
    pastebin_label_9 = "9 Adultes"
    addon.setSetting(id="pastebin_label_9", value=pastebin_label_9)
    pastebin_id_10 = "bE9gqAb10"
    addon.setSetting(id="pastebin_id_10", value=pastebin_id_10)
    pastebin_id_11 = "pnm949oQ3"
    addon.setSetting(id="pastebin_id_11", value=pastebin_id_11)
    pastebin_id_12 = "hEAy2BsY0"
    addon.setSetting(id="pastebin_id_12", value=pastebin_id_12)
    pastebin_id_13 = "5XBJXBI80"
    addon.setSetting(id="pastebin_id_13", value=pastebin_id_13)
    pastebin_label_10 = "widget films"
    addon.setSetting(id="pastebin_label_10", value=pastebin_label_10)
    pastebin_label_11 = "widget series"
    addon.setSetting(id="pastebin_label_11", value=pastebin_label_11)
    pastebin_label_12 = "widget docs"
    addon.setSetting(id="pastebin_label_12", value=pastebin_label_12)
    pastebin_label_13 = "widgets dessin animé"
    addon.setSetting(id="pastebin_label_13", value=pastebin_label_13)
    pastebin_nbItemParPage = "30"
    addon.setSetting(id="pastebin_nbItemParPage", value=pastebin_nbItemParPage)
    showInfoNotification("Ajout Past Mix ok")

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
    xbmcplugin.setPluginCategory(__handle__, "Sauvegarde et restauration")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR deepskyblue]1 CREER UNE SAUVEGARDE : [/COLOR]", 'skin_save1', artworkPath + 'icone.png')
    add_dir("Emplacement 1", 'skin_save1', artworkPath + 'icone.png')
    add_dir("Emplacement 2", 'skin_save2', artworkPath + 'icone.png')
    add_dir("Emplacement 3", 'skin_save3', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]2 RESTAURER UNE SAUVEGARDE : [/COLOR]", 'skin_restor1', artworkPath + 'icone.png')
    add_dir("Emplacement 1", 'skin_restor1', artworkPath + 'icone.png')
    add_dir("Emplacement 2", 'skin_restor2', artworkPath + 'icone.png')
    add_dir("Emplacement 3", 'skin_restor3', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

##############################################

# SAUVEGARDE
def skin_save1():
    xbmc.executebuiltin("Notification(PREPARATION DES FICHIERS,Copie en cours...)")
    # COPIE DES DOSSIERS ET FICHIERS DU SKIN
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/skin.project.aura')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addon_data/skin.project.aura')
    source_dir1 = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
    destination_dir1 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addon_data/script.skinshortcuts')
    source_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    destination_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    shutil.copy(source_dir2, destination_dir2)
    # CREATION ARCHIVE ZIP
    shutil.make_archive((xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/Skin_save1')),'zip',(xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1')))
    xbmc.executebuiltin("Notification(SKIN SAUVEGARDE, Archive ZIP créée !)")
    sys.exit()

def skin_save2():
    xbmc.executebuiltin("Notification(PREPARATION DES FICHIERS,Copie en cours...)")
    # COPIE DES DOSSIERS ET FICHIERS DU SKIN
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/skin.project.aura')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data/skin.project.aura')
    source_dir1 = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
    destination_dir1 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data/script.skinshortcuts')
    source_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    destination_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    shutil.copy(source_dir2, destination_dir2)
    # CREATION ARCHIVE ZIP
    shutil.make_archive((xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/Skin_save1')),'zip',(xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2')))
    xbmc.executebuiltin("Notification(SKIN SAUVEGARDE, Archive ZIP créée !)")
    sys.exit()

def skin_save3():
    xbmc.executebuiltin("Notification(PREPARATION DES FICHIERS,Copie en cours...)")
    # COPIE DES DOSSIERS ET FICHIERS DU SKIN
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/skin.project.aura')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addon_data/skin.project.aura')
    source_dir1 = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
    destination_dir1 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addon_data/script.skinshortcuts')
    source_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    destination_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addons/skin.project.aura/1080i/script-skinshortcuts-includes.xml')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir1, destination_dir1, dirs_exist_ok=True)
    shutil.copy(source_dir2, destination_dir2)
    # CREATION ARCHIVE ZIP
    shutil.make_archive((xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/Skin_save1')),'zip',(xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3')))
    xbmc.executebuiltin("Notification(SKIN SAUVEGARDE, Archive ZIP créée !)")
    sys.exit()

##############################################

# RESTAURATION
def skin_restor1():
    # copie des fichiers sauvegarde
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addon_data')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/1/addons/skin.project.aura')
    destination_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(COPIE OK,Mise à jour effectuée !)")
    xbmc.sleep(5000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ACTUALISATION DU SKIN, Skin Save 1...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    sys.exit()

def skin_restor2():
    # copie des fichiers sauvegarde
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addon_data')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/2/addons/skin.project.aura')
    destination_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura')
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
    # copie des fichiers sauvegarde
    source_dir = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addon_data')
    destination_dir = xbmc.translatePath('special://home/userdata/addon_data')
    source_dir2 = xbmc.translatePath('special://home/userdata/addon_data/Scripts/Skin_save/3/addons/skin.project.aura')
    destination_dir2 = xbmc.translatePath('special://home/addons/skin.project.aura')
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    shutil.copytree(source_dir2, destination_dir2, dirs_exist_ok=True)
    xbmc.executebuiltin("Notification(COPIE OK,Mise à jour effectuée !)")
    xbmc.sleep(5000)
    # actualisation du skin
    xbmc.executebuiltin("Notification(ACTUALISATION DU SKIN, Skin Save 3...)")
    xbmc.sleep(2000)
    xbmc.executebuiltin('ReloadSkin')
    sys.exit()

##############################################

# MENU MAJ DATABASE
def menumajhk2():
    # menu maj
    xbmcplugin.setPluginCategory(__handle__, "Mise a Jour Database HK2")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR deepskyblue]1 - Forcer Mise a jour[/COLOR]", 'forcermaj', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]2 - Actualiser Skin[/COLOR]", 'actuskin', artworkPath + 'icone.png')
    add_dir("[COLOR red]En cas de soucis [/COLOR][COLOR deepskyblue]CHANGER COMPTES PREMIUM ALEATOIRE[/COLOR]", 'menuKey', artworkPath + 'icone.png')
    add_dir("--- [COLOR green]Clic ci dessous pour changer de skin[/COLOR] ---", 'hk2lite', artworkPath + 'icone.png')
    add_dir("SKIN LIGHT [COLOR deepskyblue](le + leger)[/COLOR]", 'hk2lite', artworkPath + 'icone.png')
    add_dir("SKIN FULL [COLOR deepskyblue](le + gourmand)[/COLOR]", 'hk2full', artworkPath + 'icone.png')
    add_dir("SKIN KIDS [COLOR deepskyblue](special enfants)[/COLOR]", 'hk2kids', artworkPath + 'icone.png')
    add_dir("SKIN RETRO [COLOR deepskyblue](pour les nostalgiques)[/COLOR]", 'hk2retro', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

def forcermaj():
    # forcer maj
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.sendtokodiU2P/?action=majHkNew)')
    
def actuskin():
    # actualiser 
    xbmc.executebuiltin("Notification(actualisation OK,Faites retour !)")
    xbmc.sleep(1000)
    xbmc.executebuiltin('ReloadSkin')

##############################################

# MENU NETTOYAGE
def nettoye():
    #menu nettoyage
    xbmcplugin.setPluginCategory(__handle__, "NETTOYER KODI")
    xbmcplugin.setContent(__handle__, 'files')
    add_dir("[COLOR red]NETTOYER TOUT D'UN COUP : [/COLOR]clic ici", 'vider_cache', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Vider Cache uniquement[/COLOR]", 'cache_seul', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Vider Tmp uniquement[/COLOR]", 'tmp_seul', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Vider Packages uniquement[/COLOR]", 'package_seul', artworkPath + 'icone.png')
    add_dir("[COLOR deepskyblue]Vider Thumbnails uniquement[/COLOR]", 'thumb_seul', artworkPath + 'icone.png')
    xbmcplugin.endOfDirectory(handle=__handle__, succeeded=True)  

##############################################

# NETTOYER TOUT D UN COUP
def vider_cache():
    #nettoyer tout
    xbmc.executebuiltin("Notification(FICHIER TEMP,Effacement en cours...)")
    # suppression dossier temporaire
    dirPath = xbmc.translatePath('special://home/temp/temp/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(DOSSIER PACKAGES,Effacement en cours...)")
    # suppression dossier packages
    dirPath = xbmc.translatePath('special://home/addons/packages/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(DOSSIER THUMBNAILS,Effacement en cours...)")
    # suppression dossier thumbnails
    dirPath = xbmc.translatePath('special://home/userdata/Thumbnails/')
    try:
       shutil.rmtree(dirPath)
    except:
       print('Error while deleting directory')
    xbmc.sleep(1000)
    xbmc.executebuiltin("Notification(CACHE TEMP,Effacement en cours...)")
    # suppression dossier cache
    dirPath = xbmc.translatePath('special://home/cache/temp/')
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
    dirPath = xbmc.translatePath('special://home/cache/temp/')
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
    dirPath = xbmc.translatePath('special://home/temp/temp/')
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
    dirPath = xbmc.translatePath('special://home/addons/packages/')
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
    dirPath = xbmc.translatePath('special://home/userdata/Thumbnails/')
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

def router(paramstring):
    params = dict(parse_qsl(paramstring))    
    dictActions = {
        #key uptobox
        'menuKey':(menuKey, ""),
        #skin
        'choixpastmix': (importpastmix, ""),
        'choixpastall': (importpastall, ""),
        'choixskinsuplitev': (importSkin, 'https://github.com/prf2/pack/raw/kodi/v_super_lite.zip'),
        'choixskinlitev': (importSkin, 'https://github.com/prf2/pack/raw/kodi/v_light.zip'),
        'choixskinfullv': (importSkin, 'https://github.com/prf2/pack/raw/kodi/v_full.zip'),
        'choixskinkidsv': (importSkin, 'https://github.com/prf2/pack/raw/kodi/v_kids.zip'),
        'hk2lite': (importSkin, 'http://kodi.prf2.ovh/pack/hk2_light.zip'),
        'hk2full': (importSkin, 'http://kodi.prf2.ovh/pack/hk2_full.zip'),
        'hk2kids': (importSkin, 'http://kodi.prf2.ovh/pack/hk2_kids.zip'),
        'hk2retro': (importSkin, 'http://kodi.prf2.ovh/pack/hk2_retro.zip'),
        #skin hk
        'hk2': (hk2, ""),
        #skin vstream
        "suppast": (suppast, ""),
        "vstream": (vstream, ""),
        #maj hk2
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
        'skin_save1': (skin_save1, ""), 
        'skin_save2': (skin_save2, ""), 
        'skin_save3': (skin_save3, ""), 
        'skin_restor1': (skin_restor1, ""), 
        'skin_restor2': (skin_restor2, ""), 
        'skin_restor3': (skin_restor3, ""), 
        #autres
        #'ad_maj2': (ad_maj2, ""),
        'au_maj': (au_maj, ""),
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
    __addon__ = xbmcaddon.Addon("plugin.program.skinrayflix")
    __handle__ = int(sys.argv[1])
    router(sys.argv[2][1:])