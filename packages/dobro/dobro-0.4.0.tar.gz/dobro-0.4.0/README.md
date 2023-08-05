# dobro

[![PyPI - version](https://img.shields.io/pypi/v/dobro.svg?maxAge=2592000)](https://pypi.python.org/pypi/dobro)
[![PyPI - status](https://img.shields.io/pypi/status/dobro.svg?maxAge=2592000)](https://pypi.python.org/pypi/dobro)
[![Travis CI](https://img.shields.io/travis/snoopdouglas/dobro.svg)](https://travis-ci.org/snoopdouglas/dobro)

Manage DigitalOcean droplets by tag.

## Overview

**dobro** is a tag-centric droplet management CLI tool built on
[doctl](https://github.com/digitalocean/doctl).

dobro isn't so much a tool as a way of working with droplets. It *forces* you to
manage your droplets by tag, which is a good way of doing things if you want to
run lots of automation. It allows you to create, delete, retag and untag
droplets, using tags themselves as criteria.

It names droplets after their IDs*. So, other than that, they are only
identifiable by their tags. You can then resolve which tasks to run on each of
your pool of droplets by checking which tags each one has. DigitalOcean
therefore becomes your dynamic host inventory.

\* *Optional naming is now possible! (in case ya like that.)*

### Example: creating a droplet

```
$ dobro create db postgres

[dobro - info] ssh-key: create: 'dobro-bro'
[dobro - info] droplet: create: 'bro-new-20160729232127-0'
Identity added: /Users/doug/.ssh/id_rsa (/Users/doug/.ssh/id_rsa)
[dobro - info] droplet: wait for ssh: 'bro-new-20160729232127-0'
[dobro - info] droplet: rename: 'bro-new-20160729232127-0' => 'bro-20957830'
Warning: Permanently added '139.59.189.41' (ECDSA) to the list of known hosts.
Connection to 139.59.189.41 closed.
[dobro - info] tag: create: 'db'
[dobro - info] tag: create: 'postgres'
[dobro - info] droplet: tag: 'bro-20957830' => 'db'
[dobro - info] droplet: tag: 'bro-20957830' => 'postgres'
[dobro - info] droplet: ip: 'bro-20957830' => '139.59.189.41'
```

We now have a fresh droplet tagged with `db` and `postgres`. As per usual with
new droplets, you can ssh into it as root.

dobro automatically takes care of ssh-related things too, hence the
`identity added` and `known hosts` output. See [ssh keys](#ssh-keys) for more
info.


## Installation

### Prerequisites

- Python 2.7+ with pip.
- [doctl](https://github.com/digitalocean/doctl) 1.5.0+.

Make sure you have an ssh key pair handy, and that you've authorised doctl
(`doctl auth init`) before going any further.

If your key pair is somewhere other than the usual `~/.ssh/id_rsa`,
[there's an environment variable for that.](#environment-variables)

### Install

```
pip install dobro
```

You might need to stick a `sudo` behind this if on OS X. (which, let's face it,
you probably are, you little tart)


## CLI

```
dobro create [-n|--name <NAME>] [-c|--droplet-count <NUMBER>] <TAGS>
```

Create droplet(s) with the specified tags.

`-n|--name <NAME>` optionally creates the droplets with a name, rather than
using their IDs:

> `dobro create some-tag` => `bro-12345678`
>
> `dobro create -n hello some-tag` => `bro-hello`

`-c|--droplet-count <NUMBER>` specifies the number of droplets. By default, only
one is created.

`<TAGS>` specifies tags to apply, separated by whitespace.

If using `-n` and `-c` together, droplet names will have their number appended
to them.

**Note that prior to 0.4,** `-n` specified the number of droplets.

---

```
dobro list [-a|--all]
```

Information listing on all droplets in namespace. This is just a filtered
`doctl compute droplet list` that'll also notify you if there are any droplets
*not* in your namespace.

`-a|--all` removes the filter.

---

```
dobro tag -c|--criteria <IDs|IPs|TAGS> -t|--tag <TAGS>
```

Adds the specified tags to all matched droplets.

`-c|--criteria` *(required)* specifies any number of IDs, IPv4 public addresses,
and tags.

- All droplets specified by ID or IP will be matched, regardless of how many
  tags are specified (if any).
- Where tags are specified, only droplets with *all* of these tags will be
  matched, *in addition* to droplets matched by ID or IP.

`-t|--tag` *(required)* specifies tags to apply, separated by whitespace.

---

```
dobro untag -c|--criteria <IDs|IPs|TAGS> -t|--tag <TAGS>
```

**Currently unimplemented until the fix for [digitalocean/doctl#119](https://github.com/digitalocean/doctl/issues/119) is
released.**

Removes the specified tags from all matched droplets.

Parameters as with `dobro tag`.

---

```
dobro ssh-key
```

Ensures your public key is up-to-date on DigitalOcean. This is done before any
`create` action too.

---

```
dobro delete <IDs|IPs|TAGS>
```

Deletes all matched droplets.

`<IDs|IPs|TAGS>` are criteria as with `dobro tag`.

---

```
dobro version
```

Displays version information.

---

### Generic flags

`-v|--verbose` includes detailed program breakdown and debugging information in
output.

`-q|--quiet` suppresses all output except warnings and errors.


## Environment variables

Here are the variables that dobro pays attention to, complete with defaults.

```
DOBRO_NAMESPACE="bro"

# Locations of your SSH keys.
DOBRO_SSH_PRIVATE_KEY="$HOME/.ssh/id_rsa"
DOBRO_SSH_PUBLIC_KEY="$DOBRO_SSH_PRIVATE_KEY.pub"

# Tags applied to all new droplets, separated by whitespace (eg. "new db").
DOBRO_NEW_DROPLET_TAGS=""

# Droplet creation arguments.
DOBRO_NEW_DROPLET_ARGS="--region lon1 --size 512mb --image ubuntu-16-04-x64"

# Any other flags for *all* doctl calls - e.g. "--access-token a82be5f..."
DOBRO_DOCTL_EXTRA_ARGS="doctl"
```

**Note that prior to 0.4,** `DOBRO_NEW_DROPLET_ARGS` was `DOBRO_NEW_DROPLET_FLAGS`.


## Workflow

### Namespacing

dobro namespaces all of its droplets in order to distinguish them from non-dobro
droplets. By default, this namespace is `bro` - see
[environment variables](#environment-variables).

Your public key on DigitalOcean will be named `dobro-<NAMESPACE>` - so
`dobro-bro` by default.

### ssh keys

Currently, DigitalOcean instantiates droplets to be ssh'd into as root. You have
two options here: get emailed a password, or authorise a public key. So, unless
you want to receive countless emails and deal with an automation nightmare,
you'll go for the latter option.

dobro actually demands that you use a key, and tries to streamline the process
for you:

- Firstly, your key on DigitalOcean needs a name; see
  [namespacing](#namespacing).
- Before droplet creation, your public key (`~/.ssh/id_rsa.pub` - or see
  [environment variables](#environment-variables)) will be checked against
  DigitalOcean.
  - If it doesn't exist on DigitalOcean, dobro will create it.
  - If it's out of date, dobro will replace it.

- If dobro needs it - for example, when creating a droplet - your key will be
  added to your ssh agent.

dobro will also automatically accept created droplets' host keys because it
ssh's into them; see [renaming](#renaming-created-droplets). We're still waiting
for DigitalOcean to provide host keys for new droplets through its API - which
would make this just a little bit more secure - but until then, you'd have to do
this anyway when ssh'ing in for the first time, so yeah.

#### Note on duplicate keys

DigitalOcean doesn't like storing the same key under two names - so if you get
an error straight after `ssh-key: create`, your key is likely already stored,
so you'll need to delete it.

(hint: `doctl compute ssh-key delete ...`)

### Tags

dobro requires a format for tags in order to distinguish them from IDs and IPs:

```
/[a-zA-Z][a-zA-Z0-9_-]*/
```

In other words: first character must be a letter; others must be either
alphanumeric, or `_`, or `-`.

### Renaming created droplets

As mentioned in the [overview](#overview), dobro names droplets after their IDs
for convenience. In the [example](#example-creating-a-droplet), you may have
noticed a renaming operation taking place. This is because droplets need a name
specified before they are assigned an ID by DigitalOcean.

So, upon creation, they are essentially named after a timestamp, eg.:

```
bro-new-20160729232127-0
```

The format of which being:

```
<NAMESPACE>-new-<TIMESTAMP>-<N>
```

...where `<N>` will increment if creating multiple droplets.

Renaming a droplet in DigitalOcean's eyes is as simple as an API call.
Unfortunately, this doesn't change its internal hostname, so we have to wait for
the droplet to listen, then ssh into it and run the commands needed.

All of this is why you'll see the `wait for ssh:` and `added to known hosts`
lines in dobro's output.

### Hooks

If you want to run hooks before or after any state change, you can add the
following executables to `~/.dobro/hooks/`:

- `~/.dobro/hooks/pre` - executed before any state change
- `~/.dobro/hooks/post` - executed after any state change

Currently, 'state change' comes down to either a droplet creation, deletion or
[un-]tagging.

### Default tags

The [environment variable](#environment-variables) `DOBRO_NEW_DROPLET_TAGS` can
be set as a list of tags (separated by whitespace) - eg. `"_new setup-needed"` -
that will automatically be applied to all droplets upon creation.

This is useful if there is any one-time setup you may need to do on a droplet,
such as locking down SSH access from droplets' default root login.

(Obviously remember to remove them afterwards though! Hint: `dobro untag ...`)


## License

MIT


---

#### Footnote

I'm British, so if you submit PRs attempting to "correct" the spelling of
'initialise' to 'initialize', I will arrange for you to be skewered through the
gizzard by a Worcesterman.

"Wuss-ter-mn".
