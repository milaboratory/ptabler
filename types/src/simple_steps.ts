import type { Expression } from './expressions';

/**
 * Defines a step that adds one or more new columns to an existing table in the tablespace.
 * This operation modifies the specified table in place.
 */
export interface AddColumnsStep {
  /**
   * The type identifier for this step.
   * Must be 'add_columns'.
   */
  type: 'add_columns';

  /**
   * The name of the target DataFrame in the tablespace to which columns will be added.
   */
  table: string;

  /**
   * An array defining the new columns to be added.
   * Each object in the array specifies the name of a new column and the expression to compute its values.
   */
  columns: {
    /**
     * The name of the new column.
     */
    name: string;

    /**
     * An Expression object defining how to compute the column's values.
     * The expression will be evaluated for each row to generate the values for the new column.
     */
    expression: Expression;
  }[];
}

/**
 * Defines a step that filters rows in a table based on a specified condition
 * and outputs the result to a new table in the tablespace.
 */
export interface FilterStep {
  /**
   * The type identifier for this step.
   * Must be 'filter'.
   */
  type: 'filter';

  /**
   * The name of the input table in the tablespace from which rows will be filtered.
   */
  input_table: string;

  /**
   * The name for the resulting filtered table that will be added to the tablespace.
   * This new table will contain only the rows that satisfy the condition.
   */
  output_table: string;

  /**
   * A boolean Expression object used as the filter condition.
   * Rows for which this expression evaluates to true are kept in the output_table.
   * Rows for which it evaluates to false or null are excluded.
   */
  condition: Expression;
}
