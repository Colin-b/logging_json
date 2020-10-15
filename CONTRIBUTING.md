# How to contribute

Everyone is free to contribute on this project.

There are 2 ways to contribute:

- [Submit an issue.](#submitting-an-issue)
- [Submit a pull request.](#submitting-a-pull-request)

## Submitting an issue

Before creating an issue please make sure that it was not already reported.

### When?

- You encountered an issue.
- You have a change proposal.
- You have a feature request.

### How?

1) Go to the *Issues* tab and click on the *New issue* button.
2) Title should be a small sentence describing the request.
3) The comment should contains as much information as possible
    * Actual behavior (including the version you used)
    * Expected behavior
    * Steps to reproduce

## Submitting a pull request

### When?

- You fixed an issue.
- You changed something.
- You added a new feature.

### How?

#### Code

1) Create a new branch based on `develop` branch.
2) Fetch all dev dependencies.
    * Install required python modules using [`pip`](https://pypi.org/project/pip/): **python -m pip install .[testing]**
3) Ensure tests are ok by running them using [`pytest`](http://doc.pytest.org/en/latest/index.html).
4) Follow [Black](https://black.readthedocs.io/en/stable/) code formatting.
    * Install [pre-commit](https://pre-commit.com) python module using pip: **python -m pip install pre-commit**
    * To add the [pre-commit](https://pre-commit.com) hook, after the installation run: **pre-commit install**
5) Add your changes.
    * The commit should only contain small changes and should be atomic.
    * The commit message should follow [those rules](https://chris.beams.io/posts/git-commit/).
6) Add or update at least one [`pytest`](http://doc.pytest.org/en/latest/index.html) test case.
    * Unless it is an internal refactoring request or a documentation update.
    * Each line of code should be covered by the test cases.
7) Add related [changelog entry](https://keepachangelog.com/en/1.1.0/) in the Unreleased section.
    * Unless it is a documentation update.

#### Enter pull request

1) Go to the *Pull requests* tab and click on the *New pull request* button.
2) *base* should always be set to `develop` and it should be compared to your branch.
3) Title should be a small sentence describing the request.
4) The comment should contains as much information as possible
    * Actual behavior (before the new code)
    * Expected behavior (with the new code)
5) A pull request can contain more than one commit, but the entire content should still be [atomic](#what-is-an-atomic-pull-request).

##### What is an atomic pull request

It is important for a Pull Request to be atomic. But with a Pull Request, we measure the "succeed" as the ability to deliver the smallest possible piece of functionality, it can either be composed by one or many atomic commits.

One of the bad practices of a Pull Request is changing things that are not concerned with the functionality that is being addressed, like whitespace changes, typo fixes, variable renaming, etc. If those things are not related to the concern of the Pull Request, it should probably be done in a different one.

One might argue that this practice of not mixing different concerns and small fixes in the same Pull Request violates the Boy Scout Rule because it doesn't allow frequent cleanup. However, cleanup doesn't need to be done in the same Pull Request, the important thing is not leaving the codebase in a bad state after finishing the functionality. If you must, refactor the code in a separate Pull Request, and preferably before the actually concerned functionality is developed, because then if there is a need in the near future to revert the Pull Request, the likelihood of code conflict will be lower. [source](https://medium.com/@fagnerbrack/one-pull-request-one-concern-e84a27dfe9f1)