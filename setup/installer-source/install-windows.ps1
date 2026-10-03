#Requires -Version 5.1

<#
.SYNOPSIS
Sets up a Windows computer for the Project Syncere Python course.

.DESCRIPTION
Installs Python 3.12, Git, Visual Studio Code, and the VS Code Python
extension. It then clones or updates the course repository, creates its
virtual environment, installs course packages, verifies Python, and opens
the repository in Visual Studio Code.
#>

[CmdletBinding()]
param(
    [string]$CourseDirectory = (Join-Path ([Environment]::GetFolderPath("MyDocuments")) "project-syncere-cs-2027"),
    [switch]$SkipSoftwareInstall,
    [switch]$SkipCourseEnvironment,
    [switch]$DoNotOpenVSCode
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$repositoryUrl = "https://github.com/lhernandez-sudo/project-syncere-cs-2027.git"

function Write-Step {
    param([Parameter(Mandatory)][string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Refresh-ProcessPath {
    $machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = "$machinePath;$userPath"
}

function Test-WingetPackage {
    param([Parameter(Mandatory)][string]$Id)
    & winget list --id $Id --exact --accept-source-agreements *> $null
    return $LASTEXITCODE -eq 0
}

function Install-WingetPackage {
    param(
        [Parameter(Mandatory)][string]$Id,
        [Parameter(Mandatory)][string]$Name
    )

    if (Test-WingetPackage -Id $Id) {
        Write-Host "$Name is already installed." -ForegroundColor Green
        return
    }

    Write-Host "Installing $Name..."
    & winget install --id $Id --exact --silent --accept-source-agreements --accept-package-agreements
    if ($LASTEXITCODE -ne 0) {
        throw "$Name could not be installed. winget exit code: $LASTEXITCODE"
    }
}

function Find-VSCodeCommand {
    $command = Get-Command code -ErrorAction SilentlyContinue
    if ($null -ne $command) {
        return $command.Source
    }

    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin\code.cmd",
        "$env:ProgramFiles\Microsoft VS Code\bin\code.cmd"
    )
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }
    return $null
}

function Find-RepositoryRoot {
    $scriptRepository = Split-Path -Parent $PSScriptRoot
    if ((Test-Path (Join-Path $scriptRepository "requirements.txt")) -and
        (Test-Path (Join-Path $scriptRepository ".git"))) {
        return $scriptRepository
    }
    return $CourseDirectory
}

Write-Host "Project Syncere - Windows Python Setup" -ForegroundColor DarkCyan
Write-Host "This may take several minutes. Windows may ask you to approve an installation."

if (-not $SkipSoftwareInstall) {
    Write-Step "Checking the Windows package manager"
    if ($null -eq (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "winget was not found. Install App Installer from the Microsoft Store, then run this setup again."
    }

    Write-Step "Installing required software"
    Install-WingetPackage -Id "Python.Python.3.12" -Name "Python 3.12"
    Install-WingetPackage -Id "Git.Git" -Name "Git"
    Install-WingetPackage -Id "Microsoft.VisualStudioCode" -Name "Visual Studio Code"
    Refresh-ProcessPath
}

if ($null -eq (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not available. Restart Windows, then run Start-Setup.bat again."
}

$repositoryRoot = Find-RepositoryRoot
$gitDirectory = Join-Path $repositoryRoot ".git"
if (Test-Path -LiteralPath $gitDirectory) {
    Write-Step "Updating the course repository"
    & git -C $repositoryRoot pull --ff-only
    if ($LASTEXITCODE -ne 0) {
        throw "The course repository could not be updated. Ask the instructor to check this computer."
    }
} elseif (Test-Path -LiteralPath $repositoryRoot) {
    $existingItems = @(Get-ChildItem -LiteralPath $repositoryRoot -Force)
    if ($existingItems.Count -gt 0) {
        throw "The course folder already exists but is not a Git repository: $repositoryRoot"
    }

    Write-Step "Cloning the course repository"
    & git clone $repositoryUrl $repositoryRoot
    if ($LASTEXITCODE -ne 0) { throw "The course repository could not be cloned." }
} else {
    Write-Step "Cloning the course repository"
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $repositoryRoot) | Out-Null
    & git clone $repositoryUrl $repositoryRoot
    if ($LASTEXITCODE -ne 0) { throw "The course repository could not be cloned." }
}

Write-Step "Installing the Visual Studio Code Python extension"
$codeCommand = Find-VSCodeCommand
if ($null -eq $codeCommand) {
    Write-Warning "The VS Code command was not found. Restart Windows and run Start-Setup.bat again."
} else {
    & $codeCommand --install-extension ms-python.python --force
    if ($LASTEXITCODE -ne 0) { throw "The VS Code Python extension could not be installed." }
}

if (-not $SkipCourseEnvironment) {
    Write-Step "Creating the course Python environment"
    if ($null -eq (Get-Command py -ErrorAction SilentlyContinue)) {
        throw "The Python launcher is not available. Restart Windows and run Start-Setup.bat again."
    }

    $requirementsPath = Join-Path $repositoryRoot "requirements.txt"
    $verificationPath = Join-Path $repositoryRoot "setup\verify_setup.py"
    if (-not (Test-Path -LiteralPath $requirementsPath)) {
        throw "requirements.txt is missing from the course repository."
    }

    $virtualEnvironment = Join-Path $repositoryRoot ".venv"
    $virtualPython = Join-Path $virtualEnvironment "Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $virtualPython)) {
        & py -3.12 -m venv $virtualEnvironment
        if ($LASTEXITCODE -ne 0) { throw "The course virtual environment could not be created." }
    } else {
        Write-Host "The course virtual environment already exists." -ForegroundColor Green
    }

    & $virtualPython -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw "pip could not be updated." }
    & $virtualPython -m pip install -r $requirementsPath
    if ($LASTEXITCODE -ne 0) { throw "The course Python packages could not be installed." }

    Write-Step "Verifying Python"
    & $virtualPython $verificationPath
    if ($LASTEXITCODE -ne 0) { throw "The Python verification check failed." }
}

Write-Host "`nSetup complete." -ForegroundColor Green
Write-Host "Course folder: $repositoryRoot"
Write-Host "Keep this window open if you need to show the result to your instructor."

if ((-not $DoNotOpenVSCode) -and ($null -ne $codeCommand)) {
    Write-Step "Opening the course in Visual Studio Code"
    & $codeCommand $repositoryRoot
}
