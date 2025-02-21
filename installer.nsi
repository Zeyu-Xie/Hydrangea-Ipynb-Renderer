
Outfile "Jupyrender_Setup-0.1.0-Windows-x64.exe"
InstallDir "$PROGRAMFILES\Jupyrender"
ShowInstDetails show
InstallDirRegKey HKCU "Software\Jupyrender" "Install_Dir"

Section "Install"
    SetOutPath $INSTDIR
    File /r "dist\Jupyrender\*"
    WriteRegStr HKCU "Software\Jupyrender" "Install_Dir" "$INSTDIR"
    CreateShortcut "$DESKTOP\Jupyrender.lnk" "$INSTDIR\Jupyrender.exe"
    SetOutPath "$APPDATA\Jupyrender"
    CreateDirectory "$APPDATA\Jupyrender"
    File "dist\Jupyrender\_internal\config.yaml"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\Jupyrender.exe"
    Delete "$INSTDIR\config.yaml"
    Delete "$INSTDIR\src\css\*"
    RMDir "$INSTDIR\src\css"
    RMDir "$INSTDIR"
    Delete "$DESKTOP\Jupyrender.lnk"
    RMDir "$APPDATA\Jupyrender"
    DeleteRegKey HKCU "Software\Jupyrender"
SectionEnd
