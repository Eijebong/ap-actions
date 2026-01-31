# Apworld github actions

This repository contains a bunch of github actions to help with apworld development

## `Eijebong/ap-actions/fuzz`

This action will take an apworld, setup a base archipelago installation and run my [fuzzer](https://github.com/Eijebong/Archipelago-fuzzer) on the world.

Example:

```yaml
name: Fuzz apworld
on:
  push:
  pull_request:

jobs:
  fuzz:
    runs-on: ubuntu-latest
    steps:
      - uses: Eijebong/ap-actions/fuzz@main
        with:
          apworld-path: worlds/pokemon_crystal
          ap-version: '0.6.1' # Can also be "latest" to always get the latest, stable release of AP.
          python-version: '3.12'
          runs: 500 # This is optional
          yamls-per-run: 1 # This is optional
          meta: path-to-meta.yaml # This is optional
          dump-ignored: false # This is optional
```

## `Eijebong/ap-actions/ap-tests`

This action will take an apworld, setup a base archipelago installation and run the unit tests for that apworld.
Note that unlike the original CI, this action will only run tests related to
the apworld passed in instead of the entirety of the archipelago CI which makes
it much faster and much less prone to getting random fill errors from core verified worlds.

Example:

```yaml
name: Test apworld
on:
  push:
  pull_request:

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: Eijebong/ap-actions/ap-tests@main
        with:
          apworld-path: worlds/pokemon_crystal
          ap-version: '0.6.1'
          python-version: '3.12'
```


## `Eijebong/ap-actions/.github/workflows/release-apworld.yml`

This is a fully fledged reusable workflow that you can use to release your apworld.
It will package your apworld, create a default template for it and then create or update a github release
The following example will trigger the workflow when you create a github
release through the github UI as well as if you push a tag through git.

Example:

```yaml
name: Release APWorld
on:
  push:
    tags:
      - '**'
jobs:
  release:
    uses: Eijebong/ap-actions/.github/workflows/release-apworld.yml@main
    with:
      apworld-path: worlds/pokemon_crystal
      ap-version: '0.6.1'
      python-version: '3.12'
```

> [!NOTE]
> This requires the workflow to have write access to the repository. Make sure `Settings > Actions > General > Workflow permissions` is set to `Read and write permissions`.
