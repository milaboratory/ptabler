---
"@platforma-open/milaboratories.software-ptabler": minor
"@platforma-open/milaboratories.software-ptabler.schema": minor
---

- Added `StructFieldExpression` for accessing nested data structures in JSON imports and other hierarchical data
  - Implements robust error handling using `map_elements` with Python's dict `.get()` method for graceful handling of both null structs and missing fields
  - Supports deeply nested field access with automatic null propagation when intermediate structures are missing  
  - Compatible with inconsistent schemas across records - missing fields return null rather than errors
  - Added comprehensive test coverage including edge cases for missing fields, null structs, and deeply nested non-existent paths
  - TypeScript schema definition with single field extraction support for optimal Polars compatibility