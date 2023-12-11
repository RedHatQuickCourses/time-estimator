# time-estimator
This collection of scripts automatically estimates the time to read/watch/complete a section in quick courses

## estimator-qc.py
- Place at top level of course dir
- looks for adoc files in the modules/chapter#/pages path.
- includes variables for:
  - *reading speed* in words per minute
  - *image *viewing time* in seconds (one size fits all)
  - *code block viewing time* in seconds (one size fits all)
- when run, adds or replaces `:time_estimate:` attribute in relevant section#.adoc file *Note: we may want to change this for layout purposes.*
