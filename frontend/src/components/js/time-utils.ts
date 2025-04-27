const getStartOfMonth = (date: Date): Date => {
  return new Date(date.getFullYear(), date.getMonth(), 1);
}

const getEndOfMonth = (date: Date): Date => {
  return new Date(date.getFullYear(), date.getMonth() + 1, 0);
}

const getMonthStartDates = (start: Date, end: Date): string[] => {
  const result: string[] = [];

  const current = new Date(start.getFullYear(), start.getMonth(), 1);

  while (current <= end) {
    result.push(formatDate(current));
    current.setMonth(current.getMonth() + 1);
  }

  return result;
}

// Вспомогательная функция форматирования
const formatDate = (date: Date): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}



export { getStartOfMonth, getEndOfMonth, getMonthStartDates, formatDate };
