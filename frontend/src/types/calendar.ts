export interface Calendar {
  id:	number,
  user: number,
  calendar_id: string,  // Идентификатор календаря из Google.
  summary: string, //   Название календаря, как отображается у пользователя.
  description?:	string
  owner:	boolean,
  background_color:	string,
  selected:	boolean,
  created_at:	string,
  updated_at: string,
  time_zone: string,
  primary: boolean,
}
