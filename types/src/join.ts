/**
 * Defines the type for join operations (excluding cross join) in a workflow.
 * This step joins two tables from the tablespace based on specified columns and join strategy.
 */
export interface JoinStep {
  /** The type of the step, which is always "join" for this operation. */
  type: 'join';

  /** The name of the left table in the tablespace to be joined. */
  leftTable: string;

  /** The name of the right table in the tablespace to be joined. */
  rightTable: string;

  /** The name to be assigned to the resulting joined table in the tablespace. */
  outputTable: string;

  /** A list of column names from the left table to be used for the equi-join. */
  leftOn: string[];

  /** A list of column names from the right table to be used for the equi-join. */
  rightOn: string[];

  /** The type of join to perform. */
  how: JoinStrategy;

  /** An optional record to select and rename columns from the left table. */
  leftColumns?: Record<string, string>;

  /** An optional record to select and rename columns from the right table. */
  rightColumns?: Record<string, string>;
}

/**
 * Defines the type for a cross join operation in a workflow.
 * This step computes the Cartesian product of two tables.
 */
export interface CrossJoinStep {
  /** The type of the step, which is always "join" for this operation. */
  type: 'join'; // Or should this be 'cross_join'? For now, keeping it 'join' as per user doc for steps having a 'type'.

  /** The name of the left table in the tablespace to be joined. */
  leftTable: string;

  /** The name of the right table in the tablespace to be joined. */
  rightTable: string;

  /** The name to be assigned to the resulting joined table in the tablespace. */
  outputTable: string;

  /** The type of join to perform, which is always "cross" for this operation. */
  how: 'cross';

  /** An optional record to select and rename columns from the left table. */
  leftColumns?: Record<string, string>;

  /** An optional record to select and rename columns from the right table. */
  rightColumns?: Record<string, string>;
}

/** Defines the possible join strategies for a standard join operation (excluding cross join). */
export type JoinStrategy = 'inner' | 'left' | 'right' | 'full';

/** Defines any possible join step. */
export type AnyJoinStep = JoinStep | CrossJoinStep;
