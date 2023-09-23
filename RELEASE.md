# Releasing the Python SDK

## Step 1: Update version number

You'll need to update the version number in the format `X.Y.Z`.

We are following the SEMVER spec, so:

- increase `X` for breaking changes
- increase `Y` for non-breaking changes that add functionality
- increase `Z` for non-breaking bug fixes

You'll need to bump the version number in `<WEBDEV_ROOT>/python-sdk/lightspark/version.py`.

## Step 2: Changelog

Edit the file `<WEBDEV_ROOT>/sdk/CHANGELOG.md` and add all the relevant changes since the last version.

## Step 3: Tag and publish the release

After merging these changes to main, open the repo in github and publish a new release from the main branch
with the version number you chose in step 1 (tagged `vX.Y.Z`). The release notes should be the same as the
changelog you wrote in step 2.

Publishing the release will automatically trigger a CI job to publish the new version to PyPI.
