export interface TimeLog {
  id: number;
  start_time: string;   // ISO-строка (DateTime)
  end_time: string;     // ISO-строка (DateTime)
  created_at: string;   // readOnly
  updated_at: string;   // readOnly
  google_event_id?: string | null;
}

export type TaskPriority = "NONE" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface Task {
  id: number;                // readOnly
  title: string;             // max 255
  priority: TaskPriority;
  category?: number | null;  // x-nullable
  due_date?: string | null;  // ISO, x-nullable
  calendar: number;
  completed: boolean;
  created_at: string;        // readOnly
  updated_at: string;        // readOnly
  time_logs: TimeLog[];      // readOnly
  el: null | HTMLElement;
  duration?: number;
  notes?: string | null;
}

export type WithEl<T> = T & { el: Element | null };

// Конкретный UI-тип для этого компонента
export type UiTask = WithEl<Task>;

export interface TaskCreate {
  title: string;
  priority?: TaskPriority;
  category?: number;
  due_date?: string;
  calendar?: number;
  duration?: number;
  notes?:string,
  completed?: boolean,
}
