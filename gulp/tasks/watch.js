module.exports = (gulp, config) => {
  const watchConfig = {
    cwd: config.sourcePath,
    usePolling: true
  }

  gulp.task('sassWatch', () => {
    const watcher = gulp.watch('scss/**/*.scss', watchConfig, gulp.series(['sass']))

    watcher.on('change', (path, stats) => {
      console.log(path + ' changed')
    })

    watcher.on('add', path => {
      console.log(path + ' added')
    })

    watcher.on('unlink', path => {
      console.log(path + ' removed')
    })
  })

  gulp.task('watch', gulp.parallel(['build', 'sassWatch']))
}
