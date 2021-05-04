function Show-Menu {
    param (
        [string]$Title = 'Kaopy Boilerplate'
    )
    Clear-Host
    Write-Host "================ $Title ================"
    
    Write-Host "1: Press '1' for Setup Python Virtual Env."
    Write-Host "2: Press '2' for Clear Python Virtual Env."
    Write-Host "3: Press '3' for Activate Python Virlual Env."
    Write-Host "4: Press '4' for Install Requirement."
    Write-Host "Q: Press 'Q' to quit."
}


function SetUpPythonEnv {
    python -m venv .
}

function ClearPythonEnv {
    if ((Get-Item .\env).Exists) {
        Remove-Item -Path .\env -Force
    }
}
function ClearPythonEnvEachPath {
    if ((Get-Item .\Lib).Exists) {
        Remove-Item -Path .\Lib  -Force
    }
    if ((Get-Item .\Include).Exists) {
        Remove-Item -Path .\Include  -Force
    }
 
    if ((Get-Item .\Scripts).Exists) {
        Remove-Item -Path .\Scripts  -Force
    }
}

function ActivatePythonEnv {
    .\Scripts\Activate.ps1
}
function RequirementsInstall {
    ActivatePythonEnv
    pip install -r requirements.txt
}

do {
    Show-Menu
    $selection = Read-Host "Please make a selection"
    switch ($selection) {
        '1' {
            SetUpPythonEnv
        } '2' {
            ClearPythonEnvEachPath
        } '3' {
            ActivatePythonEnv
        }
        '4' {
            RequirementsInstall
        }
    }
    pause
}
until ($selection -eq 'q')
