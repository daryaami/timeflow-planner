import {SelectSmallOption} from "@/types/selectSmallOption";
import {TaskPriority} from "@/types/task";

const PRIORITIES: SelectSmallOption<TaskPriority | null>[] = [
  {
    value: null,
    label: "No priority",
    icon: "flag",
    color: "inactive",
  },
  {
    value: "MEDIUM",
    label: "Medium",
    icon: "flag",
    color: "medium",
  },
  {
    value: "HIGH",
    label: "High",
    icon: "flag",
    color: "high",
  },
];

export {PRIORITIES}
