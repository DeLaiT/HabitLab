# HabitLab

HabitLab integrates Habitica with GitLab.

### Features:

- [x] Score habit after commit
- [x] Sychronization of GitLab's issues and Habitica's TO-DOs
- [ ] Sychronization of Merge requests and Habitica's TO-DOs

## Usage
 
1. create `config.json` file in project's root. You can find example config in `config_example.json`
2. Add webhook to your gitlab project with url `<address>/gitlab_event/` with Push events and Issues checkbox checked
3. run server with command `python runserver <address>`
