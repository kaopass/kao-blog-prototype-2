function Show-Menu
{
    param (
        [string]$Title = 'Kaopy Boilerplate'
    )
    Clear-Host
    Write-Host "================ $Title ================"

    Write-Host "1: Press '1' for Setup Python Virtual Env."
    Write-Host "2: Press '2' for Clear Python Virtual Env."
    Write-Host "3: Press '3' for Activate Python Virlual Env."
    Write-Host "4: Press '4' for Install Requirement."
    Write-Host "5: Press '5' for start Django server."
    Write-Host "6: Press '6' for migrate data."
    Write-Host "7: Press '7' for make migration."
    Write-Host "8: Press '8' for Create super user."
    Write-Host "9: Press '9' Dump authenticate data."
    Write-Host "10: Press '10' Dump sessions data."
    Write-Host "11: Press '11' Dump section data."


    Write-Host "Q: Press 'Q' to quit."
}


function SetUpPythonEnv
{
    python -m venv .
}

function ClearPythonEnv
{
    if ((Get-Item .\env).Exists)
    {
        Remove-Item -Path .\env -Force
    }
}
function ClearPythonEnvEachPath
{
    if ((Get-Item .\Lib).Exists)
    {
        Remove-Item -Path .\Lib  -Force
    }
    if ((Get-Item .\Include).Exists)
    {
        Remove-Item -Path .\Include  -Force
    }

    if ((Get-Item .\Scripts).Exists)
    {
        Remove-Item -Path .\Scripts  -Force
    }
}

function ActivatePythonEnv
{
    .\Scripts\Activate.ps1
}

function RequirementsInstall
{
    ActivatePythonEnv
    pip install -r requirements.txt
    pip list
}

do
{
    echo $1
    Show-Menu
    $selection = Read-Host "Please make a selection"
    switch ($selection)
    {
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
        '5' {
            py .\manage.py migrate --run-syncdb
            py .\manage.py runserver 8080
        }
        '6' {
            py .\manage.py migrate
        }
        '7' {
            py .\manage.py makemigrations
        }
        '8' {
            py .\manage.py createsuperuser
        }
          '9' {
            py  .\manage.py dumpdata --indent=2 auth > initial_data.json
        }
          '10' {
            py .\manage.py dumpdata --indent=2 sessions
        }
          '11' {
             py .\manage.py migrate --run-syncdb
        }
    }
    pause
}
until ($selection -eq 'q')
