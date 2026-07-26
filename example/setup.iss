[Setup]
AppId={{YOUR-UNIQUE-GUID-HERE}}
AppName=AutoUpdateApp
AppVersion=1.0.1
DefaultDirName={autopf}\AutoUpdateApp
DefaultGroupName=AutoUpdateApp
OutputDir=.
OutputBaseFilename=mysetup
Compression=lzma
SolidCompression=yes
; Crucial flags to allow updater to close old version safely:
CloseApplications=yes
RestartApplications=yes

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AutoUpdateApp"; Filename: "{app}\app.exe"
Name: "{autodesktop}\AutoUpdateApp"; Filename: "{app}\app.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
