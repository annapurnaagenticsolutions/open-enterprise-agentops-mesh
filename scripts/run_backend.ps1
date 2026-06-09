Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\framework\backend"
uvicorn agentops_mesh_api.main:app --reload
