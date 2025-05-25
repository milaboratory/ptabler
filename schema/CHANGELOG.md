# @platforma-open/software-ptabler.types

## 1.5.0

### Minor Changes

- 40f3aab: Refactored the sort step to use expressions instead of column names for defining sort criteria

## 1.4.0

### Minor Changes

- ff909b6: Support for group by expression

## 1.3.0

### Minor Changes

- 3d4f2d2: - Module rename
  - Add Select and WithColumns steps

## 1.2.0

### Minor Changes

- 37ba5b4: - Add new expressions for floor, round, ceil, and cast operations.
  - Use infer_schema & schema_override for CSV parsing.

## 1.1.0

### Minor Changes

- ac10024: - Add Concatenate step for vertical table concatenation; update related interfaces and tests. Introduce new tests for various concatenation scenarios, including error handling for missing tables and columns.
  - Add StringReplaceExpression for string replacement operations; update related interfaces and tests. Introduce functionality to replace patterns in strings with specified replacements, including support for regex and capture groups.
  - Add Sort step implementation with tests for sorting functionality, including handling of null values and stability.
  - Introduce migration guide from ptransform to ptabler, detailing key differences and step mappings.
  - Add FillNaExpression for handling null values
  - Enhance HashExpression to support additional encodings and optional bit truncation. Introduce 'base64_alphanumeric' and 'base64_alphanumeric_upper' encodings, and implement a 'bits' parameter for controlling output length based on entropy. Update related tests to validate new functionality and ensure correct behavior across various hash types and encodings.
  - Add WindowExpression and AggregationType for enhanced window function support. Introduce WindowExpression class for generic window function calls and define AggregationType for standard aggregation operations.
  - Enhance Join step to support column mappings with optional renaming. Refactor left_columns and right_columns to use a list of ColumnMapping objects instead of dictionaries.
  - Add coalesce option to Join step for handling key columns with the same name.

## 1.0.1

### Patch Changes

- 28353d4: chore: bump version
