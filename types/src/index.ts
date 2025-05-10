import type { ReadCsvStep, WriteCsvStep } from './io';
import type { AddColumnsStep, FilterStep } from './simple_steps';
import type { AggregateStep } from './aggregate';
import type { AnyJoinStep } from './join';

export type PTablerStep =
  | ReadCsvStep
  | WriteCsvStep
  | AddColumnsStep
  | FilterStep
  | AggregateStep
  | AnyJoinStep;

export type PTablerWorkflow = {
  workflow: PTablerStep[];
};
