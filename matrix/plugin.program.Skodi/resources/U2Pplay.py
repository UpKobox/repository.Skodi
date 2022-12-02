import xbmc
import time

xbmc.executebuiltin("Notification(Chargement HK2...,,2000)")
xbmc.sleep(2000)
xbmc.executebuiltin('PlayMedia("plugin://plugin.video.sendtokodiU2P/?action=majhkneww")')
xbmc.executebuiltin( "Notification(HK2 OK...,,2000)" )
time.sleep(10)
xbmc.executebuiltin( 'ReloadSkin()' )
xbmc.executebuiltin( "Notification(Rafraichissement Skin,,2000)" )