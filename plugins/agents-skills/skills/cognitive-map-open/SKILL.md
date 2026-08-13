---
name: cognitive-map-open
description: Open a generated cognitive-map webpage in the local browser. Use when the user asks to open, launch, view, browse, or reopen a cognitive map, including requests such as "open the map", "show the cognitive map", or "launch map.html". Resolve the current project's map automatically or accept an explicit HTML, Markdown, or directory path.
---

# Open a cognitive map

1. Resolve the target from a user-provided path. With no path, look in the current project for `map.html`, then for the most recently modified `*-map.html`.
2. Launch the page with the bundled script, using its absolute path. The launcher regenerates the webpage automatically when it is missing or older than its Markdown source:

   ```sh
   python3 <skill-dir>/scripts/open_map.py [path]
   ```

   Opening a browser is a GUI action. Request the required execution approval instead of bypassing it. Use `--print-only` only for diagnostics and tests.

3. Report the resolved webpage path, that it opened in the default browser, and that graph nodes link back to their explanations in the rendered Markdown content.

If no map source or webpage exists, stop and ask the user to create one with `$agents-skills:cognitive-map`. Do not create an unrelated placeholder map.
