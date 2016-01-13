taskkill /IM ArcMap.exe
makeaddin.py
for %%f in (*.esriaddin) do (

            %%f
    )
start "" "C:\Program Files (x86)\ArcGIS\Desktop10.3\bin\ArcMap.exe"
exit
