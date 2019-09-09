const exec = require('child_process').execSync
const path = require('path')

const packageJson = require('./package.json')
// Check if we've got govuk-frontend installed and install it if not
try {
  require.resolve('govuk-frontend')
} catch(e) {
  console.log('govuk-frontend not found, installing...')
  exec('npm install --no-save govuk-frontend@' + packageJson.config['govuk-frontend-version'])
}

// Check we've got the right version, and die if we don't
const govukFrontendPath = path.dirname(require.resolve('govuk-frontend/README.md'))
const govPackageJson = require(path.join(govukFrontendPath, 'package.json'))
if(govPackageJson.version !== packageJson.config['govuk-frontend-version']) {
  console.error('govuk-frontend', govPackageJson.version, 'found. Expected', packageJson.config['govuk-frontend-version'])
  console.error('Please delete node_modules and npm install again.')
  process.exit(1)
}
