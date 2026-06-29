Adds `is_minor` computed field to `res.partner`.

Depends on `partner_family` and `partner_contact_birthdate`.

A partner is considered a minor when their `age` is strictly below the
`minor_age_limit` configured on the company (default: 18).

The limit is configurable per company in *Settings > Family*.
