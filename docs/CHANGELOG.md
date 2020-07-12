# KCCS-Official discord bot
> windowsboy111

## [Unreleased]
### Added
- message when bot joins a guild (being invited)
- detailed `/msgstats` command
- `/info` command
### Removed
- excessive python syntax, imports, f-strings, etc (code formatting)
### Changed
- `/ping` and `/msgstats` are both now in Debug cog instead of `Utils`
- `man` cog has been renamed to `mod`
### Fixed
- failed to import `find()` from `imports_init`
- cannot remove warnings

## [2.1-b]
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
- eval command for bot owner only
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


[Unreleased]:   https://github.com/windowsboy111/Merlin-py/compare/2.1-b...HEAD
[2.1-b]:        https://github.com/windowsboy111/Merlin-py/compare/2.1-a2...2.1-b
[2.1-a2]:       https://github.com/windowsboy111/Merlin-py/compare/2.1-a1...2.1-a2
[2.1-a1]:       https://github.com/windowsboy111/Merlin-py/compare/2.1a...2.1-a1
[2.1-a]:        https://github.com/windowsboy111/Merlin-py/compare/2.0.0...2.1a