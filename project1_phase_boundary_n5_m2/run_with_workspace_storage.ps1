param([Parameter(Mandatory=$true)][string]$Python,[Parameter(Mandatory=$true)][string]$Script,[string[]]$ScriptArguments=@())
$workspaceStorage = 'D:/Study/PHD UIUC/LLM project/algoverse'
$storageDirectories = @('tmp','cache/huggingface','cache/torch','cache/matplotlib','cache/pip','cache/uv','cache/xdg')
foreach ($storageDirectory in $storageDirectories) { New-Item -ItemType Directory -Path (Join-Path $workspaceStorage $storageDirectory) -Force | Out-Null }
$env:TEMP = Join-Path $workspaceStorage 'tmp'; $env:TMP = $env:TEMP
$env:HF_HOME = Join-Path $workspaceStorage 'cache/huggingface'
$env:HF_HUB_CACHE = Join-Path $env:HF_HOME 'hub'
$env:HF_DATASETS_CACHE = Join-Path $env:HF_HOME 'datasets'
$env:TORCH_HOME = Join-Path $workspaceStorage 'cache/torch'
$env:MPLCONFIGDIR = Join-Path $workspaceStorage 'cache/matplotlib'
$env:PIP_CACHE_DIR = Join-Path $workspaceStorage 'cache/pip'
$env:UV_CACHE_DIR = Join-Path $workspaceStorage 'cache/uv'
$env:XDG_CACHE_HOME = Join-Path $workspaceStorage 'cache/xdg'
$env:PYTHONDONTWRITEBYTECODE = '1'
& $Python $Script @ScriptArguments
exit $LASTEXITCODE
