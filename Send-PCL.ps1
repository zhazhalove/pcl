# IPP Printer URL and PCL file path
$printerUrl = "http://<printer-ip>:631/ipp/print"   # Change <printer-ip> to your printer's IP
$pclFilePath = "C:\path\to\pclfile.pcl"

# Create PCL6 command file (PCL6 is also known as PCL XL)
# PCL6 commands are binary, so we’ll use hex values.
$pclCommands = @(
    0x1B, 0x45,                    # ESC E: Reset Printer
    0x1B, 0x26, 0x6C, 0x32, 0x48,  # ESC &l2H: Select Tray 2
    [byte[]][char[]]"hello world",  # The text "hello world" in ASCII
    0x1B, 0x45                     # ESC E: Reset Printer after the job
)

# Save PCL commands to the file
[System.IO.File]::WriteAllBytes($pclFilePath, $pclCommands)

# Function to send the file to an IPP printer
Function Send-PCLToIPPPrinter {
    param(
        [string]$PrinterUrl,
        [string]$FilePath
    )

    # Create a new WebClient object
    $webClient = New-Object System.Net.WebClient

    # Set headers for IPP print job
    $webClient.Headers.Add("Content-Type", "application/octet-stream")

    # Upload the PCL file to the printer
    try {
        $response = $webClient.UploadFile($PrinterUrl, "POST", $FilePath)
        Write-Host "PCL file sent successfully."
    } catch {
        Write-Host "Failed to send PCL file. Error: $_"
    }
}

# Call the function to send PCL file to IPP printer
Send-PCLToIPPPrinter -PrinterUrl $printerUrl -FilePath $pclFilePath
