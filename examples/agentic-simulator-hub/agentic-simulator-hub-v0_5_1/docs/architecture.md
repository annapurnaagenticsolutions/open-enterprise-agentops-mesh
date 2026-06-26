# Architecture — v0.5.1

## Static architecture

The hub is a static HTML/CSS/JS site.

```text
index.html
simulators.html
demo-guide.html
architecture.html
roadmap.html
assets/
  css/styles.css
  js/shared.js
  js/simulator-data.js
  js/simulator-engine.js
  js/renderers.js
  js/simulators-page.js
```

## Runtime flow

1. `simulators.html` loads data, engine, renderers, and page controller.
2. The page controller renders simulator filters and simulator list.
3. Selecting a simulator renders only that simulator's field configuration.
4. Dependent field changes are handled in `handleDependentFieldChange`.
5. Submitting the form calls the generator matching the active simulator id.
6. Output is rendered with scorecard, workflow, sections, and isolation note.

## Business scenario fix

Business scenario data is used by both:

- form default population
- output generation

This prevents mismatch between visible input fields and generated result.
