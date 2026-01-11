export type Line =
  | { type: "text"; value: string; copied?: boolean }
  | { type: "ok"; value: string }
  | { type: "error"; value: string };

export type CommandSpec = {
  usage: string;
  example?: string;
  minArgs?: number;
};
