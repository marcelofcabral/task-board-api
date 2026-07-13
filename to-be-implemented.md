## Common business rules

- [x] Only users with access to the board can alter it (read/update/delete) tasks.
- [x] Implement two user roles: viewer and editor.
- [x] Add endpoint to reassign task to different user.
- [ ] Add "column" entity. One-to-many relation with "task" (one column can have many tasks, FK lives in the task).
- [ ] Adapt board to reference columns instead of tasks. One-to-many relation between "board" and "column" (one board can have many columns, FK lives in the column).
