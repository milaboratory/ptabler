import type { DataType } from './common';

/**
 * Represents the schema definition for a single column.
 */
export interface ColumnSchema {
  /** The name of the column. */
  column: string;
  /** Optional: The expected Polars data type for this column. */
  type?: DataType;
  /** Optional: A specific string to be interpreted as a null value for this column. */
  nullValue?: string;
}

/** Represents the configuration for a step that reads data from a CSV file into the tablespace. */
export interface ReadCsvStep {
  /** The type of the step, which is always 'read_csv' for this operation. */
  type: 'read_csv';
  /** Path to the CSV file to be read. */
  file: string;
  /** The name assigned to the loaded DataFrame in the tablespace. */
  name: string;
  /** Optional: The delimiter character used in the CSV file. */
  delimiter?: string;
  /**
   * Optional: Provides schema information for specific columns.
   * If `noHeader` is true, this field is **required**, and the order of `ColumnSchema`
   * definitions determines the column order in the resulting DataFrame. `infer_schema`
   * is implicitly false in this case.
   * If `noHeader` is false (or not provided):
   *   - If `infer_schema` is `true` (default), these definitions act as overrides
   *     to the types inferred by Polars. Each `ColumnSchema` can specify a `type`
   *     and/or a `nullValue`.
   *   - If `infer_schema` is `false`, these definitions are used directly; for columns
   *     not listed, Polars' default behavior when no type is specified (e.g., reading
   *     as string) will apply.
   */
  schema?: ColumnSchema[];
  /**
   * Optional: Whether to infer the schema from the CSV file using Polars'
   * default inference mechanism (e.g., reading a certain number of rows).
   * Defaults to `true`. If set to `false`, type inference is disabled,
   * and types will rely on the `schema` field or Polars' defaults for
   * columns not specified in `schema`.
   * If `noHeader` is `true`, this field is implicitly `false` and any provided value is ignored.
   */
  infer_schema?: boolean;
  /**
   * Optional: Indicates that the CSV file does not have a header row.
   * If `true`:
   *   - The data is read starting from the very first line.
   *   - A `schema` must be provided, and the order of columns in the `schema` array
   *     defines the column names and their order in the DataFrame.
   *   - `infer_schema` is implicitly `false`, regardless of its provided value.
   * Defaults to `false`.
   */
  noHeader?: boolean;
}

/**
 * Represents the configuration for a step that writes a table from the tablespace to a CSV file.
 */
export interface WriteCsvStep {
  /** The type of the step, which is always 'write_csv' for this operation. */
  type: 'write_csv';
  /** The name of the table in the tablespace to be written. */
  table: string;
  /** Path to the output CSV file. */
  file: string;
  /** Optional: A list of column names to write to the CSV. If omitted, all columns are written. */
  columns?: string[];
  /** Optional: The delimiter character to use in the output CSV file. */
  delimiter?: string;
}

/**
 * Represents the configuration for a step that writes a table from the tablespace to a JSON file.
 */
export interface WriteJsonStep {
  /** The type of the step, which is always 'write_json' for this operation. */
  type: 'write_json';
  /** The name of the table in the tablespace to be written. */
  table: string;
  /** Path to the output JSON file. */
  file: string;
  /** Optional: A list of column names to write to the JSON. If omitted, all columns are written. */
  columns?: string[];
}
