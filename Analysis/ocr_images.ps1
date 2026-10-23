param([string]$Root)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null=[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$null=[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.SoftwareBitmap,Windows.Foundation,ContentType=WindowsRuntime]
$null=[Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$taskMethod=[System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
function Await-Result($operation,[Type]$resultType) {
 $task=$taskMethod.MakeGenericMethod($resultType).Invoke($null,@($operation))
 $task.Wait()
 return $task.Result
}
$engine=[Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if($null -eq $engine){throw 'No installed Windows OCR language'}
$results=New-Object System.Collections.Generic.List[object]
$files=Get-ChildItem -LiteralPath (Join-Path $Root 'ocr') -Filter '*.png'
foreach($item in $files){
 try{
  $file=Await-Result ([Windows.Storage.StorageFile]::GetFileFromPathAsync($item.FullName)) ([Windows.Storage.StorageFile])
  $stream=Await-Result ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
  $decoder=Await-Result ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
  $bitmap=Await-Result ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
  $result=Await-Result ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
  $results.Add([pscustomobject]@{index=[int]$item.BaseName;text=$result.Text})
  $bitmap.Dispose();$stream.Dispose()
 }catch{$results.Add([pscustomobject]@{index=[int]$item.BaseName;error=$_.Exception.Message})}
 if($results.Count % 100 -eq 0){Write-Output ('OCR '+$results.Count+'/'+$files.Count)}
}
$results | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Root 'ocr_results.json') -Encoding UTF8
Write-Output ('OCR completed: '+$results.Count)
