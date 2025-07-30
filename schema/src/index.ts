import type { ReadCsvStep, ReadNdjsonStep, WriteCsvStep, WriteJsonStep, WriteNdjsonStep, BaseFileReadStep, BaseFileWriteStep } from './io';
import type { AddColumnsStep, FilterStep, SelectStep, WithColumnsStep, WithoutColumnsStep } from './basic_steps';
import type { AggregateStep } from './aggregate';
import type { AnyJoinStep } from './join';
import type { ConcatenateStep } from './concatenate';
import type { SortStep } from './sort';

export type PTablerStep =
  | ReadCsvStep
  | ReadNdjsonStep
  | WriteCsvStep
  | WriteNdjsonStep
  | AddColumnsStep
  | FilterStep
  | AggregateStep
  | AnyJoinStep
  | ConcatenateStep
  | SortStep
  | SelectStep
  | WithColumnsStep
  | WithoutColumnsStep;

export type PTablerWorkflow = {
  workflow: PTablerStep[];
};

// Re-export base interfaces for potential external use
export type { BaseFileReadStep, BaseFileWriteStep };
