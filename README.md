# pre-push-hook
A git hook which does not allow to push to master on Fridays and after 4pm

## Usage
Just try to `git push`, if it is Friday (or weekend) the hook will abort the action.
Also on other days of week you are allowed to push to master only between 8am and 4pm.

### Skip the hook
If you need to push to master and want to skip this script. Add `--no-verify` parameter to git command, example:
`git push --no-verify`

## Installation

### In one repository
Copy the file to your hooks directory, remember to remove the file type suffix and make the file executable.

```sh
cp pre-push.py .git/hooks/pre-push
chmod u+x .git/hooks/pre-push
```

### Globally
Create a global hooks directory.
Copy the file to that directory, remember to remove the file type suffix and make the file executable.
Set the core.hooksPath parameter to your global hooks directory.

Example
```sh
mkdir ~/git-global-hooks
cp pre-push.py ~/git-global-hooks/pre-push
chmod u+x ~/git-global-hooks/pre-push
git config --global core.hooksPath /Users/username/git-global-hooks/
```
## How to remove the global hook

```sh
git config --global --unset core.hooksPath
```
