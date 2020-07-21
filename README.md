# HMLR Design System

## Approach to common patterns

- Regular review of proposed patterns
- Multiple avenues in? Could be a sketch on a bit of paper for an initial idea, or a component that is actually already live in a service

## Contribution process

Broadly propose that we follow a similar process to the [GOV.UK Design System community proposals](https://design-system.service.gov.uk/community/propose-a-component-or-pattern/)

- Initial idea
- Prototype
- Reviewed and discussed - either return to the prototyping phase, or continue
- Creation of production ready version
- Create demos and documentation on the design system homepage
- Schedule a post implementation review - how's it going 6 months later?

## Technical approach

- Target platforms. Python/flask (Jinja) and React? Any others? And how do we handle this?
- Prototype kit
- Axure

## Release process

Releases are pushed to internally hosted versions of PyPi and npm on the Nexus repository manager. The process is as follows:

- Get master to the desired state wish to release
- Ensure package.json contains the version number for the tag you are about to release (Following semver principles)
- Set up an additional upstream remote to the version on GitLab (In the common group). Don't replace the main GitHub remote - you want to end up with two remotes.
- Push the code to Gitlab (Something along the lines of `git push gitlab` assuming you called the remote that)
- Go to GitLab and tag the branch. This will cause the pipeline to run and push the npm and PyPi packages to Nexus
- These can then be used in your applications as normal, assuming you have pointed npm and PyPi at Nexus (See `pip.conf` and `.npmrc` files in flask-skeleton-ui for examples of how to do this)
