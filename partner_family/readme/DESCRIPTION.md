Adds a **Family** partner type to group family members under a single entity.

A family partner (`company_type = 'family'`) acts as a household unit.
Members are linked via the standard `parent_id` / `child_ids` mechanism.

**Family model**

```
Family DUPONT  (company_type='family', no address required)
  ├── Jean DUPONT   (type='contact', own address)
  ├── Marie MARTIN  (type='contact', own address)
  └── Child         (type='contact')
```

Each member keeps their own address. The family itself does not require one.
