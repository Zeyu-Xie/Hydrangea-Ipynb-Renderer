
Outfile "Jupyrender_Setup-0.1.0-Windows-x64.exe"
InstallDir "$PROGRAMFILES\Jupyrender"
ShowInstDetails show
InstallDirRegKey HKCU "Software\Jupyrender" "Install_Dir"

Section "Install"
    SetOutPath $INSTDIR
    File /r "dist\Jupyrender\*"
    WriteRegStr HKCU "Software\Jupyrender" "Install_Dir" "$INSTDIR"
    CreateShortcut "$DESKTOP\Jupyrender.lnk" "$INSTDIR\Jupyrender.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\Jupyrender.exe"
    Delete "$INSTDIR\config.yaml"
    Delete "$INSTDIR\src\css\*"
    RMDir "$INSTDIR\src\css"
    RMDir "$INSTDIR"
    Delete "$DESKTOP\Jupyrender.lnk"
    DeleteRegKey HKCU "Software\Jupyrender"
SectionEnd
