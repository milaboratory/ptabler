---
"@platforma-open/milaboratories.software-ptabler": minor
"@platforma-open/milaboratories.software-ptabler.schema": minor
---

Add struct field expression for nested data access

Added new `StructFieldExpression` to enable accessing fields within nested data structures like JSON objects. This feature is essential for working with complex data formats where nested structures are common.

Key features:
- Extract single fields from struct objects using `struct.field()` functionality
- Support for deeply nested field access through expression chaining
- Graceful handling of missing fields and struct objects
- Compatible with JSON data processing workflows

The implementation supports single field extraction and provides comprehensive test coverage for various edge cases including missing data scenarios.
