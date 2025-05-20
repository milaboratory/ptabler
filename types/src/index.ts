import type { ReadCsvStep, WriteCsvStep } from './io';
import type { AddColumnsStep, FilterStep } from './basic_steps';
import type { AggregateStep } from './aggregate';
import type { AnyJoinStep } from './join';
import type { ConcatenateStep } from './concatenate';
import type { SortStep } from './sort';

export type PTablerStep =
  | ReadCsvStep
  | WriteCsvStep
  | AddColumnsStep
  | FilterStep
  | AggregateStep
  | AnyJoinStep
  | ConcatenateStep
  | SortStep;

export type PTablerWorkflow = {
  workflow: PTablerStep[];
};
