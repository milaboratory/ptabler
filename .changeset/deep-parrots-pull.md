---
"@platforma-open/software-ptabler": minor
"@platforma-open/software-ptabler.types": minor
---

- Add Concatenate step for vertical table concatenation; update related interfaces and tests. Introduce new tests for various concatenation scenarios, including error handling for missing tables and columns.
- Add StringReplaceExpression for string replacement operations; update related interfaces and tests. Introduce functionality to replace patterns in strings with specified replacements, including support for regex and capture groups.
- Add Sort step implementation with tests for sorting functionality, including handling of null values and stability.
- Introduce migration guide from ptransform to ptabler, detailing key differences and step mappings.
- Add FillNaExpression for handling null values
- Enhance HashExpression to support additional encodings and optional bit truncation. Introduce 'base64_alphanumeric' and 'base64_alphanumeric_upper' encodings, and implement a 'bits' parameter for controlling output length based on entropy. Update related tests to validate new functionality and ensure correct behavior across various hash types and encodings.