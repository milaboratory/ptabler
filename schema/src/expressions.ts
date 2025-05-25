import type { DataType } from './common';

export type Expression =
  | ComparisonExpression
  | BinaryArithmeticExpression
  | UnaryArithmeticExpression
  | CastExpression
  | BooleanLogicExpression
  | NotExpression
  | NullCheckExpression
  | StringJoinExpression
  | HashExpression
  | ColumnReferenceExpression
  | ConstantValueExpression
  | RankExpression
  | CumsumExpression
  | ExtendedUnaryStringExpression
  | StringDistanceExpression
  | FuzzyStringFilterExpression
  | WhenThenOtherwiseExpression
  | SubstringExpression
  | StringReplaceExpression
  | MinMaxExpression
  | FillNaExpression
  | WindowExpression;

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
  | 'negate'
  | 'floor'
  | 'round'
  | 'ceil';

/** Represents a unary arithmetic operation on a single expression. */
export interface UnaryArithmeticExpression {
  /** The type of unary operation (e.g., 'log10', 'abs'). */
  type: UnaryArithmeticOperator;
  /** The expression to operate on. */
  value: Expression;
}

/**
 * Represents a type casting operation that converts the result of an expression to a specified data type.
 */
export interface CastExpression {
  /** The type of operation, always 'cast'. */
  type: 'cast';
  /** The expression whose result will be cast to the target data type. */
  value: Expression;
  /** The target data type to cast the expression result to. */
  dtype: DataType;
  /**
   * Whether to use strict casting mode. If true, conversion errors and overflows will throw exceptions.
   * If false or undefined, uses non-strict mode where failures result in null values. Defaults to false.
   */
  strict?: boolean;
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

/**
 * Defines the encoding for the hash output.
 * - 'hex': Standard hexadecimal encoding.
 * - 'base64': Standard base64 encoding.
 * - 'base64_alphanumeric': Base64 encoding with non-alphanumeric characters (e.g., '+', '/') removed.
 * - 'base64_alphanumeric_upper': Base64 encoding with non-alphanumeric characters removed and the result converted to uppercase.
 */
export type HashEncoding =
  | 'hex'
  | 'base64'
  | 'base64_alphanumeric'
  | 'base64_alphanumeric_upper';

/** Represents a hashing operation on an expression. */
export interface HashExpression {
  /** The specific type of hash algorithm to apply. */
  type: 'hash';
  /** The type of hash algorithm to apply. */
  hashType: HashType;
  /** The encoding for the output hash string. */
  encoding: HashEncoding;
  /** The expression whose value will be hashed. */
  value: Expression;
  /** Optional. Minimal number of entropy bits required. Affects encoding, truncating the result to the shortest string with the requested entropy. No error if bits exceed what the hash offers. */
  bits?: number;
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

/**
 * Represents a rank function applied over a dataset partition.
 * Calculates the rank of each row within its partition based on the specified ordering.
 */
export interface RankExpression {
  /** The type of operation, always 'rank'. */
  type: 'rank';
  /** List of expressions to partition the data by before ranking. The output of these expressions will be used for partitioning. */
  partitionBy: Expression[];
  /** Defines the ordering expressions within partitions to determine the rank. */
  orderBy: Expression[];
  /** Whether to sort in descending order. Defaults to false (ascending). */
  descending?: boolean;
}

/**
 * Represents a cumulative sum function applied over a dataset partition.
 * Calculates the cumulative sum of the 'value' expression within each partition,
 * based on the specified ordering. Values are sorted by value and then by
 * additional_order_by before summing.
 */
export interface CumsumExpression {
  /** The type of operation, always 'cumsum'. */
  type: 'cumsum';
  /** The expression whose values will be cumulatively summed. */
  value: Expression;
  /** Defines additional ordering within partitions for the cumulative sum calculation, in addition to the ordering of the values themselves. */
  additionalOrderBy: Expression[];
  /** List of expressions to partition the data by before calculating the cumulative sum. The output of these expressions will be used for partitioning. */
  partitionBy: Expression[];
  /** Whether to sort in descending order. Defaults to false (ascending). */
  descending?: boolean;
}

/** Defines the supported unary string operators. */
export type UnaryStringOperator = 'to_upper' | 'to_lower';

/** Represents a unary string operation on a single expression. */
export interface ExtendedUnaryStringExpression {
  /** The type of unary string operation (e.g., 'to_upper', 'to_lower', 'str_len'). */
  type: UnaryStringOperator | 'str_len';
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
  returnSimilarity?: boolean;
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

/**
 * Represents a single "when" condition and its corresponding "then" result expression.
 * Used within the WhenThenOtherwiseExpression.
 */
export interface WhenThenClause {
  /** The condition expression. Should evaluate to a boolean. */
  when: Expression;
  /** The result expression if the 'when' condition is true. */
  then: Expression;
}

/**
 * Represents a conditional expression that evaluates a series of "when"
 * conditions and returns the corresponding "then" expression's value.
 * If no "when" condition is met, it returns the value of the "otherwise" expression.
 * This mimics Polars' when/then/otherwise functionality.
 */
export interface WhenThenOtherwiseExpression {
  /** The type of operation, always 'when_then_otherwise'. */
  type: 'when_then_otherwise';
  /** An array of "when/then" clauses to be evaluated in order. */
  conditions: WhenThenClause[];
  /** The expression whose value is returned if none of the "when" conditions are met. */
  otherwise: Expression;
}

/**
 * Represents a substring extraction operation on an expression.
 * Extracts a portion of the string value resulting from the 'value' expression.
 * The substring starts at the 'start' index (0-based).
 * - If 'length' is provided, it specifies the maximum length of the substring.
 * - If 'end' is provided, it specifies the index *before* which the substring ends.
 * - If neither 'length' nor 'end' is provided, the substring extends to the end of the string.
 * - 'length' and 'end' are mutually exclusive.
 * If the requested substring range extends beyond the actual string length,
 * the extraction automatically stops at the end of the string.
 */
export interface SubstringExpression {
  /** The type of operation, always 'substring'. */
  type: 'substring';
  /** The expression whose string value will be used. */
  value: Expression;
  /** The starting position (0-indexed). */
  start: number;
  /** The length of the substring. Mutually exclusive with 'end'. */
  length?: number;
  /** The end position of the substring (exclusive). Mutually exclusive with 'length'. */
  end?: number;
}

/**
 * Represents a string replacement operation.
 * Replaces occurrences of a pattern (regex or literal) in a string expression with a replacement string.
 * The behavior is aligned with Polars' `replace` and `replace_all` functions.
 *
 * - If `literal` is true, the `pattern` is treated as a literal string. Otherwise, it's treated as a regular expression.
 * - If `replaceAll` is true, all occurrences of the pattern are replaced. Otherwise, only the first occurrence is replaced.
 *
 * When using regular expressions (i.e., `literal` is false or undefined):
 * - Positional capture groups can be referenced in the `replacement` string using `$n` or `${n}` (e.g., `$1` for the first group).
 * - Named capture groups can be referenced using `${name}`.
 * - To include a literal dollar sign (`$`) in the replacement, it must be escaped as `$$`.
 */
export interface StringReplaceExpression {
  /** The type of operation, always 'str_replace'. */
  type: 'str_replace';
  /** The input string expression to operate on. */
  value: Expression;
  /** The pattern (regex or literal string) to search for. Can be a string literal or an expression evaluating to a string. */
  pattern: Expression | string;
  /** The replacement string. Can be a string literal or an expression evaluating to a string. Can use $n or ${name} for captured groups if pattern is a regex. */
  replacement: Expression | string;
  /** If true, replace all occurrences of the pattern. If false or undefined, replace only the first. Defaults to false. */
  replaceAll?: boolean;
  /** If true, treat the pattern as a literal string. If false or undefined, treat it as a regex. Defaults to false. */
  literal?: boolean;
}

/** Defines the supported min/max operators. */
export type MinMaxOperator = 'min' | 'max';

/** Represents a min or max operation on a list of expressions. */
export interface MinMaxExpression {
  /** The type of operation ('min' or 'max'). */
  type: MinMaxOperator;
  /** An array of expressions to find the minimum or maximum value from. */
  operands: Expression[];
}

/**
 * Represents a fill NA (null) operation.
 * If the 'input' expression evaluates to null, the 'fillValue' expression is used.
 * Otherwise, the 'input' expression's value is used.
 * This is a convenience shortcut for a common pattern often implemented with
 * conditional expressions (e.g., when(is_na(input), fillValue).otherwise(input)).
 */
export interface FillNaExpression {
  /** The type of operation, always 'fill_na'. */
  type: 'fill_na';
  /** The primary expression to evaluate. */
  input: Expression;
  /** The expression whose value is used if 'input' is null. */
  fillValue: Expression;
}

/**
 * Defines standard aggregation functions that can be used in window expressions.
 */
export type AggregationType =
  | 'sum'
  | 'mean'
  | 'median'
  | 'min'
  | 'max'
  | 'std'
  | 'var'
  | 'count'
  | 'first'
  | 'last'
  | 'n_unique';

/**
 * Represents a window function call.
 * This allows applying an aggregation function over a specific partition of the data.
 */
export interface WindowExpression {
  /** The type of operation, always 'aggregate'. Note: This might be confusing, consider 'window_aggregate' or similar if 'aggregate' is heavily used elsewhere for a different step type. */
  type: 'aggregate';
  /** The aggregation function to apply (e.g., 'sum', 'mean'). */
  aggregation: AggregationType;
  /** The expression to apply the aggregation function to. */
  value: Expression;
  /** List of expressions to partition the data by. The aggregation is performed independently within each partition. */
  partitionBy: Expression[];
}
