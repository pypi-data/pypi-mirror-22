trellobug is a script that files a bug based on a Trello card.  It
also updates the card's description, inserting the URL of the new bug
as the first line.


The script has one mandatory argument:  the short id or URL of a Trello
card.

It uses a config file named .trellobug in the current working directory
or the user's home directory.  A config file of any name can also be passed
in via the `--config` option.

If the config file is not found, it will be created on first run.  The user
will be queried for mandatory config variables.  There are also several optional
config variables.

Here are all the options:

    [bugzilla]
    api_key: a Bugzilla API key
    url: optional URL to a Bugzilla instance; defaults to bugzilla.mozilla.org
    product: Product bugs will be filed in; currently defaults to "Conduit"
    component: Component bugs will be filed in; currently defaults to "General"
    version: Version new bugs will be set to; defaults to "unspecified"

    [trello]
    api_key: Trello API key
    api_secret: Trello API secret
    oauth_token: Trello OAuth token
    oauth_token_secret: Trello OAuth token secret

The `--product`, `--component`, and `--version` command-line options
can be used to specify the Bugzilla product, component, and version,
respectively.  They override the corresponding `[bugzilla]`
config-file options, if set.

If provided, the `--assign` command-line option will assign the bug to
the current user (as identified by the provided Bugzilla API key) and
set the status to `ASSIGNED`.  Otherwise, the bug will be unassigned
and set to the default status.


