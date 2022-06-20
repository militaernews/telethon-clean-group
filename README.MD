# telethon-clean-group

This script will go through all members of a given group and remove some of them, if they match certain criteria.

## Usage

This script uses [Telethon](https://docs.telethon.dev/en/stable/) as a client. Replace `config.api_id`
and `config.api_hash` with your
own. You can get them [here](https://my.telegram.org).

Before letting it run in your group, make sure to set `config.testing` to `True`, then inspect the output while running.
If everything works as intended, set it back to `False`. This prevents you from kicking possibly too many people.

## Criteria

There's two main criteria after which a user might get kicked: being a scammer or being overly inactive. You can
optionally set `config.strict` to `True`.

## Contributions

Improvements to the code are welcome :)