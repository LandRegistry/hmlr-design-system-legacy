var exec = require('child_process').execSync
var semver = require('semver')
var packageJson = require('./package.json')

var installedNpm = exec('npm -v', { encoding: 'utf8' }).trim()

var npmOK = semver.satisfies(installedNpm, packageJson.engines.npm)
var nodeOK = semver.satisfies(process.versions.node, packageJson.engines.node)

if (npmOK) {
  console.log('Found npm', installedNpm)
} else {
  console.error('Installed npm version', installedNpm, 'does not match the semver range', packageJson.engines.npm)
}

if (nodeOK) {
  console.log('Found node', process.versions.node)
} else {
  console.error('Installed node version', process.versions.node, 'does not match the semver range', packageJson.engines.node)
}

process.exit((npmOK && nodeOK) ? 0 : 1)
