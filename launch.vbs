' Guitar Tuner Web - VBS Launcher Wrapper
' This script launches the batch file in a visible, non-closeable window

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Run the batch file in a command window that stays open
objShell.Run "cmd /k """ & scriptDir & "\run.bat""", 1, False
