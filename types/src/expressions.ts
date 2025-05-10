export type Expression =
  | ComparisonExpression
  | BinaryArithmeticExpression
  | UnaryArithmeticExpression
  | BooleanLogicExpression
  | NotExpression
  | NullCheckExpression
  | StringJoinExpression
  | HashExpression
  | ColumnReferenceExpression
  | ConstantValueExpression
  | WindowFunctionExpression
  | UnaryStringExpression
  | StringDistanceExpression
  | FuzzyStringFilterExpression;

/** Represents all possible expression types in the system. */
export type ComparisonOperator = 'gt' | 'ge' | 'eq' | 'lt' | 'le' | 'neq';

/** Defines a comparison operation between two expressions. */
export interface ComparisonExpression {
  /** The type of comparison (e.g., 'gt', 'eq'). */
  type: ComparisonOperator;
  /** The left-hand side expression. */
  lhs: Expression;
  /** The right-hand side expression. */
  rhs: Expression;
}

/** Defines the supported binary arithmetic operators. */
export type BinaryArithmeticOperator =
  | 'plus'
  | 'minus'
  | 'multiply'
  | 'truediv'
  | 'floordiv';

/** Represents a binary arithmetic operation between two expressions. */
export interface BinaryArithmeticExpression {
  /** The type of arithmetic operation (e.g., 'plus', 'minus'). */
  type: BinaryArithmeticOperator;
  /** The left-hand side expression. */
  lhs: Expression;
  /** The right-hand side expression. */
  rhs: Expression;
}

/** Defines the supported unary arithmetic operators. */
export type UnaryArithmeticOperator =
  | 'log10'
  | 'log'
  | 'log2'
  | 'abs'
  | 'sqrt'
  | 'minus';

/** Represents a unary arithmetic operation on a single expression. */
export interface UnaryArithmeticExpression {
  /** The type of unary operation (e.g., 'log10', 'abs'). */
  type: UnaryArithmeticOperator;
  /** The expression to operate on. */
  value: Expression;
}

/** Defines the supported boolean list operators. */
export type BooleanListOperator = 'and' | 'or';

/** Represents a boolean logic operation (AND, OR) on a list of expressions. */
export interface BooleanLogicExpression {
  /** The type of boolean operation ('and', 'or'). */
  type: BooleanListOperator;
  /** An array of boolean expressions as operands. */
  operands: Expression[]; // Array of boolean expressions
}

/** Represents a logical NOT operation on a single boolean expression. */
export interface NotExpression {
  /** The type of operation, always 'not'. */
  type: 'not';
  /** The boolean expression to negate. */
  value: Expression;
}

/** Defines the supported null check operators. */
export type NullCheckOperator = 'is_na' | 'is_not_na';

/** Represents a null check operation (is NA, is not NA) on an expression. */
export interface NullCheckExpression {
  /** The type of null check ('is_na', 'is_not_na'). */
  type: NullCheckOperator;
  /** The expression to check for nullity. */
  value: Expression;
}

/** Represents a string join operation on an array of expressions. */
export interface StringJoinExpression {
  /** The type of operation, always 'str_join'. */
  type: 'str_join';
  /** An array of expressions whose string representations will be joined. */
  operands: Expression[];
  /** An optional delimiter string to insert between joined elements. */
  delimiter?: string;
}

/** Defines the supported hash types. Includes common cryptographic and non-cryptographic algorithms. */
export type HashType =
  | 'sha256' // Cryptographic
  | 'sha512' // Cryptographic
  | 'md5' // Cryptographic (use with caution due to vulnerabilities)
  | 'blake3' // Cryptographic
  | 'wyhash' // Non-cryptographic
  | 'xxh3'; // Non-cryptographic

/** Defines the encoding for the hash output. */
export type HashEncoding = 'hex' | 'base64';

/** Represents a hashing operation on an expression. */
export interface HashExpression {
  /** The specific type of hash algorithm to apply. */
  type: HashType;
  /** The expression whose value will be hashed. */
  value: Expression;
  /** The encoding for the output hash string. */
  encoding: HashEncoding;
}

/** Represents a reference to a column by its name. */
export interface ColumnReferenceExpression {
  /** The type of operation, always 'col'. */
  type: 'col';
  /** The name of the column to reference. */
  name: string;
}

/** Represents a constant literal value (string, number, boolean, or null). */
export interface ConstantValueExpression {
  /** The type of operation, always 'const'. */
  type: 'const';
  /** The constant value. */
  value: string | number | boolean | null;
}

/** Defines how a column should be ordered, either by name or by an object specifying column and direction. */
export type OrderBy = string | { column: string; descending?: boolean };

/** Defines the supported window functions. */
export type WindowFunction =
  | 'rank'
  | 'cumsum';

/** Represents a window function applied over a dataset partition. */
export interface WindowFunctionExpression {
  /** The type of window function (e.g., 'rank', 'cumsum'). */
  type: WindowFunction;
  /** The expression on which the window function is applied. */
  input_expression: Expression;
  /** List of column names to partition the data by. */
  partition_by: string[];
  /** Defines the ordering within partitions, can be a single column name, an OrderBy object, or an array of OrderBy objects. */
  order_by: OrderBy | OrderBy[];
}

/** Defines the supported unary string operators. */
export type UnaryStringOperator = 'to_upper' | 'to_lower';

/** Represents a unary string operation on a single expression. */
export interface UnaryStringExpression {
  /** The type of unary string operation (e.g., 'to_upper', 'to_lower'). */
  type: UnaryStringOperator;
  /** The string expression to operate on. */
  value: Expression;
}

/** Defines the supported string distance metrics. */
export type StringDistanceMetric =
  | 'levenshtein'
  | 'optimal_string_alignment'
  | 'jaro_winkler';

/**
 * Represents a string distance/similarity calculation between two expressions.
 * Computes metrics like Levenshtein, Optimal String Alignment, or Jaro-Winkler.
 */
export interface StringDistanceExpression {
  /** The type of operation, always 'string_distance'. */
  type: 'string_distance';
  /** The specific distance metric to use. */
  metric: StringDistanceMetric;
  /** The first string expression. */
  string1: Expression;
  /** The second string expression to compare against. */
  string2: Expression;
  /**
   * If true, the expression returns a similarity score (typically normalized between 0 and 1).
   * If false or undefined, it returns the raw edit distance (e.g., Levenshtein, OSA).
   * Jaro-Winkler inherently returns a similarity score; this flag might be ignored or influence its normalization if applicable.
   */
  return_similarity?: boolean;
}

/** Defines the supported fuzzy string filter distance metrics. */
export type FuzzyFilterDistanceMetric = 'levenshtein' | 'hamming';

/**
 * Represents a fuzzy string filter operation on an expression.
 * This operation compares the string value of an expression (`value`)
 * against another string or string expression (`pattern`) using a specified
 * distance metric (`levenshtein` or `hamming`), returning true if the distance is
 * within the specified `bound`.
 */
export interface FuzzyStringFilterExpression {
  /** The type of operation, always 'fuzzy_string_filter'. */
  type: 'fuzzy_string_filter';
  /** The distance metric to use for the fuzzy comparison. */
  metric: FuzzyFilterDistanceMetric;
  /** The expression whose string value will be compared. */
  value: Expression;
  /** The expression representing the string pattern to compare against. */
  pattern: Expression;
  /** The maximum allowed distance for a match (inclusive). */
  bound: number;
}
