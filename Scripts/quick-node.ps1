# Quick Node.js Launcher with DevTools npm config
$DevTools = "D:\DevTools"
$NodeModules = "$DevTools\NodeJS\global_modules"

# Set npm prefix for this session
$env:NPM_CONFIG_PREFIX = $NodeModules
$env:PATH = "$NodeModules;$env:PATH"

if ($args.Count -gt 0) {
    node $args
} else {
    node
}
