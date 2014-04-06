!include "MUI2.nsh"

Name "APP_NAME VERSION_NAME"
OutFile "OUT_FILE_NAME"

InstallDir "$PROGRAMFILES\DOManager"
InstallDirRegKey HKLM "Software\DOManager" "Install_Dir"

RequestExecutionLevel admin

SetCompressor /SOLID lzma
SetCompressorDictSize 10

BrandingText "Aoizora Org"

!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_FUNCTION RunDO
!define MUI_BUTTONTEXT_FINISH      "Finish"
!define MUI_TEXT_FINISH_INFO_TITLE "Installation complete"
!define MUI_TEXT_FINISH_RUN        "Launch DO Manager"

!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Icon "source\domanager\resources\main_logo_color.ico"

Function RunDO
  SetOutPath $INSTDIR
  Exec '"$INSTDIR\domanager.exe"'
	loop:
	    System::Call user32::GetForegroundWindow()i.r0
	    Sleep 200
	    IntCmpU $0 $hwndparent loop
  SetErrorLevel 0
FunctionEnd

Function .onInit
  nsExec::Exec "taskkill.exe /F /IM domanager.exe"
  nsExec::Exec "taskkill.exe /F /IM domanager.exe"
  nsExec::Exec "taskkill.exe /F /IM domanager.exe"
  FindProcDLL::FindProc "domanager.exe"
  IntCmp $R0 1 0 notRunning
    nsExec::Exec "taskkill.exe /F /IM domanager.exe"
    Goto notRunning
  notRunning:
FunctionEnd

Section "APP_NAME VERSION_NAME" InstSection

  RMDir /r "$INSTDIR\*.*"
  RMDir "$INSTDIR"

  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DOManager"
  DeleteRegKey HKLM SOFTWARE\DOManager

  SectionIn RO
  SetOutPath $INSTDIR
  File "domanager.nsi"
  File /r "DIST_DIR\*.*"

  WriteRegStr HKLM SOFTWARE\DOManager "Install_Dir" "$INSTDIR"

  ; Write the uninstall keys for Windows
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DOManager" "DisplayName" "APP_NAME VERSION_NAME"
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DOManager" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DOManager" "QuietUninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DOManager" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DOManager" "NoRepair" 1
  WriteUninstaller "uninstall.exe"

  ExecWait '"$INSTDIR\vcredist_2008_x86.exe" /qn+'
  SetErrorLevel 0

SectionEnd

Section "Start menu shortcuts" s2

  CreateDirectory "$SMPROGRAMS\APP_NAME"
  CreateShortCut  "$SMPROGRAMS\APP_NAME\Uninstall APP_NAME.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut  "$SMPROGRAMS\APP_NAME\APP_NAME.lnk" "$INSTDIR\domanager.exe" "" "$INSTDIR\\resources\main_logo_color.ico" 0

SectionEnd

Section "Desktop shortcut" s3

  CreateShortCut "$DESKTOP\APP_NAME.lnk" "$INSTDIR\domanager.exe" "" "$INSTDIR\\resources\main_logo_color.ico" 0

SectionEnd

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${InstSection} "The program core and main components (required)"
  !insertmacro MUI_DESCRIPTION_TEXT ${s2} "Shortcuts for the Start Menu"
  !insertmacro MUI_DESCRIPTION_TEXT ${s3} "Shortcut to run program from the Desktop"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

Section "Uninstall"

  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DOManager"
  DeleteRegKey HKLM SOFTWARE\DOManager

  RMDir /r "$INSTDIR\*.*"
  RMDir "$INSTDIR"

  Delete "$DESKTOP\APP_NAME.lnk"
  Delete "$SMPROGRAMS\APP_NAME\*.*"
  RMDir  "$SMPROGRAMS\APP_NAME"

  SetErrorLevel 0

SectionEnd