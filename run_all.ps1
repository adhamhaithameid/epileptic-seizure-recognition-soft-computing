param(
  [ValidateSet("auto", "cpu", "gpu")]
  [string]$Device = "auto",
  [switch]$Fresh,
  [switch]$AllowPartial,
  [switch]$StrictDevice,
  [int]$CheckpointEvery = 120,
  [int]$Jobs = 1,
  [int]$SelectionJobs = 1,
  [int]$MaxRows = -1
)

$argsList = @(
  "run_all.py",
  "--device", $Device,
  "--checkpoint-every", "$CheckpointEvery",
  "--jobs", "$Jobs",
  "--selection-jobs", "$SelectionJobs"
)

if ($Fresh) { $argsList += "--fresh" }
if ($AllowPartial) { $argsList += "--allow-partial" }
if ($StrictDevice) { $argsList += "--strict-device" }
if ($MaxRows -gt 0) { $argsList += @("--max-rows", "$MaxRows") }

python @argsList

