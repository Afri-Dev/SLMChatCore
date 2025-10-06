# Verification Script for app.py
# This checks if your app.py has the correct fixes

Write-Host "`n🔍 Verifying app.py has correct error handler fixes...`n" -ForegroundColor Cyan

$appPath = "c:\Users\sepok\SLMChatCore-1\app.py"
$content = Get-Content $appPath -Raw

# Check 1: JSONResponse import
if ($content -match "from fastapi.responses import JSONResponse") {
    Write-Host "✅ JSONResponse import found" -ForegroundColor Green
} else {
    Write-Host "❌ JSONResponse import MISSING" -ForegroundColor Red
    Write-Host "   Add: from fastapi.responses import JSONResponse" -ForegroundColor Yellow
}

# Check 2: Request import
if ($content -match "from fastapi import FastAPI, HTTPException, Request") {
    Write-Host "✅ Request import found" -ForegroundColor Green
} else {
    Write-Host "❌ Request import MISSING" -ForegroundColor Red
    Write-Host "   Add: from fastapi import FastAPI, HTTPException, Request" -ForegroundColor Yellow
}

# Check 3: Exception handlers return JSONResponse
$jsonResponseCount = ([regex]::Matches($content, "return JSONResponse\(")).Count
if ($jsonResponseCount -ge 3) {
    Write-Host "✅ Found $jsonResponseCount JSONResponse returns (need at least 3)" -ForegroundColor Green
} else {
    Write-Host "❌ Only found $jsonResponseCount JSONResponse returns (need at least 3)" -ForegroundColor Red
}

# Check 4: No dict returns in exception handlers
if ($content -match '@app\.exception_handler.*\s+return \{') {
    Write-Host "❌ WARNING: Found exception handler returning dict directly!" -ForegroundColor Red
    Write-Host "   This will cause 'dict' object is not callable error" -ForegroundColor Yellow
} else {
    Write-Host "✅ No dict returns in exception handlers" -ForegroundColor Green
}

# Check 5: Port 7860 (for HF Spaces)
if ($content -match 'port = int\(os\.environ\.get\("PORT", 7860\)\)') {
    Write-Host "✅ Port set to 7860 (HF Spaces compatible)" -ForegroundColor Green
} else {
    Write-Host "⚠️  Port not set to 7860 (check if intentional)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Gray
Write-Host " SUMMARY " -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Gray

$allChecks = $true
if ($content -notmatch "from fastapi.responses import JSONResponse") { $allChecks = $false }
if ($content -notmatch "from fastapi import FastAPI, HTTPException, Request") { $allChecks = $false }
if ($jsonResponseCount -lt 3) { $allChecks = $false }
if ($content -match '@app\.exception_handler.*\s+return \{') { $allChecks = $false }

if ($allChecks) {
    Write-Host "`n✅ app.py is CORRECT and ready to deploy!" -ForegroundColor Green
    Write-Host "`n📤 Next step: Upload this file to Hugging Face Spaces" -ForegroundColor Cyan
    Write-Host "   File location: $appPath" -ForegroundColor White
} else {
    Write-Host "`n❌ app.py needs fixes before deploying!" -ForegroundColor Red
    Write-Host "`n🔧 Run the creation script again or manually fix the issues above" -ForegroundColor Yellow
}

Write-Host "`n"
