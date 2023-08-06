gitlab\_release
===============

This python script uses the gitlab api to simplify uploading specific
files from a gitlab-ci build as downloadable resources for a tagged
release.

It can be used in a gitlab-ci.yml stage like:

::

    release:
      stage: release
      script:
        - pip3 install gitlab_release
        - python3 -m gitlab_release $PRIVATE_TOKEN *.zip
      only:
        - tags

Or if you want to bundle a bunch of files into a zip and upload that

::

    release:
      stage: release
      script:
        - pip3 install gitlab_release
        - python3 -m gitlab_release --zip "release-${CI_COMMIT_TAG}.zip" " $PRIVATE_TOKEN *
      only:
        - tags

This currently requires you to put a copy of your PRIVATE\_TOKEN in a
secret CI variable for it to post back to the project

Get token from https://gitlab.com/profile/account

Or better, create a Personal Access Token and use that:
https://gitlab.com/profile/personal\_access\_tokens

Add it to a secret variable called PRIVATE\_TOKEN for the project you’re
building at https://gitlab.com/\<user\>/\<project\>/settings/ci\_cd

On any tagged release the files specified in the glob will then be
availble on the Tags tab of your project


