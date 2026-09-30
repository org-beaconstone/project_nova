# Nova desktop update recovery

## Update lifecycle

On macOS and Windows, the updater retains the previous working version
of Nova until the updated application starts successfully.

If installation fails, the updater restores the previous version.
The user can continue working and retry the update later.

## Local data

Recovery preserves cached content and queued drafts. Replacing the
application must not clear locally stored user work.

## Scope

This behaviour applies to application installation and startup during
updates. It does not change synchronization conflict handling or
expand the desktop app’s offline capabilities.
