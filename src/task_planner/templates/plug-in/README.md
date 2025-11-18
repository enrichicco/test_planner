# Plug-in Brand Templates

This folder contains Plug-in-specific template overrides for strong brandization.

## Usage

Place templates here only when Plug-in requires a different layout or content
from the default multibrand templates.

## Structure

```
plug-in/
  pages/
    dashboard.html       # Plug-in-specific dashboard (if needed)
    custom_page.html     # Plug-in-only pages
```

## Fallback Chain

1. Check `templates/plug-in/{template}`
2. Fallback to `templates/multibrand/{template}`

## Note

- Only create overrides when necessary
- Most pages should use multibrand templates
- base.html is always from multibrand (no override)
