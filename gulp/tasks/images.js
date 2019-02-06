const path = require('path')

module.exports = (gulp, config) => {
  gulp.task('appImages', () =>
    gulp
      .src(path.join(config.sourcePath, 'images/**'))
      .pipe(gulp.dest(path.join(config.destinationPath, 'images/app')))
  )

  gulp.task('images', gulp.parallel(['appImages']))
}
