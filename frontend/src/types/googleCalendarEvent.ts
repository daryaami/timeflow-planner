export interface GoogleCalendarEvent {
  id: string;              // уникальный id события
  summary: string;         // краткое описание
  status: string;          // статус (confirmed, tentative, cancelled)
  htmlLink: string;        // ссылка на событие в Google Calendar
  created: string;         // дата создания (ISO 8601)
  updated: string;         // дата обновления (ISO 8601)
  start: {
    [key: string]: string | null; // например: date или dateTime, timeZone
  };
  end: {
    [key: string]: string | null;
  };
  user_calendar_id: number;        // id календаря
}
