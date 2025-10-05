export interface SelectSmallOption<T = string | null> {
  label: string;
  value: T;
  icon: string;
  class?: string;
  color?: "inactive" | "medium" | "high";
}
