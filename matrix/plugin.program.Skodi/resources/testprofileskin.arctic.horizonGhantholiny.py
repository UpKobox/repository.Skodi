import xbmc
xbmc.executebuiltin('RunPlugin(plugin://plugin.program.Skodi/?action=GhantholinyAH)')
xbmc.sleep(1000)
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.estuary"}}')
xbmc.sleep(100)
xbmc.executebuiltin('SendClick(11)')
xbmc.sleep(100)
xbmc.executebuiltin('System.Logoff()')
xbmc.sleep(100)
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.arctic.horizon"}}')
xbmc.sleep(100)
xbmc.executebuiltin('SendClick(11)')