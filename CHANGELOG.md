# KCCS-Official discord bot
> windowsboy111

## [Unreleased]
### Added
- allowing users to end all polls in a channel with `/poll end all` (buggy)
### Changed
- compressed the code for a bit without losing readability and performance
- QuickPoll now have special return code representing different errors
### Removed
- ability for not specifying the amount of messages to read for `/poll check`
### Fixed
- check polls might compare str with int
- preventing the bot from deleting every messages starting with `/` (which is the prefix)

## [2.1-a1]
### Added
- allowing users to add custom shortcuts for `/mc srv`
- allowing moderators to add `"`s in warnings reasons
### Changed
- Changelogs
### Removed
- sudo mode (moderating)

## [2.1-a]
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


[Unreleased]:   https://github.com/windowsboy111/Merlin-py/compare/3.0-a...HEAD
[3.0-a1]:       https://github.com/windowsboy111/Merlin-py/compare/2.0.0...3.0-a
[2.1-a]:        https://github.com/windowsboy111/Merlin-py/compare/2.0.0...3.0-a
[2.0.0]:        https://github.com/windowsboy111/Merlin-py/releases/tag/2.0.0

[Merlin-js]:    https://github.com/windowsboy111/Merlin-js
