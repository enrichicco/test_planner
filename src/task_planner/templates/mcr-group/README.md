# MCR Group Brand Templates

This folder contains MCR-specific template overrides for strong brandization.

## Usage

Place templates here only when MCR requires a different layout or content
from the default multibrand templates.

## Structure

```
mcr-group/
  pages/
    dashboard.html       # MCR-specific dashboard (if needed)
    custom_page.html     # MCR-only pages
```

## Fallback Chain

1. Check `templates/mcr-group/{template}`
2. Fallback to `templates/multibrand/{template}`

## Note

- Only create overrides when necessary
- Most pages should use multibrand templates
- base.html is always from multibrand (no override)
