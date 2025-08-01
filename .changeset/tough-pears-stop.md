---
"@platforma-open/milaboratories.software-ptabler": minor
"@platforma-open/milaboratories.software-ptabler.schema": minor
---

Enhanced struct_field expression with recursive field access, default values, and type casting

- Support recursive field access using arrays: `fields: ["location", "coordinates", "lat"]`
- Add optional `dtype` parameter for automatic type casting of extracted values
- Add optional `default` parameter with scalar values for missing fields
- Maintain full backward compatibility with existing single field access
