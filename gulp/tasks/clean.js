const del = require('del')
const path = require('path')

module.exports = (gulp, config) => {
  gulp.task('cleanDist', () => del(config.destinationPath))
  gulp.task('cleanGov', () => del(path.join(config.applicationPath, 'templates/vendor/.govuk-frontend')))
  gulp.task('clean', gulp.parallel(['cleanDist', 'cleanGov']))
}
