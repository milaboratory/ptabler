/**
 * Defines the supported Polars primitive data types for schema definition.
 *
 * The following are aliases for convenience:
 * - 'Int': maps to 'Int32'
 * - 'Long': maps to 'Int64'
 * - 'Float': maps to 'Float32'
 * - 'Double': maps to 'Float64'
 */
export type DataType =
  | 'Int8'
  | 'Int16'
  | 'Int32'
  | 'Int64'
  | 'UInt8'
  | 'UInt16'
  | 'UInt32'
  | 'UInt64'
  | 'Float32'
  | 'Float64'
  | 'Boolean'
  | 'String'
  | 'Date'
  | 'Datetime'
  | 'Time'
  // Aliases
  | 'Int'
  | 'Long'
  | 'Float'
  | 'Double';

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
   * Optional: An explicit schema definition for the CSV file.
   * Each element in the array defines the schema for a column.
   */
  schema?: ColumnSchema[];
  /** Optional: A list of column names to read from the CSV. If omitted, all columns are read. */
  columns?: string[];
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
