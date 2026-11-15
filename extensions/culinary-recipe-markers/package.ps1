$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$extensionDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = $MyInvocation.MyCommand.Path
$package = Get-Content -Raw (Join-Path $extensionDirectory "package.json") | ConvertFrom-Json
$vsixPath = Join-Path $extensionDirectory "$($package.name)-$($package.version).vsix"

if (Test-Path -LiteralPath $vsixPath) {
    Remove-Item -LiteralPath $vsixPath
}

$categories = ($package.categories | ForEach-Object {
    "<Category>$( [System.Security.SecurityElement]::Escape($_) )</Category>"
}) -join ""
$displayName = [System.Security.SecurityElement]::Escape($package.displayName)
$description = [System.Security.SecurityElement]::Escape($package.description)
$publisher = [System.Security.SecurityElement]::Escape($package.publisher)
$name = [System.Security.SecurityElement]::Escape($package.name)
$version = [System.Security.SecurityElement]::Escape($package.version)
$vscodeEngine = [System.Security.SecurityElement]::Escape($package.engines.vscode)

$manifest = @"
<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Language="en-US" Id="$name" Version="$version" Publisher="$publisher" />
    <DisplayName>$displayName</DisplayName>
    <Description xml:space="preserve">$description</Description>
    <Categories>$categories</Categories>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="$vscodeEngine" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui" />
    </Properties>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code" />
  </Installation>
  <Dependencies />
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" />
    <Asset Type="Microsoft.VisualStudio.Code.Extension" Path="extension/" />
  </Assets>
</PackageManifest>
"@

$contentTypes = @"
<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="text/xml" />
  <Default Extension="vsixmanifest" ContentType="text/xml" />
</Types>
"@

$archive = [System.IO.Compression.ZipFile]::Open(
    $vsixPath,
    [System.IO.Compression.ZipArchiveMode]::Create
)

try {
    foreach ($item in @(
        @{ Name = "[Content_Types].xml"; Content = $contentTypes },
        @{ Name = "extension.vsixmanifest"; Content = $manifest }
    )) {
        $entry = $archive.CreateEntry($item.Name)
        $stream = $entry.Open()
        try {
            $writer = New-Object System.IO.StreamWriter(
                $stream,
                (New-Object System.Text.UTF8Encoding($false))
            )
            try {
                $writer.Write($item.Content)
            }
            finally {
                $writer.Dispose()
            }
        }
        finally {
            $stream.Dispose()
        }
    }

    Get-ChildItem -LiteralPath $extensionDirectory -File -Recurse |
        Where-Object { $_.FullName -ne $scriptPath -and $_.FullName -ne $vsixPath } |
        ForEach-Object {
            $relativePath = $_.FullName.Substring($extensionDirectory.Length + 1)
            $entryName = "extension/" + $relativePath.Replace("\", "/")
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                $archive,
                $_.FullName,
                $entryName,
                [System.IO.Compression.CompressionLevel]::Optimal
            ) | Out-Null
        }
}
finally {
    $archive.Dispose()
}

Write-Output "Created $vsixPath"
