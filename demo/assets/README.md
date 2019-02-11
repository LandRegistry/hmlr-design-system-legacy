# Frontend assets

Frontend dependencies are managed using `npm` and are tracked in `package.json`. These are pulled together by a [Gulp](http://gulpjs.com/) build process to generate the CSS output for this service. _Note: Where npm, node or Gulp command line tools are discussed below, they should be run inside the docker container_

------

## Building the frontend assets

The gulp build process is encapsulated in the `Gulpfile.js` in the root directory. This loads tasks from the `gulp/tasks` directory. These are run by the commands detailed in the package.json `scripts` section.

### Running the gulp tasks

The build tasks run inside the docker container. To run them you can either user `exec your-app-name-here npm run build` to run the build inside the container, or more simply, just `bashin` to the container like `bashin your-app-name-here`. Once you are in the container, type `npm run build` to do a one off build of the assets.

Alternatively, you can use `npm run dev` if you are going to be working on the CSS/JS repeatedly. This will watch your files for changes and rebuild the assets as necessary.

At the time of writing, the build does not run in the pipeline and must be run inside the Docker container on the developer's laptop. This means that the build artefacts need to be committed into the repository. The following files would need to be committed in, but _should not be manually modified_

- `application/assets/dist/**/*.*`
- `application/templates/vendor/.govuk-frontend/template.html` (This file is copied from the `govuk-frontend` module in `node_modules`. It is checked into the repository, but should not be modified manually.)

Application specific frontend code is held in `application/assets/src` - this is the only place you should be manually editing files.


### `node_modules`
The build tasks are written in Nodejs, and as such the repository contains a package.json which is where dependencies are configured. _Normally_, you would then run `npm install` and these dependencies would be downloaded and put in a `node_modules` folder in the repository root. However, the Dockerfile is configured to install these for you and they are installed to a slightly different location inside the Docker container (See the NODE_PATH environment variable). In order to work with this, the following guidelines should be followed:

1) Don't run `npm install` to install all the packages. You should `rebuild` your docker container and they will be installed for you.

2) If you want to install a new module, run `npm install --package-lock-only packageNameHere` which will add the module to your package.json. You should then run `rebuild hmlr-design-system` and it will install the new package. Alternatively, it is often easier to simply add the line to package.json manually yourself and then do the rebuild.

3) If you want to work on a module directly and would normally use `npm link` - unfortunately you can't because Docker volumes do not support symlinks. Instead, check out a copy of the Git repository to a `node_modules` folder inside your application's repository and work on it there. Any modules installed in `/src/node_modules` will take precedence over the modules installed at `NODE_PATH`

### JavaScript

The JavaScript is organised as a set of [ES6 modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) and bundled for the browser using [Webpack](https://github.com/webpack/docs/wiki/contents). There is a single entry point / bundle (`main.js`) by default, but additional bundles will be created for each `.js` file directly inside the `javascripts` folder.

These top levels bundles can be used to `import` files from the `modules` subfolder, or from `node_modules` (Such as if you wish to include a module from https://npmjs.org/). Webpack is set up to import ES6 modules and CommonJS modules.

No actual JS should be written here. Imports only.

### CSS (SCSS)

Similarly to the JavaScript, the files directly in the `scss` folder represent entry points / bundles, and they import files from the subdirectories. Additional entry points can be created as necessary, but no actual CSS should be written in them.

## Sourcemaps

Sourcemaps are generated for both the CSS and JS output, allowing devtools to map errors back to the original source files (rather than just "line 1, character 37948" of the output bundle).

See https://developers.google.com/web/tools/chrome-devtools/javascript/source-maps#source_maps_in_devtools_sources_panel for info on how to enable these.

## Linting

Run `npm test` to run the linter.

JavaScript is linted with [standardjs](http://standardjs.com/) which is intentionally unconfigurable ([No semicolons - it's fine. Really!](https://github.com/feross/standard#the-rules)) This is gaining widespread adoption including by GOV.UK.

SCSS is linted with [sass-lint](https://github.com/sasstools/sass-lint) but is configured to disable some of the more onerous rules.

## browserslist

A [browserslist](https://github.com/ai/browserslist) file in the root of the repository is used to automatically add CSS vendor prefixes (Via [postcss/autoprefixer](https://github.com/postcss/autoprefixer)) and any JS transformations required (Via [babel-preset-env](https://github.com/babel/babel/tree/master/packages/babel-preset-env)).

If you do not wish to support the same browsers as the defaults, feel free to edit this file.
