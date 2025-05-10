/**
 * Defines the type for join operations (excluding cross join) in a workflow.
 * This step joins two tables from the tablespace based on specified columns and join strategy.
 */
export interface JoinStep {
  /** The type of the step, which is always "join" for this operation. */
  type: 'join';

  /** The name of the left table in the tablespace to be joined. */
  left_table: string;

  /** The name of the right table in the tablespace to be joined. */
  right_table: string;

  /** The name to be assigned to the resulting joined table in the tablespace. */
  output_table: string;

  /** A list of column names from the left table to be used for the equi-join. */
  left_on: string[];

  /** A list of column names from the right table to be used for the equi-join. */
  right_on: string[];

  /** The type of join to perform. */
  how: JoinStrategy;
}

/**
 * Defines the type for a cross join operation in a workflow.
 * This step computes the Cartesian product of two tables.
 */
export interface CrossJoinStep {
  /** The type of the step, which is always "join" for this operation. */
  type: 'join'; // Or should this be 'cross_join'? For now, keeping it 'join' as per user doc for steps having a 'type'.

  /** The name of the left table in the tablespace to be joined. */
  left_table: string;

  /** The name of the right table in the tablespace to be joined. */
  right_table: string;

  /** The name to be assigned to the resulting joined table in the tablespace. */
  output_table: string;

  /** The type of join to perform, which is always "cross" for this operation. */
  how: 'cross';
}

/** Defines the possible join strategies for a standard join operation (excluding cross join). */
export type JoinStrategy = 'inner' | 'left' | 'right' | 'outer';

/** Defines any possible join step. */
export type AnyJoinStep = JoinStep | CrossJoinStep;
