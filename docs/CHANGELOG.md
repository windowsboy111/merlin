# KCCS-Official discord bot
> windowsboy111

## [Unreleased]
### Added
- README.md badges
### Changed
- in detailed `/ping` command
### Fixed
- `/help` command did not work with commands that does not have aliases
- removed print message content
- `/unban` command now will unban the last member banned if no argument is inputted

## [2.1.1]
### Added
- `/avatar` command
- `/res` command to see CPU / RAM usages
- `/info user`, `/info member`, `/info channel`
- `/help` command now shows command aliases
### Changed
- `/sandbox` command now belongs to cog debug
### Fixed
- now only can use invite in guild
- no attribute hint
- stage is now stable
- member dm welcome
- spam detecion system now won't crash randomly cannot delete the message
- `@Merlin` prefix now works

## [2.1.0]
### Added
- hint logging level
- added description for bot_settings, also changed the description for imports_share
- sandbox command
- more pypi classifiers
### Changed
- consolemod styles are now str, not function
- help command now if have sub-command will have details

## [2.1-b3]
### Added
- error message will split out if restarting the bot failed
- if fail to import extension when bot starts, bot treat start as a reconnect
- build number for bot info
- better look for `/info bot`
- `/kick`, `/ban` will now put reason into discord.py
- `/mute` command now checks if a Muted role exists
- owner is always "sudoers" in guild
- owner check is now handled
- it now checks if it can run inside DMs / PMs
- stdout now logs user issuing commands with prefix `[CMDHDL]\t`
- track last message from a user with `/quote`
- `is_sudoers()` moved to imports_share and new `@chk_sudo()`
### Changed
- Dynamic welcome message
- group `/mc` is now cog `utils`
- `invite me` command now moved to `/invite`
### Removed
- `/nickname` command
### Fixed
- kick commands, those kinds of things do not work
- keep alive func [FATAL]
- a lot of bugs when merging git :/ [FATAL]
- help command will not show hidden commands when wd is `<GLOBAL>`
- couldn't use commands via dm
- it shows that it is in loop with stdout even the loop does not exist in the first place

## [2.1-b2]
### Added
- descriptions for many things (see them with `help()`)
- now a module
### Fixed
- mute command might break

## [2.1-b1]
### Added
- \*load commands now accept command name as argument
- can run Merlin-py as a module
- message when bot joins a guild (being invited)
- detailed `/msgstats` command
- `/info` command
- `/mute` command
- string table (actually json) `ext/wrds.json`
- can now run `/check` without specifying the amount of messages to read (the feature that has been removed in [2.1-a2])
### Removed
- excessive python syntax, imports, f-strings, etc (code formatting)
### Changed
- `/ping` and `/msgstats` are both now in `Debug` cog instead of `Utils`
- `man` cog has been renamed to `mod`
### Fixed
- `/help` command completed
- failed to import `find()` from `imports_init`
- PEP code formatting
- fs reorganizing
- cannot remove warnings
- some grammar issues

## [2.1-b] - 2020-07-09
### Added
- can now hide commands in `/help`
- logging console
- debug / fix mode
- ability to unload, reload and load commands (owner only)
- new warning system that replace the old one and have less security issues
- command error handler
- `.gitignore`
### Changed
- rearranged the repo fs
### Removed
- not working `/emojis` command
- `easteregg.py` will no longer presents in the repo
### Fixed
- preventing the bot from deleting every messages starting with the prefix (the one in [2.1-a2] does not work)
- Duplicated logging what users have issued (especially in the fun cog)

## [2.1-a2] - 2020-07-05
### Added
- allowing users to end all polls in a channel with `/poll end all` (buggy)
- compressed spamming warning system, boosted performance
- compressed bot.py
- bot owner can now run `/eval` python expressions.
### Changed
- compressed the code for a bit without losing readability and performance
- QuickPoll now have special return code representing different errors
- the python shell will now print out the whole traceback
### Removed
- ability for not specifying the amount of messages to read for `/poll check`
- the `/table` command
### Fixed
- check polls might compare str with int
- ~~preventing the bot from deleting every messages starting with `/` (which is the prefix)~~
- bot might read its own error messages in the python debugging channel

## [2.1-a1] - 2020-07-02
### Added
- allowing users to add custom shortcuts for `/mc srv`
- allowing moderators to add `"`s in warnings reasons
### Changed
- Changelogs
### Removed
- sudo mode (moderating)

## [2.1-a] - 2020-06-22
### Added
- Karma system integrated with [Merlin-js]
- more fun commands
### Fixed
- quick poll has runtime error without error messages for the discord users

## [2.0.0]
### Changed
- bot is finally public on github
- optimized
### Removed
- no more verbose mode :O


[Unreleased]:   https://github.com/windowsboy111/Merlin-py/compare/2.1.1...HEAD
[2.1.1]:        https://github.com/windowsboy111/Merlin-py/compare/r2.1.0...2.1.1
[2.1.0]:        https://github.com/windowsboy111/Merlin-py/compare/2.1-b3...r2.1.0
[2.1-b3]:       https://github.com/windowsboy111/Merlin-py/compare/2.1-b2...2.1-b3
[2.1-b2]:       https://github.com/windowsboy111/Merlin-py/compare/2.1-b1...2.1-b2
[2.1-b1]:       https://github.com/windowsboy111/Merlin-py/compare/2.1-b...2.1-b1
[2.1-b]:        https://github.com/windowsboy111/Merlin-py/compare/2.1-a2...2.1-b
[2.1-a2]:       https://github.com/windowsboy111/Merlin-py/compare/2.1-a1...2.1-a2
[2.1-a1]:       https://github.com/windowsboy111/Merlin-py/compare/2.1a...2.1-a1
[2.1-a]:        https://github.com/windowsboy111/Merlin-py/compare/2.0.0...2.1a
