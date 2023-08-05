""" Finds any disconnected terminal service sessions and logs them off"""
import win32ts
sessions = win32ts.WTSEnumerateSessions(win32ts.WTS_CURRENT_SERVER_HANDLE)
for session in sessions:
    """
    WTS_CONNECTSTATE_CLASS: WTSActive,WTSConnected,WTSConnectQuery,WTSShadow,WTSDisconnected,
          WTSIdle,WTSListen,WTSReset,WTSDown,WTSInit
    """
    if session['State'] == win32ts.WTSDisconnected:
        sessionid = session['SessionId']
        username = win32ts.WTSQuerySessionInformation(
            win32ts.WTS_CURRENT_SERVER_HANDLE, sessionid, win32ts.WTSUserName)
        print('Logging off disconnected user:', username)
        win32ts.WTSLogoffSession(
            win32ts.WTS_CURRENT_SERVER_HANDLE, sessionid, True)
